# Generated by Django 3.2.5 on 2021-10-02 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0010_auto_20211001_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='deforestationreport',
            name='location',
            field=models.CharField(default='default location', max_length=750),
            preserve_default=False,
        ),
    ]
