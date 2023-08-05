from django.db import models
from django.conf import settings

class Item(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __unicode__(self):
        return self.key
