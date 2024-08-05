import csv
from django.views.generic import TemplateView, FormView, ListView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from io import StringIO
from .forms import *
from .models import Infra, Filiales, Servicios, Unidades, Actividad
from .utils import *


# Vista que carga la página de inicio
class InicioView(TemplateView):
    """vista que carga la pagina de inicio"""
    template_name="inicio.html"

# Vista que carga el csv de Infra
class cargaCsvInfra(FormView):
    template_name = "infra/carga_infra.html"
    form_class = InfraUploadForm
    success_url = reverse_lazy("infra_app:carga_infra")
    
    def form_valid(self, form):
        # función para el manejo de errores

        file = form.cleaned_data["file"]
        csv_file = StringIO(file.read().decode("utf-8"))
        reader = csv.reader(csv_file, delimiter=";")
        # Saltar la cabecera
        next(reader) 
        
        data = []

        for row in reader:
            try:
                # validaciones INT
                id_filial_csv = parse_int(row[0], "id_filial")
                id_unidad_csv = parse_int(row[5], "id_unidad")
                ejercicio_csv = parse_int(row[1], "ejercicio")
                mes_csv = parse_int(row[2], "mes")
                validar_mes(mes_csv)
                dia_csv = parse_int(row[3], "dia")
                validar_dia(dia_csv)
                hora_csv = parse_int(row[4], "hora")
                validar_hora(hora_csv)
                disponible_csv_str = row[6].replace(',', '.')
                disponible_csv = parse_decimal(disponible_csv_str, "disponible")
                habilitado_csv = parse_decimal(row[7], "habilitado")
                instalado_csv = parse_decimal(row[8], "instalado")

                # validación de negocio
                if disponible_csv > habilitado_csv:
                    raise ValueError(f"Error en la fila {reader.line_num}: Infraestructura disponible no puede ser mayor que infraestructura habilitada")
                if habilitado_csv > instalado_csv:
                    raise ValueError(f"Error en la fila {reader.line_num}: Infraestructura habilitada no puede ser mayor que infraestructura instalada")
                
                infra_instance = Infra(
                    # en esta linea se puede gatillar la excepción de que id filial no existe
                    id_filial= Filiales.objects.get(id_filial=id_filial_csv),  #filial_instance
                    ejercicio=ejercicio_csv,
                    mes=mes_csv,
                    dia=dia_csv,
                    hora=hora_csv,
                    # en esta linea se puede gatillar la excepción de que id unidad no existe
                    id_unidad= Unidades.objects.get(id_unidad=id_unidad_csv),  #unidad_instance
                    disponible=disponible_csv,
                    habilitado=habilitado_csv,
                    instalado=instalado_csv
                )
                
                data.append(infra_instance)

            except IndexError:
                return msg_error(self.request, self, form, "El número de columnas del archivo csv no es válido")          
            except Filiales.DoesNotExist:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: El id_filial ingresado no existe")  
            except Unidades.DoesNotExist:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: El id_unidad ingresado no existe")  
            except Exception as e:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: La carga ha presentado un error: {e}")            
        
        # Inserción a la base de datos
        try:
            with transaction.atomic():                      
                Infra.objects.bulk_create(data)
            messages.success(self.request, "Archivo cargado correctamente en la base de datos")    
        except IntegrityError as e:
             mensaje = str(e.__cause__)
             index_msg = str(e.__cause__).find(":")
             return msg_error(self.request, self, form, f"Registro duplicado: {mensaje[index_msg+2:].strip()}")      
       
        return super().form_valid(form)
    
# Vista para cargar el CSV de servicios    
class cargaCsvServicios(FormView):
    template_name = "infra/carga_servicios.html"
    form_class = InfraUploadForm
    success_url = reverse_lazy("infra_app:carga_servicios")
    
    def form_valid(self, form):
        file = form.cleaned_data["file"]
        csv_file = StringIO(file.read().decode("utf-8"))
        reader = csv.reader(csv_file, delimiter=";")
        # Saltar la cabecera
        next(reader)
        
        data = []

        for row in reader:
            try:
                id_servicio_csv = parse_int(row[0], "id_servicio")
                servicio_instance = Servicios(
                    id_servicio=id_servicio_csv,
                    nombre_servicio=row[1].strip(),
                )
                data.append(servicio_instance)           
                                                   
            except IndexError:
                return msg_error(self.request, self, form, "El número de columnas del archivo csv no es válido")
            except Exception as e:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: {e}")
            
        try:                  
            Servicios.objects.bulk_create(data)
            messages.success(self.request, "Archivo cargado correctamente en la base de datos")
        except IntegrityError as e:
             mensaje = str(e.__cause__)
             index_msg = str(e.__cause__).find(":")
             return msg_error(self.request, self, form, f"Llave duplicada: {mensaje[index_msg+2:].strip()}")     
 
        return super().form_valid(form)

