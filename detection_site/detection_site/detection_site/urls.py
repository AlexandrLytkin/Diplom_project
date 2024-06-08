"""
URL configuration for detection_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('object_detection/', include('object_detection.urls')),
    path('', RedirectView.as_view(url='/object_detection/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# https://docs.djangoproject.com/en/3.1/howto/static-files/
# Строка "+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)" в коде Django предоставляет возможность
# обслуживать статические файлы, такие как изображения, при разработке приложения.
# Это добавляет маршрут для обработки запросов к статическим файлам в Django URL-конфигурации.
# В данном случае, "static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)" добавляет маршрут для
# обработки запросов к медиафайлам. Параметры "MEDIA_URL" и "MEDIA_ROOT" задаются в файле настроек Django и
# определяют URL-путь и физический путь к медиафайлам соответственно.
# Таким образом, "+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)" позволяет обрабатывать запросы
# к медиафайлам, которые хранятся в указанной директории "MEDIA_ROOT", и возвращать их веб-сервером приложения Django.
# Это важно для отображения и обслуживания статических файлов, таких как изображения, веб-страницами.
