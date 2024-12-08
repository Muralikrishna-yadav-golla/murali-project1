from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('admin/', admin.site.urls),
    path('', include(('videos.urls', 'videos'), namespace='videos')),
]