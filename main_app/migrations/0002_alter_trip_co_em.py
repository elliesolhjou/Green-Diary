# Generated by Django 5.0.1 on 2024-01-19 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='co_em',
            field=models.IntegerField(default=0.0),
        ),
    ]
