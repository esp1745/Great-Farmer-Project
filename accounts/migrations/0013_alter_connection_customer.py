# Generated by Django 4.0.4 on 2022-11-01 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_post_farmer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='customer',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
        ),
    ]
