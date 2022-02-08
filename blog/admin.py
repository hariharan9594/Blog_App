from pyexpat import model
from urllib import request
from django.contrib import admin
from blog.models import Post, Profile
# Register your models here.

admin.site.register(Post)
admin.site.register(Profile)