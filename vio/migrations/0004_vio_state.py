# Generated by Django 3.2.5 on 2021-09-20 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vio', '0003_remove_vio_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='vio',
            name='state',
            field=models.CharField(choices=[('EMAIL_UNVERIFIED', 'Email_Unverified'), ('DELETE', 'Deleted'), ('UNAPPROVED', 'Unapproved'), ('REJECTED', 'Rejected'), ('APPROVED', 'Approved')], default='EMAIL_UNVERIFIED', max_length=25),
        ),
    ]