# Generated by Django 5.1.6 on 2025-02-13 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_soft', '0002_room_tenant_delete_one'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_number', models.PositiveIntegerField()),
                ('is_vacant', models.BooleanField(default=False)),
                ('pg_name', models.CharField(max_length=100)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beds', to='admin_soft.room')),
            ],
        ),
    ]
