# Generated by Django 3.0.2 on 2020-10-12 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_auto_20201003_0845'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinOneDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_minone', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField(default=3400)),
                ('key', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('who_uses_minone', models.TextField()),
                ('benefit_of_minone_to_lenders', models.TextField()),
                ('benefit_of_minone_to_borrowers', models.TextField()),
                ('users', models.ManyToManyField(blank=True, null=True, to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'Minone Description',
                'verbose_name_plural': 'Minone Description',
                'db_table': 'minone_description',
                'unique_together': {('key',)},
            },
        ),
    ]
