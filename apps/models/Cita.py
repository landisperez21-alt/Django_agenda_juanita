
from django.db import models


class Cita(models.Model):

    TIPOS = [
        ("Virtual", "Virtual"),
        ("Presencial", "Presencial"),
    ]

    id_cita = models.BigAutoField(primary_key=True)
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    direccion = models.CharField( max_length=200, blank=True  )
    referencia = models.CharField( max_length=200,  blank=True  )
    tipo_reunion = models.CharField(  max_length=20,   choices=TIPOS  )
    enlace_virtual = models.URLField(blank=True)
    cliente = models.ForeignKey("apps.Cliente", on_delete=models.PROTECT, related_name="citas",
        db_column="id_cliente"
    )

    def __str__(self):
        return self.motivo
