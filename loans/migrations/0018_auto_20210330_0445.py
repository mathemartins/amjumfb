# Generated by Django 3.0.2 on 2021-03-30 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0017_loanrequests_duration_figure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrequests',
            name='request_status',
            field=models.CharField(blank=True, choices=[('Granted', 'Granted'), ('Rejected', 'Rejected'), ('Still Processing', 'Still Processing'), ('Completed', 'Completed')], default='Still Processing', max_length=20, null=True),
        ),
    ]
