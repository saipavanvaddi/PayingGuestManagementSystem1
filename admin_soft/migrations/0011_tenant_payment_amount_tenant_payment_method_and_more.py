# Generated by Django 5.1.6 on 2025-02-18 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_soft', '0010_tenant_complaints'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='payment_amount',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='payment_method',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='tenant',
            name='payment_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
