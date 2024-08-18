from django.contrib import admin
from .models import Infra, Filiales, Servicios, Unidades, Actividad, Users

# Register your models here.

admin.site.register(Users)
admin.site.register(Infra)
admin.site.register(Filiales)
admin.site.register(Servicios)
admin.site.register(Unidades)
admin.site.register(Actividad)
