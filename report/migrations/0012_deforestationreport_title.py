# Generated by Django 3.2.5 on 2021-11-03 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0011_deforestationreport_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='deforestationreport',
            name='title',
            field=models.CharField(default='Plant trees in colombo', max_length=255),
            preserve_default=False,
        ),
    ]
