# Generated by Django 4.1.7 on 2023-03-10 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0013_remove_user_is_details_verified_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplierdetails",
            name="profile_pic",
            field=models.ImageField(
                default="default-avatar.png", upload_to="profile_pics"
            ),
        ),
    ]
