# Generated by Django 3.2 on 2024-11-28 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendedores', '0002_remove_usuario_direccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='ingresos_totales',
        ),
    ]