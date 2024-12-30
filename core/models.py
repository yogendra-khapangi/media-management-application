from django.db import models


from django.core.exceptions import ValidationError
import os
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from PIL import Image
from django.http import HttpResponse

# Utility function to validate file size
def validate_file_size(file):
    max_size = 10 * 1024 * 1024  # 10MB
    min_size = 100 * 1024  # 100KB
    if file.size > max_size:
        raise ValidationError("File size exceeds the maximum limit of 10MB.")
    if file.size < min_size:
        raise ValidationError("File size is below the minimum limit of 100KB.")

# Utility function to validate file extension
def validate_file_extension(file):
    valid_extensions = ['.mp3', '.mp4', '.jpeg', '.jpg', '.png', '.gif']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}. Allowed extensions are {', '.join(valid_extensions)}.")

class UploadedFile(models.Model):
    CATEGORY_CHOICES = [
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('image', 'Image'),
    ]

    file = models.FileField(upload_to='uploads/', validators=[validate_file_size, validate_file_extension])
    name = models.CharField(max_length=255, editable=False)
    size = models.PositiveIntegerField(editable=False)
    type = models.CharField(max_length=50, editable=False)
    duration = models.FloatField(null=True, blank=True, editable=False)  # For audio/video files
    dimensions = models.CharField(max_length=50, null=True, blank=True, editable=False)  # For images
    date_uploaded = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, editable=False)

    def save(self, *args, **kwargs):
        # Automatically set metadata before saving
        self.name = self.file.name
        self.size = self.file.size
        ext = os.path.splitext(self.file.name)[1].lower()

        if ext in ['.mp3']:
            self.category = 'audio'
            self.type = 'MP3 Audio'
            try:
                audio = MP3(self.file)
                self.duration = audio.info.length
            except Exception as e:
                self.duration = None

        elif ext in ['.mp4']:
            self.category = 'video'
            self.type = 'MP4 Video'
            try:
                clip = VideoFileClip(self.file.path)
                self.duration = clip.duration
                clip.close()
            except Exception as e:
                self.duration = None

        elif ext in ['.jpeg', '.jpg', '.png', '.gif']:
            self.category = 'image'
            self.type = f"{ext.upper()} Image"
            try:
                with Image.open(self.file) as img:
                    self.dimensions = f"{img.width}x{img.height}"
            except Exception as e:
                self.dimensions = None

        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     # Ensure the file is deleted from the file system
    #     self.file.delete(save=False)
    #     super().delete(*args, **kwargs)

    # def __str__(self):
    #     return self.name

    # def download_file(self):
    #     file_path = self.file.path
    #     with open(file_path, 'rb') as f:
    #         response = HttpResponse(f.read(), content_type="application/octet-stream")
    #         response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    #         return response
