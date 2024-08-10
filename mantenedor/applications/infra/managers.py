from django.db import models
from django.db.models import Sum, Count, F, Value
from django.db.models.functions import Round, Concat
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

class InfraManager(models.Manager):
    def calcular_promedio_diario(self):
        # Filtrar registros donde 'disponible' sea distinto de cero para despues poder horario en donde activos estuvieron disponibles al público
        infra_filtrada = self.filter(disponible__gt=0)
        
        # Agrupar por día y tipo de unidad, y realizar las agregaciones
        promedios_diarios = infra_filtrada.values(
            'id_filial__nombre_filial', 
            'ejercicio', 
            'mes', 
            'dia',
            'id_unidad__id_servicio__nombre_servicio',
            'id_unidad__nombre_unidad'
        ).annotate(
            suma_infra=Sum('disponible'),
            horas_abiertas=Count('hora'),   
        ).annotate(
            promedio_diario=Round(F('suma_infra') / F('horas_abiertas'),2)  # Calcular el promedio diario
        ).order_by("id_filial__nombre_filial", "id_unidad__id_servicio__nombre_servicio", "id_unidad__nombre_unidad", "dia")
        
        return promedios_diarios
        
    def sum_promedios_diarios(self):
        # Obtener los promedios diarios
        promedios_diarios = self.calcular_promedio_diario()

        # Agrupar los promedios diarios por mes y unidad en Python
        sum_promedios_diarios = {}
        for promedio in promedios_diarios:
            key = (promedio['id_filial__nombre_filial'], promedio['ejercicio'], promedio['mes'], promedio['id_unidad__id_servicio__nombre_servicio'], promedio['id_unidad__nombre_unidad'])
            if key not in sum_promedios_diarios:
                sum_promedios_diarios[key] = 0
            sum_promedios_diarios[key] += promedio['promedio_diario']

        # Convertir el diccionario en una lista de diccionarios para poder pasarlo a la vista
        resultado = [
            {
                'id_filial__nombre_filial': key[0],
                'ejercicio': key[1],
                'mes': key[2],
                'id_unidad__id_servicio__nombre_servicio': key[3],
                'id_unidad__nombre_unidad': key[4],
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
        actividades = Actividad.objects.values('id_filial__nombre_filial', 'ejercicio', 'mes', 'id_unidad__id_servicio__nombre_servicio', 'id_unidad__nombre_unidad').annotate(
            total_actividad=Sum('cantidad')
        )

        # Convertir el QuerySet de actividades a un diccionario para un acceso más rápido
        actividad_dict = {(a['id_filial__nombre_filial'], a['ejercicio'], a['mes'], a['id_unidad__id_servicio__nombre_servicio'], a['id_unidad__nombre_unidad']): a['total_actividad'] for a in actividades}

        # Calcular la productividad
        for dato in datos_promedios:
            key = (dato['id_filial__nombre_filial'], dato['ejercicio'], dato['mes'], dato['id_unidad__id_servicio__nombre_servicio'], dato['id_unidad__nombre_unidad'])
            actividad = actividad_dict.get(key, 0)
            dato['actividad'] = actividad
            if dato['total_promedio_mensual'] > 0:
                dato['productividad'] = round(actividad / dato['total_promedio_mensual'], 2)
            else:
                dato['productividad'] = 0

        return datos_promedios
    
    def productividad(self):
        df = pd.DataFrame(self.calcular_productividad()).query('id_unidad__nombre_unidad in ["MQ Adulto", "Box", "UCI", "UTI", "Central", "Rayos X", "Scanner", "Ecografo", "Box Adulto", "Mamografo", "Resonador Magnetico"]')
        
        # Pivotar los datos
        df_pivot = df.pivot_table(
            index=['id_unidad__id_servicio__nombre_servicio', 'id_unidad__nombre_unidad', 'ejercicio', 'mes'],
            columns='id_filial__nombre_filial',
            values='productividad'
        ).reset_index()
        # valores NaN se reemplazan por guión
        df_pivot = df_pivot.fillna('-')

        # Convertir el DataFrame a una lista de diccionarios
        df_pivot_list = df_pivot.to_dict(orient='records')
        
        return df_pivot_list
    
    def promedio_simple_activos_por_mes(self):
        data_reporte = self.filter(disponible__gt=0).values(
            'id_filial__nombre_filial',
            'id_unidad__id_servicio__nombre_servicio',
            'id_unidad__nombre_unidad',
            'ejercicio',
            'mes'
        ).annotate(
            periodo=Concat(
                F('ejercicio'), 
                Value('-'), 
                F('mes'), 
                output_field=models.CharField()
            ),
            promedio=models.Sum('disponible') / models.Count('disponible')
        ).order_by(
            'id_filial__nombre_filial', 
            'id_unidad__id_servicio__nombre_servicio', 
            'id_unidad__nombre_unidad', 
            'ejercicio', 
            'mes')
       
        # Convertir el queryset a un DataFrame de pandas
        df = pd.DataFrame(data_reporte)
        
        # Pivotar los datos
        df_pivot = df.pivot_table(
            index=['id_filial__nombre_filial', 'id_unidad__id_servicio__nombre_servicio', 'id_unidad__nombre_unidad'],
            columns='periodo',
            values='promedio'
        ).reset_index()
        
        # Convertir el DataFrame a una lista de diccionarios para poder pasarlo a la vista HTML
        df_pivot_list = df_pivot.to_dict(orient='records')
                 
        return df_pivot_list
        
    def vista_infra(self, id_filial__nombre_filial, ejercicio, mes, dia):
        datos = self.filter(
            id_filial__nombre_filial=id_filial__nombre_filial,
            ejercicio = ejercicio,
            mes = mes,
            dia  = dia
        ).values(
            'id_filial__nombre_filial', 
            'ejercicio', 
            'mes', 
            'dia',
            'hora',
            'id_unidad__id_servicio__nombre_servicio',
            'id_unidad__nombre_unidad',
            'disponible'
        ).order_by(
            "id_filial__nombre_filial", 
            "id_unidad__id_servicio__nombre_servicio", 
            "id_unidad__nombre_unidad", 
            "dia", 
            "hora")

        if not datos:
            return []

        # Convertir el queryset a un DataFrame de pandas
        df = pd.DataFrame(datos)

         # Pivotar los datos
        df_pivot = df.pivot_table(
            index=[
                'id_filial__nombre_filial', 
                'ejercicio', 
                'mes', 
                'dia',
                'id_unidad__id_servicio__nombre_servicio',
                'id_unidad__nombre_unidad',
            ],
            columns='hora',
            values='disponible'
        ).reset_index()
        
        # Convertir el DataFrame a una lista de diccionarios para poder pasarlo a la vista HTML
        df_pivot_list = df_pivot.to_dict(orient='records')
        

        return df_pivot_list
    
    def vista_update_infra(self, id_filial__nombre_filial, ejercicio, mes, dia, id_unidad__nombre_unidad):
        datos = self.filter(
            id_filial__nombre_filial=id_filial__nombre_filial,
            ejercicio = ejercicio,
            mes = mes,
            dia  = dia,
            id_unidad__nombre_unidad = id_unidad__nombre_unidad
        ).values(
            'id',
            'id_filial__nombre_filial', 
            'ejercicio', 
            'mes', 
            'dia',
            'hora',
            'id_unidad__id_servicio__nombre_servicio',
            'id_unidad__nombre_unidad',
            'disponible',
            'habilitado',
            'instalado'
        ).order_by(
            "id_filial__nombre_filial", 
            "id_unidad__id_servicio__nombre_servicio", 
            "id_unidad__nombre_unidad", 
            "dia", 
            "hora")

        if not datos:
            return []
        
        return datos

    
    