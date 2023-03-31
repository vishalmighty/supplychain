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
    PENDING = 'Pending'
    REJECTED = 'Rejected'
    APPROVED = 'Approved'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (APPROVED, 'Approved'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30,blank=True,null=True)
    contact_person = models.CharField(max_length=30, blank=True,null=True)
    quality_score = models.CharField(max_length=30,blank=True,null=True)
    gst_number = models.CharField(max_length=30,blank=True,null=True)
    address = models.CharField(max_length=30,blank=True,null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default-avatar.png')


class SupplierProduct(models.Model):
    type_choices = (
        ('Dairy products','DAIRY PRODUCTS'),
        ('Fruits','FRUITS'),
        ('Vegetables','VEGETABLES'),
        ('Meat and poultry','MEAT AND POULTRY'),
        ('Grains and cereals','Grains and cereals'),
        ('Baked goods and breads','Baked goods and breads'),
        ('Beverages','Beverages'),
        ('Snack foods','Snack foods'),
        ('Condiments and spices','Condiments and spices')
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplierproducts')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quality = models.IntegerField()
    quantity = models.IntegerField()
    type = models.CharField(max_length=50,choices=type_choices)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class SupplierOrder(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    ORDER_STATUS_CHOICES = [
        ('in_cart', 'In Cart'),
        ('order_placed', 'Order Placed'),
    ]
    id = models.AutoField(primary_key=True)
    manufacturer_or_retailers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_placed_by',limit_choices_to={'role__in': ['MANUFACTURER', 'RETAILER']})
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_received_by',limit_choices_to={'role__in': ['SUPPLIER']})
    product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    totalamount = models.FloatField(null=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='in_cart')
    def __str__(self):
        return f"{self.product.name} ordered by {self.id}"


class SupplierOrderRecord(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        ('Customer_Cancelled','Customer_Cancelled')
    ]
    ORDER_STATUS_CHOICES = [
        ('in_cart', 'In Cart'),
        ('order_placed', 'Order Placed'),
    ]
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    manufacturer_or_retailers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_placed_by_record',limit_choices_to={'role__in': ['MANUFACTURER', 'RETAILER']})
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_received_by_record',limit_choices_to={'role__in': ['SUPPLIER']})
    product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, related_name='orders_record')
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    totalamount = models.FloatField(null=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='in_cart')
    def __str__(self):
        return f"{self.product.name} ordered by {self.id}"
    
class ManufacturerProduct(models.Model):
    type_choices = (
        ('Dairy products','DAIRY PRODUCTS'),
        ('Fruits','FRUITS'),
        ('Vegetables','VEGETABLES'),
        ('Meat and poultry','MEAT AND POULTRY'),
        ('Grains and cereals','Grains and cereals'),
        ('Baked goods and breads','Baked goods and breads'),
        ('Beverages','Beverages'),
        ('Snack foods','Snack foods'),
        ('Condiments and spices','Condiments and spices')
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manufacturerproducts')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quality = models.IntegerField()
    quantity = models.IntegerField()
    type = models.CharField(max_length=50,choices=type_choices)
    is_available = models.BooleanField(default=True)

class ManufacturerOrder(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    ORDER_STATUS_CHOICES = [
        ('in_cart', 'In Cart'),
        ('order_placed', 'Order Placed'),
    ]
    id = models.AutoField(primary_key=True)
    manufacturer_or_retailers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manu_orders_placed_by',limit_choices_to={'role__in': ['RETAILER']})
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manu_orders_received_by',limit_choices_to={'role__in': ['MANUFACTURER']})
    product = models.ForeignKey(ManufacturerProduct, on_delete=models.CASCADE, related_name='manu_orders')
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    totalamount = models.FloatField(null=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='in_cart')
    def __str__(self):
        return f"{self.product.name} ordered by {self.id}"


class ManufacturerOrderRecord(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        ('Customer_Cancelled','Customer_Cancelled')
    ]
    ORDER_STATUS_CHOICES = [
        ('in_cart', 'In Cart'),
        ('order_placed', 'Order Placed'),
    ]
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    manufacturer_or_retailers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manu_orders_placed_by_record',limit_choices_to={'role__in': ['RETAILER']})
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manu_orders_received_by_record',limit_choices_to={'role__in': ['MANUFACTURER']})
    product = models.ForeignKey(ManufacturerProduct, on_delete=models.CASCADE, related_name='manu_orders_record')
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    totalamount = models.FloatField(null=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='in_cart')
    def __str__(self):
        return f"{self.product.name} ordered by {self.id}"