from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=20, null=False)
    nickname = models.CharField(max_length=20, null=False)
    email = models.EmailField(verbose_name = "email", max_length = 255, unique = True)
    user_img = models.ImageField(upload_to='accounts', blank=True, null=False)
    user_music = models.FileField(null=True)
    
    def __str__(self):
        if self.user:
            return f'{self.user.get_username()}: {self.name}'
            
        return f'{self.body}'
    