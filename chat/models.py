from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name='receiver')
    message = models.TextField() 
    date = models.DateField(null=True) 
    time = models.TimeField(null=True) 
    seen = models.BooleanField(null=True, default=False)
    
    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ['date', 'time']
        

class UserChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    channel_name = models.TextField()