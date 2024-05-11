from django.db import models

# Create your models here.


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    celular = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, default='123456')
    actividadEconomica = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    ingresos = models.DecimalField(max_digits=10, decimal_places=2)
    pasivos = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.nombre + ' ' + self.apellido
