# Generated by Django 5.1.6 on 2025-02-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_soft', '0011_tenant_payment_amount_tenant_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='password',
            field=models.CharField(default='Pavan@123', max_length=128),
            preserve_default=False,
        ),
    ]
