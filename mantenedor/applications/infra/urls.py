from django.urls import path
from . import views

app_name = "infra_app"

urlpatterns = [
    path(
        '', 
        views.InicioView.as_view(), 
        name="inicio"
    ),
    path(
        'carga-infra/', 
        views.cargaCsvInfra.as_view(), 
        name="carga_infra"
    ),
    path(
        'carga-servicios/', 
        views.cargaCsvServicios.as_view(), 
        name="carga_servicios"
    ),
    path(
        'carga-unidades/', 
        views.cargaCsvUnidades.as_view(), 
        name="carga_unidades"
    ),
    path(
        'carga-actividad/', 
        views.cargaCsvActividad.as_view(), 
        name="carga_actividad"
    ),
    path(
        'delete-infra/', 
        views.DeleteInfraView.as_view(), 
        name="delete_infra"
    ),
      path(
        'delete-actividad/', 
        views.DeleteActividadView.as_view(), 
        name="delete_actividad"
    ),


    path(
        'servicios/', 
        views.ServiciosListView.as_view(), 
        name="lista_servicios"
    ),
   
]