# Generated by Django 3.0.2 on 2020-11-02 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0010_collateraltype_owned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collateraltype',
            name='owned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loans.Collateral'),
        ),
    ]
