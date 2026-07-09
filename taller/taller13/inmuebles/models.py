from django.db import models


class Edificio(models.Model):
    TIPO_CHOICES = [
        ("residencial", "Residencial"),
        ("comercial", "Comercial"),
    ]

    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return "%s - %s" % (self.nombre, self.ciudad)


class Departamento(models.Model):
    nombre_completo_propietario = models.CharField(max_length=150)
    costo_departamento = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cuartos = models.PositiveIntegerField()
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.CASCADE,
        related_name="departamentos"
    )

    def __str__(self):
        return "%s - %s" % (self.nombre_completo_propietario,
            self.edificio.nombre
        )