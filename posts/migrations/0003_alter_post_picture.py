# Generated by Django 4.2.7 on 2023-11-22 09:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_alter_post_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="picture",
            field=models.ImageField(upload_to="pictures/"),
        ),
    ]
