from django.contrib import admin
from .models import SocioComercial

@admin.register(SocioComercial)
class SocioComercialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad_sede', 'fecha_ingreso', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'ciudad_sede', 'fecha_ingreso']
    search_fields = ['nombre', 'ciudad_sede']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
