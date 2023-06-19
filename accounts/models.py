from django.db import models

class RequestCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Request Count'
