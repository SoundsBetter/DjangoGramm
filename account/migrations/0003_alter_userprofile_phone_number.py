# Generated by Django 4.2.7 on 2023-11-27 13:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_alter_userprofile_date_of_birth_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=20, unique=True, verbose_name="Phone number"
            ),
        ),
    ]
