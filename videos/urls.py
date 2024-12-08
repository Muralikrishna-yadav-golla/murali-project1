from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('list/', views.list_videos, name='list_videos'),
    path('upload/', views.upload_video, name='upload_video'),
]