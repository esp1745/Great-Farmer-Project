# Generated by Django 4.0.4 on 2022-10-18 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customer_user_alter_farmer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_type',
        ),
    ]