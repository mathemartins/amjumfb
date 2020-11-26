# Generated by Django 3.0.2 on 2020-06-20 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_auto_20200617_0103'),
        ('company', '0007_remitamandateactivationdata_loan_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='remitamandateactivationdata',
            name='mandateId',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='remitamandateactivationdata',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='remitamandateactivationdata',
            name='statuscode',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='remitamandateactivationdata',
            name='loan_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loans.Loan'),
        ),
    ]
