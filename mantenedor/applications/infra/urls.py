from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "infra_app"

urlpatterns = [
    path(
        '', 
        login_required(views.InicioView.as_view()), 
        name="home"
    ),
    path(
        'carga-infra/', 
        login_required(views.cargaCsvInfra.as_view()), 
        name="carga_infra"
    ),
    path(
        'carga-servicios/', 
        login_required(views.cargaCsvServicios.as_view()), 
        name="carga_servicios"
    ),
    path(
        'carga-unidades/', 
        login_required(views.cargaCsvUnidades.as_view()), 
        name="carga_unidades"
    ),
    path(
        'carga-actividad/', 
        login_required(views.cargaCsvActividad.as_view()), 
        name="carga_actividad"
    ),
    path(
        'delete-infra/', 
        login_required(views.DeleteInfraView.as_view()), 
        name="delete_infra"
    ),
      path(
        'delete-actividad/', 
        login_required(views.DeleteActividadView.as_view()), 
        name="delete_actividad"
    ),
      path(
        'actividad-lista/', 
        login_required(views.ActividadListView.as_view()), 
        name="actividad_lista"
    ),
      path(
        'actividad-lista-update/', 
        login_required(views.ActividadListViewUpdate.as_view()), 
        name="actividad_lista_update"
    ),
    path(
        'actividad-lista-update/update<int:pk>', 
        login_required(views.ActividadUpdateView.as_view()), 
        name="actividad_update"
    ),
    path(
        'infra-lista/', 
        login_required(views.InfraListView.as_view()), 
        name="infra_lista"
    ),
    path(
        'infra-list-update/', 
        login_required(views.InfraListViewUpdate.as_view()), 
        name="infra_list_update"
    )
    ,
    path(
        'infra-list-update/update/<int:pk>/', 
        login_required(views.InfraUpdateView.as_view()), 
        name="infra_update"
    ),
    path(
        'reporte-activos/', 
        login_required(views.ReporteActivos.as_view()), 
        name="reporte_activos"
    ),
    path(
        'reporte-productividad/', 
        login_required(views.ReporteProductividad.as_view()), 
        name="reporte_productividad"
    )
   
]