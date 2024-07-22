from django.db import models
from django.core.exceptions import ValidationError
from .managers import InfraManager


# Create your models here.

class Filiales(models.Model):
    id_filial = models.IntegerField(primary_key=True)
    nombre_filial = models.CharField(max_length=50, unique=True)

    class Meta:    

        verbose_name = 'filial'
        verbose_name_plural = 'filiales'

    def __str__(self):
        return f"{self.id_filial} - {self.nombre_filial}"
    
class Servicios(models.Model):
    id_servicio = models.IntegerField(primary_key=True)
    nombre_servicio = models.CharField(max_length=50, unique=True)
    
    class Meta:    

        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'

    def __str__(self):
        return f"{self.id_servicio} - {self.nombre_servicio}"

class Unidades(models.Model):
    id_unidad = models.IntegerField(primary_key=True)
    nombre_unidad = models.CharField(max_length=50)
    id_servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    
    class Meta:    

        verbose_name = 'unidad'
        verbose_name_plural = 'unidades'

    def __str__(self):
        return f"{self.id_unidad} - {self.nombre_unidad} - {self.id_servicio}"

class Actividad(models.Model):
    id_filial = models.ForeignKey(Filiales, on_delete=models.CASCADE)
    ejercicio = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    id_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
        
    class Meta:    

        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividad'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "id_filial", 
                    "ejercicio",
                    "mes",
                    "id_unidad",
                ],  
                name="unique_actividad_combination"
            )
        ]

    def __str__(self):
        return f"{self.id_filial} - {self.ejercicio} - {self.mes} - {self.id_unidad} - {self.cantidad}"                  

class Infra(models.Model):
    # django por defecta hará la relación contra la primary key del modelo relacionado
    id_filial = models.ForeignKey(Filiales, on_delete=models.CASCADE)
    ejercicio = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    dia = models.PositiveIntegerField()
    hora = models.PositiveIntegerField()
    id_unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE)
    disponible = models.PositiveIntegerField()
    habilitado = models.PositiveIntegerField()
    instalado = models.PositiveIntegerField()

    objects = InfraManager()

    class Meta:
        verbose_name = 'Infraestructura'
        verbose_name_plural = 'Infraestructura'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "id_filial", 
                    "ejercicio",
                    "mes",
                    "dia",
                    "hora",
                    "id_unidad"
                ],  
                name="unique_infra_combination"
            )
        ]

    def __str__(self):
        return f"{self.id_filial}_{self.ejercicio}_{self.mes}_{self.hora}_{self.id_unidad}"
    

