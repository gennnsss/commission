# Generated by Django 5.1.7 on 2025-03-31 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sparc', '0005_profile_image_alter_sale_agent_alter_sale_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
