# Generated by Django 3.0.2 on 2021-01-12 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0014_auto_20210108_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrower',
            name='cvv',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='borrower',
            name='card_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
