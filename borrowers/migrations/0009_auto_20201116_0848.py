# Generated by Django 3.0.2 on 2020-11-16 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0008_remove_borrowergroup_meeting_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowerbankaccount',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='borrowerbankaccount',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
