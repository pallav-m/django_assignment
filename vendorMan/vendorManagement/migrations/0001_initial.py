# Generated by Django 5.0.4 on 2024-05-01 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_details', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('vendor_code', models.CharField(max_length=255, unique=True)),
                ('on_time_delivery_rate', models.FloatField(blank=True)),
                ('average_response_time', models.FloatField(blank=True)),
                ('fulfillment_rate', models.FloatField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(max_length=255, unique=True)),
                ('items', models.JSONField(default=dict)),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], max_length=20)),
                ('quality_rating', models.FloatField(blank=True, null=True)),
                ('acknowledgment_date', models.DateTimeField(blank=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendorManagement.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='HistPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_time_delivery_rate', models.FloatField(blank=True, null=True)),
                ('quality_rating_avg', models.FloatField(blank=True, null=True)),
                ('fulfillment_rate', models.FloatField(blank=True, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendorManagement.vendor')),
            ],
        ),
    ]