from django.db import models

from user.models import User

# Create your models here.


class Badge(models.Model):
    id = models.UUIDField(primary_key=True)
    image = models.Field()
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
