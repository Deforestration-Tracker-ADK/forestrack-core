# Generated by Django 3.2.5 on 2021-09-11 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_email_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(choices=[('EUN', 'Email_Unverified'), ('D', 'Deleted'), ('U', 'Unapproved'), ('A', 'Approved')], default='EUN', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False, verbose_name='email_verified'),
        ),
    ]
