from django.db import models
from django.conf import settings

#モデルクラスを定義
class ContactInfo(models.Model):
    Name = models.CharField(max_length=100) 
    Tell = models.CharField(max_length=15, blank=True, null=True)
    Mail = models.EmailField(max_length=100) 
    Text = models.TextField() 
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
