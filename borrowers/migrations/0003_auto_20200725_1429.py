# Generated by Django 3.0.2 on 2020-07-25 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0002_auto_20200725_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrower',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='borrowergroup',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, null=True, unique=True),
        ),
    ]
