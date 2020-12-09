# Generated by Django 3.0.2 on 2020-11-07 09:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_remitamandatestatusreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('maximum_withdrawal_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('annual_interest_rate', models.DecimalField(decimal_places=2, help_text='Interest rate from 0 - 100', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('interest_calculation_per_year', models.PositiveSmallIntegerField(help_text='The number of times interest will be calculated per year', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
            ],
        ),
    ]