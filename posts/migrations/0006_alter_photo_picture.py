# Generated by Django 4.2.7 on 2024-01-28 12:27

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0005_alter_photo_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="picture",
            field=cloudinary.models.CloudinaryField(
                max_length=255, verbose_name="picture"
            ),
        ),
    ]
