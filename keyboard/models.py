from django.db import models

# Create your models here.

class Partition(models.Model):
    name = models.CharField(max_length=30)
    notes= models.JSONField()
