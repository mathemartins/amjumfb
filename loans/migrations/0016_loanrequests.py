# Generated by Django 3.0.2 on 2020-12-18 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0013_borrower_imageurl'),
        ('loans', '0015_auto_20201116_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(blank=True, max_length=300, null=True)),
                ('request_status', models.CharField(blank=True, choices=[('Granted', 'Granted'), ('Rejected', 'Rejected'), ('Still Processing', 'Still Processing')], default='Still Processing', max_length=20, null=True)),
                ('duration', models.CharField(blank=True, choices=[('Years', 'Years'), ('Months', 'Months'), ('Weeks', 'Weeks'), ('Days', 'Days')], default='Months', max_length=20, null=True)),
                ('repayment_interval', models.CharField(blank=True, choices=[('Yearly', 'Yearly'), ('Monthly', 'Monthly'), ('Weekly', 'Weekly'), ('Daily', 'Daily')], default='Monthly', max_length=20, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('borrower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='borrowers.Borrower')),
            ],
            options={
                'verbose_name': 'loanRequest',
                'verbose_name_plural': 'loanRequests',
                'db_table': 'loanRequest',
                'ordering': ('-timestamp',),
            },
        ),
    ]
