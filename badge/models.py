import uuid
from django.db import models

from user.models import User
from notification.models import Notification


class Badge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='badge_image/')
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class BadgedUser(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)     # 뱃지를 부여 받은 사람

    class Meta:
        unique_together = ['badge', 'user']

    def save(self, *args, **kwargs) -> None:
        super(BadgedUser, self).save(*args, **kwargs)
        Notification.notify_badged(self.user, self.badge.created_by, self)
