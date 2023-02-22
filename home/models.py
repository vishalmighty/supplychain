from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    # groups = models.ManyToManyField(Group, blank=True)
    ROLE_CHOICES = (
        ('SUPPLIER', 'SUPPLIER'),
        ('MANUFACTURER', 'MANUFACTURER'),
        ('RETAILER', 'RETAILER'),
    )

    # profile_photo = models.ImageField(blank=True, null=True, default='default-avatar.png')

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)