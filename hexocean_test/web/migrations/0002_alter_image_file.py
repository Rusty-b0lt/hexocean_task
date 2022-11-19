# Generated by Django 3.2.16 on 2022-11-19 12:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])]),
        ),
    ]
