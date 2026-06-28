"""
URL configuration for bulletin_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include, re_path
from django.conf.urls.static import static
from django.views.static import serve
from . import settings
import os
from django.http import FileResponse, Http404

def serve_media_production(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    raise Http404("Файл не найден на сервере")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('users/',include('users.urls')),
    path('realtime/',include('realtime.urls')),
    re_path(r'^media/(?P<path>.*)$', serve_media_production),
]
                                                             