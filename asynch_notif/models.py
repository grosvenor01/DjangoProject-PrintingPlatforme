from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.
User = get_user_model()
class notification(models.Model):
    sender = models.ForeignKey(User , on_delete=models.CASCADE , related_name="sender")
    reciever = models.ForeignKey(User , on_delete=models.CASCADE , related_name="reciever")
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)