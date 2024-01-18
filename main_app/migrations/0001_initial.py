# Generated by Django 4.2.9 on 2024-01-18 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200)),
                ('year', models.IntegerField(null=True)),
                ('fuel', models.CharField(choices=[('P', 'Premium'), ('R', 'Regular'), ('M', 'Mid-Grade')], default='R', max_length=1)),
                ('carbon', models.IntegerField(default=0)),
                ('mileage', models.IntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output', models.FloatField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('departure', models.TextField(max_length=255)),
                ('destination', models.TextField(max_length=255)),
                ('distance', models.IntegerField()),
                ('carbon', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.vehicle')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
