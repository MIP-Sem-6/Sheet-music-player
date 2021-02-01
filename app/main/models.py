from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Song(models.Model):
    #file = models.FileField(_('File'), upload_to=get_file_upload_path)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    album = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=50, blank=True)
    #cover_image = models.ImageField(_('Cover image'), upload_to=get_cover_upload_path, blank=True)
    play_count = models.IntegerField(default=0)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.title} {self.added_date}'
    
    class Meta:
        unique_together = [['user','title','added_date']]