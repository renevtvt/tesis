from django import forms
from .models import Servicios, Filiales, Unidades, Infra

class InfraUploadForm(forms.Form):
    file = forms.FileField()

class ServiciosUploadForm(forms.Form):
    file = forms.FileField()

class UnidadesUploadForm(forms.Form):
    file = forms.FileField()

class DeleteInfraForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    mes = forms.IntegerField(label='Mes')

class DeleteActividadForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    mes = forms.IntegerField(label='Mes')

class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = ['id_servicio', 'nombre_servicio']

class InfraFilterForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    mes = forms.IntegerField(label='Mes')
    dia = forms.IntegerField(label='Dia')

class InfraFilterListForm(forms.Form):
    filial = forms.ModelChoiceField(queryset=Filiales.objects.all(), label='Filial')
    ejercicio = forms.IntegerField(label='Ejercicio')
    mes = forms.IntegerField(label='Mes')
    dia = forms.IntegerField(label='Dia')
    unidad = forms.ModelChoiceField(queryset=Unidades.objects.all(), label='Unidad')

class InfraUpdateForm(forms.ModelForm):
    class Meta:
        model = Infra
        fields = ['disponible', 'habilitado', 'instalado']

  