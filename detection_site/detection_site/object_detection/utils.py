import cv2
import numpy as np
from django.core.files.base import ContentFile
from .models import ImageFeed, DetectedObject


VOC_LABELS = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"
]



def process_object_detection(image_feed_id):
    try:
        image_feed = ImageFeed.objects.get(id=image_feed_id)
        image_path = image_feed.image.path
        print(image_path)
        #
        from PIL import Image
        from transformers import pipeline
        img = Image.open(image_path)
        classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
        classifier(img)
        img.show()
        #
        return True

    except ImageFeed.DoesNotExist:
        print("ImageFeed not found.")
        return False

# def process_object_detection(image_feed_id):
#     print('Сработала process_object_detection из util.py')
#     try:
#         image_feed = ImageFeed.objects.get(id=image_feed_id)
#         image_path = image_feed.image.path
#         print(image_path)
#         print(image_feed)
#
#         new_model_path = '/Users/aleksandrlytkin/Diplom_project/detection_site/detection_site/object_detection/mask_rcnn_coco.h5'
#         # new_model_path = '/path/to/your/mask_rcnn_coco.h5'
#
#         segment_image = instance_segmentation()
#         segment_image.load_model(new_model_path)
#         segment_image.model.save('path_to_save_model', save_format='tf')
#
#         output_image_path = '/Users/aleksandrlytkin/Diplom_project/detection_site/detection_site/media/processed_images/processed_images/out_cat.jpeg'
#         segment_image.segmentImage(image_path=image_path, output_image_name=output_image_path)
#
#         # tensorfloww
#         DetectedObject.objects.filter(image_feed=image_feed).delete()  # Очистить существующие обнаруженные объекты для этого изображения
#         # Сохранить обнаруженные объекты в базе данных
#
#         return True  # Вернуть True, если процесс детекции объектов прошел успешно
#
#     except ImageFeed.DoesNotExist:
#         print("ImageFeed not found.")
#         return False


def process_image(image_feed_id):
    try:
        image_feed = ImageFeed.objects.get(id=image_feed_id)
        image_path = image_feed.image.path

        model_path = 'object_detection/mobilenet_iter_73000.caffemodel'
        config_path = 'object_detection/mobilenet_ssd_deploy.prototxt'
        net = cv2.dnn.readNetFromCaffe(config_path, model_path)

        img = cv2.imread(image_path)
        if img is None:
            print("Failed to load image")
            return False

        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5)

        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:
                class_id = int(detections[0, 0, i, 1])
                class_label = VOC_LABELS[class_id]
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"{class_label}: {confidence:.2f}"
                cv2.putText(img, label, (startX + 5, startY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                DetectedObject.objects.create(
                    image_feed=image_feed,
                    object_type=class_label,
                    location=f"{startX},{startY},{endX},{endY}",
                    confidence=float(confidence)
                )

        result, encoded_img = cv2.imencode('.jpg', img)
        if result:
            content = ContentFile(encoded_img.tobytes(), f'processed_{image_feed.image.name}')
            image_feed.processed_image.save(content.name, content, save=True)

        return True

    except ImageFeed.DoesNotExist:
        print("ImageFeed not found.")
        return False
