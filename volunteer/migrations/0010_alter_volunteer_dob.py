# Generated by Django 3.2.5 on 2021-09-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0009_remove_volunteer_specialconditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='dob',
            field=models.DateField(),
        ),
    ]
