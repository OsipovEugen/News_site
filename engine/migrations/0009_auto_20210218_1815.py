# Generated by Django 3.1.6 on 2021-02-18 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0008_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created'], 'verbose_name': 'Коментарий', 'verbose_name_plural': 'Коментарии'},
        ),
    ]