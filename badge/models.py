from django.db import models

from user.models import User

class Badge(models.Model):
    id = models.UUIDField(primary_key=True)
    image = models.ImageField(upload_to='badge_image/')
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class BadgedUser(models.Model):
    badge_id = models.ForeignKey(Badge, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)     # 뱃지를 부여 받은 사람
