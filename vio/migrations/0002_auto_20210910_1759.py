# Generated by Django 3.2.5 on 2021-09-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vio',
            name='address',
            field=models.CharField(blank=True, help_text='Register address of the vio', max_length=250),
        ),
        migrations.AddField(
            model_name='vio',
            name='district',
            field=models.CharField(blank=True, help_text='District of the vio residence', max_length=100),
        ),
    ]
