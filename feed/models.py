from django.db import models

from user.models import User

# Create your models here.


class Post(models.Model):
    id = models.UUIDField(primary_key=True)
    content = models.CharField(max_length=2000)
    tagged_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
