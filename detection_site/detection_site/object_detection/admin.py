from django.contrib import admin
from .models import (ImageFeed, DetectedObject, DetectionHistory)

admin.site.register(ImageFeed)
admin.site.register(DetectedObject)
admin.site.register(DetectionHistory)
