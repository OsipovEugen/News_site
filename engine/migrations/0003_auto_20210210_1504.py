# Generated by Django 3.1.6 on 2021-02-10 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_auto_20210210_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
