# Generated by Django 3.2.5 on 2021-09-30 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_auto_20210930_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deforestationreports',
            name='lat',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='deforestationreports',
            name='long',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
    ]