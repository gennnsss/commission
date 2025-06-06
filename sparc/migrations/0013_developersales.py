# Generated by Django 5.1.2 on 2025-03-31 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sparc', '0012_sale_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeveloperSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.CharField(max_length=255)),
                ('active_sales', models.DecimalField(decimal_places=2, max_digits=15)),
                ('cancelled_sales', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
    ]
