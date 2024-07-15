from django import forms
from .models import Servicios, Filiales

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
  