# Vista para cargar el CSV de unidades 
class cargaCsvUnidades(FormView):
    template_name = "infra/carga_unidades.html"
    form_class = UnidadesUploadForm
    success_url = reverse_lazy("infra_app:carga_unidades")
    
    def form_valid(self, form):

        file = form.cleaned_data["file"]
        csv_file = StringIO(file.read().decode("utf-8"))
        reader = csv.reader(csv_file, delimiter=";")
        # Saltar la cabecera
        next(reader)
        
        data = []

        for row in reader:
            try:
                id_unidad_csv = parse_int(row[0], "id_unidad")
                id_servicio_csv = parse_int(row[2], "id_servicio")
                # Genero instancia de unidad
                unidad_instance = Unidades(
                    id_unidad=id_unidad_csv,
                    nombre_unidad=row[1].strip(),
                    id_servicio=Servicios.objects.get(id_servicio=id_servicio_csv)
                )
                data.append(unidad_instance)           
                                                   
            except Servicios.DoesNotExist:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: El id_servicio ingresado no existe")
            except IndexError:
                return msg_error(self.request, self, form, "El número de columnas del archivo csv no es válido")
            except Exception as e:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: {e}")

        try:                  
            Unidades.objects.bulk_create(data)
            messages.success(self.request, "Archivo cargado correctamente en la base de datos")
        except IntegrityError as e:
             mensaje = str(e.__cause__)
             index_msg = str(e.__cause__).find(":")
             return msg_error(self.request, self, form, f"Llave duplicada: {mensaje[index_msg+2:].strip()}")     
 
        return super().form_valid(form)

class cargaCsvActividad(FormView):
    template_name = "infra/carga_actividad.html"
    form_class = UnidadesUploadForm
    success_url = reverse_lazy("infra_app:carga_actividad")
    
    def form_valid(self, form):

        file = form.cleaned_data["file"]
        csv_file = StringIO(file.read().decode("utf-8"))
        reader = csv.reader(csv_file, delimiter=";")
        # Saltar la cabecera
        next(reader)
        
        data = []

        for row in reader:
            try:
                id_filial_csv = parse_int(row[0], "id_filial")
                ejercicio_csv = parse_int(row[1], "ejercicio")
                mes_csv = parse_int(row[2], "mes")
                validar_mes(mes_csv)
                id_unidad_csv = parse_int(row[3], "id_unidad")
                cantidad_csv = parse_int(row[4], "actividad")
                
                actividad_instance = Actividad(
                    id_filial=Filiales.objects.get(id_filial=id_filial_csv),
                    ejercicio=ejercicio_csv,
                    mes=mes_csv,
                    id_unidad=Unidades.objects.get(id_unidad=id_unidad_csv),
                    cantidad=cantidad_csv
                )
                data.append(actividad_instance)           
                                                   
            except Filiales.DoesNotExist:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: El id_filial ingresado no existe")
            except Unidades.DoesNotExist:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: El id_unidad ingresado no existe")
            except IndexError:
                return msg_error(self.request, self, form, "El número de columnas del archivo csv no es válido")
            except Exception as e:
                return msg_error(self.request, self, form, f"Error en la fila {reader.line_num}: {e}")

        try:                  
            Actividad.objects.bulk_create(data)
            messages.success(self.request, "Archivo cargado correctamente en la base de datos")
        except IntegrityError as e:
             mensaje = str(e.__cause__)
             index_msg = str(e.__cause__).find(":")
             return msg_error(self.request, self, form, f"Registro duplicado: {mensaje[index_msg+2:].strip()}")     
 
        return super().form_valid(form)   

class DeleteInfraView(View):
    form_class = DeleteInfraForm
    template_name = 'infra/delete_infra.html'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            filial = form.cleaned_data['filial']
            ejercicio = form.cleaned_data['ejercicio']
            mes = form.cleaned_data['mes']
            
            # Eliminar datos de Infra que coincidan con los criterios
            
        infra_records = Infra.objects.filter(id_filial=filial, ejercicio=ejercicio, mes=mes)
        if infra_records:
            infra_records.delete()
            message = "Los registros se han eliminado correctamente."
        else:
            message = "Los registros que intentas eliminar no existen"
            
        return render(request, self.template_name, {'form': form, 'message': message})

class DeleteActividadView(View):
    form_class = DeleteActividadForm
    template_name = 'infra/delete_actividad.html'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            filial = form.cleaned_data['filial']
            ejercicio = form.cleaned_data['ejercicio']
            mes = form.cleaned_data['mes']
            
            # Eliminar datos de Infra que coincidan con los criterios
            
        actividad_records = Actividad.objects.filter(id_filial=filial, ejercicio=ejercicio, mes=mes)
        if actividad_records:
            actividad_records.delete()
            message = "Los registros se han eliminado correctamente."
        else:
            message = "Los registros que intentas eliminar no existen"
            
        return render(request, self.template_name, {'form': form, 'message': message})
    
class PromediosDiariosView(ListView):
    template_name = 'infra/sum_promedios_diarios.html'
    context_object_name = 'sum_promedio_diario'

    def get_queryset(self):
        sum_promedios_diarios = Infra.objects.sum_promedios_diarios()
        return sum_promedios_diarios

class ProductividadView(ListView):
    template_name = 'infra/productividad.html'
    context_object_name = 'productividad'

    def get_queryset(self):
        productividad = Infra.objects.calcular_productividad()
        return productividad

class ReporteActivos(ListView):
    template_name = 'infra/reporte_activos.html'
    context_object_name = 'reporte_activos'

    def get_queryset(self):
        activos = Infra.objects.promedio_simple_activos_por_mes()
        return activos
    
class ReporteProductividad(ListView):
    template_name = 'infra/reporte_productividad.html'
    context_object_name = 'reporte_productividad'

    def get_queryset(self):
        productividad = Infra.objects.productividad()
        return productividad     

    






