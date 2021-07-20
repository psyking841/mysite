from django.db import models

# Create your models here.

class Art(models.Model):
    title = models.CharField(max_length=128)
    art = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now=True)