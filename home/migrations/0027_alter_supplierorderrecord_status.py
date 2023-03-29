# Generated by Django 4.1.7 on 2023-03-29 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0026_alter_supplierorderrecord_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supplierorderrecord",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Completed", "Completed"),
                    ("Cancelled", "Cancelled"),
                    ("Customer_Cancelled", "Customer_Cancelled"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
    ]