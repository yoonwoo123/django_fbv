from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User # 사용하지 마세요.
# from django.contrib.auth import get_user_model
from django.conf import settings
# settings.AUTH_USER_MODEL
# default 값이 'auth.User'

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    hit = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # CASCADE는 1:N을 묶어줌
    
    def __str__(self):
        return f'<Board ({self.id})> : {self.title}' 
        
    def get_absolute_url(self):
        return reverse('boards:detail', args=[self.pk])