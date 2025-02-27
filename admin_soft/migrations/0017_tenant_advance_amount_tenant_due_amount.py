# Generated by Django 5.1.6 on 2025-02-20 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_soft', '0016_alter_tenant_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='advance_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tenant',
            name='due_amount',
            field=models.IntegerField(default=0, max_length=20),
        ),
    ]
