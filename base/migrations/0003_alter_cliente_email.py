# Generated by Django 5.0.6 on 2024-05-11 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_cliente_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]