# Generated by Django 3.2.23 on 2023-12-20 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20231220_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='customer_id',
        ),
    ]
