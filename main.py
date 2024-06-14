from PIL import Image
import torch
from transformers import pipeline, AutoModelForImageClassification, ViTImageProcessor

def detect():
    img = Image.open("/Users/aleksandrlytkin/Diplom_project/bottles.jpg")
    classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
    result = classifier(img)
    print(result)
def other():
    img = Image.open("/Users/aleksandrlytkin/Diplom_project/bottles.jpg")
    model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
    processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')
    with torch.no_grad():
        inputs = processor(images=img, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_label = logits.argmax(-1).item()
    label = model.config.id2label[predicted_label]
    print(label)


if __name__ == '__main__':
    detect()
    other()
