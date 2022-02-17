from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=25)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    image = models.ImageField(default = 'default.jpg', upload_to = "profile_pics")

    def __str__(self):
        return f'{self.user.username } Profile'

    def save(self, *args, **kwargs):
        super(Profile,self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)