# Generated by Django 3.0.2 on 2020-06-19 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_remitamandateactivationdata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='remitacredentials',
            options={'verbose_name': 'Remita Credentials', 'verbose_name_plural': 'Remita Credentials'},
        ),
        migrations.AlterField(
            model_name='remitamandateactivationdata',
            name='mandate_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remitamandateactivationdata',
            name='merchantId',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remitamandateactivationdata',
            name='payer_account',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remitamandateactivationdata',
            name='payer_email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remitamandateactivationdata',
            name='payer_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
