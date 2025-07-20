from django.contrib import admin
from .models import SeguimientoSocio

@admin.register(SeguimientoSocio)
class SeguimientoSocioAdmin(admin.ModelAdmin):
    list_display = ['socio_potencial', 'estado', 'proceso_completo', 'porcentaje_completado_display', 'fecha_actualizacion']
    list_filter = ['estado', 'proceso_completo', 'presentacion_negocio', 'contrato_firmado']
    search_fields = ['socio_potencial', 'ciudad']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'proceso_completo']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('socio_potencial', 'socio_comercial', 'estado')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'ciudad')
        }),
        ('Seguimiento del Proceso', {
            'fields': (
                ('presentacion_negocio', 'fecha_presentacion'),
                ('documentos_enviados', 'fecha_envio_documentos'),
                ('contrato_enviado', 'fecha_envio_contrato'),
                ('contrato_firmado', 'fecha_firma_contrato'),
                ('capacitacion_realizada', 'fecha_capacitacion'),
                ('usuario_creado', 'fecha_creacion_usuario'),
            )
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Estado', {
            'fields': ('proceso_completo',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )
    
    def porcentaje_completado_display(self, obj):
        return f"{obj.porcentaje_completado():.1f}%"
    porcentaje_completado_display.short_description = 'Progreso'
