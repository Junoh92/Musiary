from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    # author = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    artist_official = models.CharField(max_length=50,null=True)
    music_official = models.CharField(max_length=50,null=True)
    album_official = models.CharField(max_length=50,null=True)
    lyric_official = models.TextField() 
    albumart_official = models.CharField(max_length=200,null=True)
    song_official = models.FileField(null=True)
    title = models.CharField(max_length=200,null=True)
    tag = models.CharField(max_length=200,null=True)
    body = models.TextField()
    image = models.ImageField(upload_to='musictest', null=True)
    created_at = models.DateTimeField()
    liked_users = models.ManyToManyField(User, related_name='liked_posts')
    
    def __str__(self):
        if self.user:
            return f'{self.user.get_username()}: {self.body}'
            
        return f'{self.body}'