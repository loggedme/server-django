from django.db import models

# Create your models here.


class EmailValidation(models.Model):
    email = models.EmailField(primary_key=True, max_length=64)
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
