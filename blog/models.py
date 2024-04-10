from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    class Meta:
        permissions = [
            (
                "set_published_status",
                "Can set the status of the post to either publish or not"
            )
        ]