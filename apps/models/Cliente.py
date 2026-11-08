
from django.db import models


# TABLA CLIENTES
class Cliente(models.Model):
    id_cliente = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    dni = models.CharField(max_length=8, unique=True)
    edad = models.PositiveSmallIntegerField()
    peso = models.DecimalField(max_digits=5,decimal_places=2 )

    def __str__(self):
        return self.nombre + " " + self.apellido
