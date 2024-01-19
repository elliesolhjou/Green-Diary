# Generated by Django 5.0.1 on 2024-01-19 21:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('zipcode', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.CharField(blank=True, max_length=500, null=True)),
                ('country', models.CharField(blank=True, max_length=500, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('lat', models.CharField(blank=True, max_length=500, null=True)),
                ('lng', models.CharField(blank=True, max_length=500, null=True)),
                ('place_id', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Distances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_mins', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('from_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_location', to='main_app.locations')),
                ('to_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_location', to='main_app.locations')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200)),
                ('year', models.IntegerField(null=True)),
                ('fuel', models.CharField(choices=[('P', 'Premium'), ('R', 'Regular'), ('M', 'Mid-Grade')], default='R', max_length=1)),
                ('carbon', models.IntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('co_em', models.IntegerField()),
                ('distance', models.IntegerField()),
                ('departure_txt', models.TextField(max_length=255)),
                ('destination_txt', models.TextField(max_length=255)),
                ('departure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_departure', to='main_app.locations')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_destination', to='main_app.locations')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.vehicle')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
