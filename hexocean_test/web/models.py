from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
class UserTier(models.Model):

    name = models.CharField(max_length=50)
    thumbnail_sizes = ArrayField(models.IntegerField(), default=list)
    original_photo_access = models.BooleanField(default=False)
    expiring_link_access = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class User(AbstractUser):

    tier = models.ForeignKey(UserTier, on_delete=models.RESTRICT, null=True)

class Image(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='images/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
