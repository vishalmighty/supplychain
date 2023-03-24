# Generated by Django 4.1.7 on 2023-03-24 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0023_alter_supplierorder_manufacturer_or_retailers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplierorder",
            name="order_status",
            field=models.CharField(
                choices=[("in_cart", "In Cart"), ("order_placed", "Order Placed")],
                default="in_cart",
                max_length=20,
            ),
        ),
    ]
