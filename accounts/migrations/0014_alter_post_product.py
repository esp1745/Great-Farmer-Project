# Generated by Django 4.0.4 on 2022-11-02 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_connection_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='product',
            field=models.CharField(max_length=200, null=True),
        ),
    ]