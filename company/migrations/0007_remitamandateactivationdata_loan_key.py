# Generated by Django 3.0.2 on 2020-06-19 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20200619_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='remitamandateactivationdata',
            name='loan_key',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]