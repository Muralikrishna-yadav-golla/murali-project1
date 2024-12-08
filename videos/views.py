from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from boto3.session import Session
from .models import Video
from .forms import VideoUploadForm
import re
from datetime import datetime
from django.contrib import messages
from botocore.config import Config
import boto3

# Initialize S3 Session
session = Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_DEFAULT_REGION,
)
s3 = session.resource('s3', config=Config(signature_version='s3v4'))
bucket = s3.Bucket(settings.AWS_BUCKET_NAME)

# Upload Video View
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']
            if video_file.name.split('.')[-1].lower() != 'mp4':
                messages.error(request, "Only MP4 files are supported.")
                return render(request, 'videos/upload.html', {'form': form})

            try:
                current_time = datetime.now().strftime('%H%M%S')
                start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
                end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()

                new_file_name = f"{start_date.strftime('%d%m%Y')}{current_time}-{end_date.strftime('%d%m%Y')}{current_time}.mp4"
                bucket.upload_fileobj(video_file, new_file_name, ExtraArgs={'ContentType': 'video/mp4'})

                Video.objects.create(file_name=new_file_name, start_time=start_date, end_time=end_date)
                messages.success(request, f"Video uploaded successfully as {new_file_name}!")
            except Exception as e:
                messages.error(request, f"Failed to upload to S3: {e}")

            return render(request, 'videos/upload.html', {'form': form})

        messages.error(request, "Invalid form data.")
    else:
        form = VideoUploadForm()

    return render(request, 'videos/upload.html', {'form': form})


# List Videos View
def list_videos(request):
    videos = Video.objects.all().order_by('start_time')
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                videos = Video.objects.filter(start_time__gte=start_date, start_time__lte=end_date).order_by('start_time')
            except ValueError:
                return render(request, 'videos/list_videos.html', {
                    'videos': videos,
                    'error': "Invalid date format. Use YYYY-MM-DD."
                })
    for video in videos:
        video.url = generate_presigned_url("murali-s3-files", video.file_name)
    return render(request, 'videos/list_videos.html', {'videos': videos})

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    s3_client = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'))
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None

