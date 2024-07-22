from django.db import models
from django.db.models import Sum, Count, F, FloatField
from django.db.models.functions import Round, Cast



class InfraManager(models.Manager):
    def calcular_promedio_diario(self):
        # Filtrar registros donde 'disponible' sea distinto de cero para despues poder horario en donde activos estuvieron disponibles al público
        infra_filtrada = self.filter(disponible__gt=0)
        
        # Agrupar por día y tipo de unidad, y realizar las agregaciones
        promedios_diarios = infra_filtrada.values('ejercicio', 'mes', 'dia', 'id_unidad').annotate(
                suma_infra=Cast(Sum('disponible'), FloatField()),  # Convertir 'disponible' a FloatField
                horas_abiertas=Cast(Count('hora'), FloatField())   # Asegurar que horas_abiertas sea un FloatField
            ).annotate(
                promedio_diario=Round(F('suma_infra') / F('horas_abiertas'),2)  # Calcular el promedio diario
            ).order_by("id_unidad", "dia")
        
        return promedios_diarios
        
    def sum_promedios_diarios(self):
        # Obtener los promedios diarios
        promedios_diarios = self.calcular_promedio_diario()

        # Agrupar los promedios diarios por mes y unidad en Python
        sum_promedios_diarios = {}
        for promedio in promedios_diarios:
            key = (promedio['ejercicio'], promedio['mes'], promedio['id_unidad'])
            if key not in sum_promedios_diarios:
                sum_promedios_diarios[key] = 0
            sum_promedios_diarios[key] += promedio['promedio_diario']

        # Convertir el diccionario en una lista de diccionarios para poder pasarlo a la vista
        resultado = [
            {
                'ejercicio': key[0],
                'mes': key[1],
                'id_unidad': key[2],
                'total_promedio_mensual': promedio_mensual
            }
            for key, promedio_mensual in sum_promedios_diarios.items()
        ]

        return resultado
    
    def calcular_productividad(self):
        from .models import Actividad
        # Obtener los datos de promedios diarios sumados
        datos_promedios = self.sum_promedios_diarios()

        # Obtener la actividad por unidad, ejercicio y mes
        actividades = Actividad.objects.values('ejercicio', 'mes', 'id_unidad').annotate(
            total_actividad=Sum('cantidad')
        )

        # Convertir el QuerySet de actividades a un diccionario para un acceso más rápido
        actividad_dict = {(a['ejercicio'], a['mes'], a['id_unidad']): a['total_actividad'] for a in actividades}

        # Calcular la productividad
        for dato in datos_promedios:
            key = (dato['ejercicio'], dato['mes'], dato['id_unidad'])
            actividad = actividad_dict.get(key, 0)
            dato['actividad'] = actividad
            if dato['total_promedio_mensual'] > 0:
                dato['productividad'] = round(actividad / dato['total_promedio_mensual'], 2)
            else:
                dato['productividad'] = 0

        return datos_promedios
    
    