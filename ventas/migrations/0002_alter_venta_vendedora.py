# Generated by Django 3.2 on 2024-11-27 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendedores', '0001_initial'),
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='vendedora',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedores.vendedora'),
        ),
    ]
