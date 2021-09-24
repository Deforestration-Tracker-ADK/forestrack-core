# Generated by Django 3.2.5 on 2021-09-11 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20210911_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_verified',
        ),
        migrations.AlterField(
            model_name='user',
            name='email_token',
            field=models.CharField(max_length=100, unique=True, verbose_name='email_token'),
        ),
    ]