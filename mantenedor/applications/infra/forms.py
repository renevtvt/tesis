from django import forms
from .models import Servicios

class InfraUploadForm(forms.Form):
    file = forms.FileField()

class ServiciosUploadForm(forms.Form):
    file = forms.FileField()

class UnidadesUploadForm(forms.Form):
    file = forms.FileField()

class ServiciosForm(forms.ModelForm):
    class Meta:
        model = Servicios
        fields = ['id_servicio', 'nombre_servicio']  
  