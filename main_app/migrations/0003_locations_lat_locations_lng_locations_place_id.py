# Generated by Django 5.0.1 on 2024-01-18 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_locations'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='lat',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='locations',
            name='lng',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='locations',
            name='place_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
