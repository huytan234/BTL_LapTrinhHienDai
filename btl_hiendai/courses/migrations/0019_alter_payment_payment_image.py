# Generated by Django 4.2.13 on 2024-06-14 01:36

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_alter_payment_payment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_image',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, null=True),
        ),
    ]
