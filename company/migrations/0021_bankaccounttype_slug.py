# Generated by Django 3.0.2 on 2020-11-08 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0020_bankaccounttype_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccounttype',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
