# Generated by Django 3.0.2 on 2020-11-16 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0021_bankaccounttype_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccounttype',
            name='color_code',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
