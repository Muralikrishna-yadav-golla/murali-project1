from django.db import models

class Video(models.Model):
    file_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name