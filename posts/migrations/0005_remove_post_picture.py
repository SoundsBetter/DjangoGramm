# Generated by Django 4.2.7 on 2023-11-23 11:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0004_alter_post_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="picture",
        ),
    ]