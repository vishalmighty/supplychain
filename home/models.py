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

class SupplierDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(blank=True, null=True)
    contact_person = models.CharField(max_length=20, blank=True)
    quality_score = models.BigIntegerField(blank=True, null=True)
    gst_number = models.BigIntegerField(blank=True, null=True)
    

class SupplierProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplierproducts')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quality = models.IntegerField()
    quantity = models.IntegerField()
    type = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name