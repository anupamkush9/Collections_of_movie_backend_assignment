from django.contrib import admin
from blog.models import Post

# Register your models here.
class AdminPost(admin.ModelAdmin):
    list_display = ["title", "body"]

admin.site.register(Post, AdminPost)