# Generated by Django 3.1.6 on 2021-04-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_auto_20210428_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='face_link',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='user',
            name='inst_link',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='user',
            name='lin_ling',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
