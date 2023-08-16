from random import randint

from django.db import models

# Create your models here.


def gen_code():
    code = ''
    for i in range(6):
        code += chr(randint(ord('A'), ord('Z')))
    return code


class EmailValidation(models.Model):
    email = models.EmailField(primary_key=True, max_length=64)
    code = models.CharField(max_length=8, default=gen_code)
    created_at = models.DateTimeField(auto_now_add=True)
