from django.db import models
from django.contrib.auth.models import Permission
import traceback

class RequestCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Request Count'

def getpermissionchoices():
    try:
        features_permissions_list = []
        features_permissions_list.append(( "set_published_status", "Can set the status of the post to either publish or not"))
        features_permissions_list.append(( "post", "Post"))
        features_permissions_list.append(( "moviecollection", "MovieCollection"))
        features_permissions_list.append(( "collection", "Collection"))
        features_permissions_list.append(( "movie", "Movie"))
        # changes for post title wise permission
        from blog.models import Post
        post_titles = Post.objects.all().values_list('title', flat=True)
        if post_titles and len(post_titles) > 0:
            post_titles = [(post_title,post_title.replace("_"," ")) for post_title in post_titles]
            features_permissions_list.extend(post_titles)
        return features_permissions_list
    except Exception as e:
        print("Exception in getpermissionchoices",e)
        print(traceback.format_exc())

class UserPermissionCredit(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    permission = models.CharField(max_length=255, choices=getpermissionchoices(), blank=True, null=True)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.permission} - {self.credits} credits"
