# Generated by Django 3.2.5 on 2021-09-11 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vio', '0002_auto_20210910_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vio',
            name='state',
        ),
    ]