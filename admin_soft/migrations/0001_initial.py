# Generated by Django 5.1.6 on 2025-02-12 11:36

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartment_name', models.CharField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('contact_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid 10-digit contact number')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('password', models.CharField(max_length=128)),
                ('role', models.CharField(default='apartment', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('specialty', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=15)),
                ('joining_date', models.DateField()),
                ('hospital', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=150, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('contact_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid 10-digit contact number')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('password', models.CharField(max_length=128)),
                ('role', models.CharField(default='hospital', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('manufacturer', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hospital', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='One',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pg_name', models.CharField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('contact', models.CharField(max_length=15)),
                ('hospital', models.CharField(max_length=255)),
                ('joining_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pg_name', models.CharField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('contact_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Enter a valid 10-digit contact number')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('password', models.CharField(max_length=128)),
                ('role', models.CharField(default='pg', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserHospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('contact_number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(choices=[('doctor', 'Doctor'), ('receptionist', 'Receptionist'), ('pharmacist', 'Pharmacist'), ('other', 'Other Employees')], max_length=20)),
                ('permissions', models.JSONField()),
                ('hospital', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AvailableSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('interval', models.IntegerField()),
                ('hospital', models.CharField(max_length=255)),
                ('is_booked', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_soft.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reason', models.TextField()),
                ('hospital', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('Canceled', 'Canceled'), ('Completed', 'Completed')], default='Scheduled', max_length=10)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_soft.availableslot')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_soft.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_soft.patient')),
            ],
        ),
    ]
