from django.db import models
from django.contrib.auth.models import User
import random

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))
