from django import forms
from .models import Servicios, Filiales, Unidades, Infra, Actividad

# FORMULARIO PARA CARGAR INFRAESTRUCTURA
class InfraUploadForm(forms.Form):
    file = forms.FileField()

# FORMULARIO PARA CARGAR SERVICIOS
class ServiciosUploadForm(forms.Form):
    file = forms.FileField()

# FORMULARIO PARA CARGAR UNIDADES
class UnidadesUploadForm(forms.Form):
    file = forms.FileField()

# FORMULARIO PARA BORRAR INFRAESTRUCTURA
class DeleteInfraForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    mes = forms.IntegerField(label='Mes')

# FORMULARIO PARA BORRAR ACTIVIDAD
class DeleteActividadForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    mes = forms.IntegerField(label='Mes')

class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = ['id_servicio', 'nombre_servicio']

# FORMULARIO PARA FILTRAR INFRAESTRUCTURA EN VISTA QUE LISTA INFRA
class InfraFilterForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    mes = forms.IntegerField(label='Mes')
    dia = forms.IntegerField(label='Dia')

# FORMULARIO PARA FILTRAR INFRAESTRUCTURA EN VISTA PERMITE VISUALIZAR DATOS PARA ACTUALIZAR
class InfraFilterUpdateForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    mes = forms.IntegerField(label='Mes')
    dia = forms.IntegerField(label='Dia')
    unidad = forms.ModelChoiceField(queryset=Unidades.objects.all(), label='Unidad')

# FORMULARIO PARA CARGAR DATOS INFRA DE REGISTRO A ACTUALIZAR
class InfraUpdateForm(forms.ModelForm):
    class Meta:
        model = Infra
        fields = ['disponible', 'habilitado', 'instalado']

# FORMULARIO PARA CARGAR DATOS ACTIVIDAD EN VISTA QUE LISTA ACTIVIDAD PARA ACTUALIZAR
class ActividadFilterUpdateForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    unidad = forms.ModelChoiceField(queryset=Unidades.objects.all(), label='Unidad')

# FORMULARIO QUE CARGA ACTIVIDAD EN REGISTRO A ACTUALIZAR
class ActividadUpdateForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['cantidad']
   


  