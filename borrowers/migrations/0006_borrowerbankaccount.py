# Generated by Django 3.0.2 on 2020-11-07 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0018_bankaccounttype'),
        ('borrowers', '0005_auto_20200729_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowerBankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.PositiveIntegerField(unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('interest_start_date', models.DateField(blank=True, help_text='The month number that interest calculation will start from', null=True)),
                ('initial_deposit_date', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('account_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='company.BankAccountType')),
                ('borrower', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account', to='borrowers.Borrower')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Company')),
            ],
        ),
    ]
