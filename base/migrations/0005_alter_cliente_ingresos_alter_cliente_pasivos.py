# Generated by Django 5.0.6 on 2024-05-31 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_cliente_email_alter_cliente_ingresos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='ingresos',
            field=models.DecimalField(decimal_places=30, max_digits=40),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='pasivos',
            field=models.DecimalField(decimal_places=30, max_digits=40),
        ),
    ]
