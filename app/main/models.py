from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Song(models.Model):
    file = models.FileField(upload_to='songs',blank=False,default='aot.mp3')
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100,default=' ')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    album = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=50, blank=True)
    cover_image = models.ImageField(default='default_cover.jpg',upload_to='cover_images')
    play_count = models.IntegerField(default=0)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.title} {self.album}'
    
    class Meta:
        unique_together = [['user','title','added_date']]