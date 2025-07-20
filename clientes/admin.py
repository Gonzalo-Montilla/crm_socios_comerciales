from django.contrib import admin
from .models import Cliente, CupoCredito

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cedula', 'socio_comercial', 'fecha_compra', 'valor_compra']
    list_filter = ['fecha_compra', 'socio_comercial', 'ciudad']
    search_fields = ['nombre', 'cedula', 'socio_comercial__nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

@admin.register(CupoCredito)
class CupoCreditoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'valor_aprobado', 'fecha_aprobacion']
    list_filter = ['ciudad', 'fecha_aprobacion']
    search_fields = ['nombre', 'ciudad']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
