from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class User(AbstractUser):
    is_active = models.BooleanField(default=False)  # Сначала неактивен
    confirmation_code = models.CharField(max_length=6, blank=True, null=True, unique=True)

    def generate_confirmation_code(self):
        self.confirmation_code = f'{random.randint(100000, 999999)}'
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

STARS = [(i, '★' * i) for i in range(1, 6)]  # От 1 до 5

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=STARS)

    def __str__(self):
        return f"{self.product.title} - {'★' * self.stars}"

