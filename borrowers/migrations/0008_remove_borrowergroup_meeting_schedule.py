# Generated by Django 3.0.2 on 2020-11-12 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0007_auto_20201111_0758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowergroup',
            name='meeting_schedule',
        ),
    ]
