# Generated by Django 4.0.4 on 2022-10-29 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_customer_customer_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='classificatoin',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
