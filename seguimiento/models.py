from django.db import models
from django.urls import reverse
from socios.models import SocioComercial

class SeguimientoSocio(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    socio_potencial = models.CharField(
        max_length=200, 
        verbose_name="Nombre del Socio Potencial"
    )
    socio_comercial = models.ForeignKey(
        SocioComercial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Socio Comercial (Si ya se creó)",
        help_text="Se asociará automáticamente cuando el socio potencial se convierta en socio comercial"
    )
    
    # Pasos del proceso
    presentacion_negocio = models.BooleanField(
        default=False, 
        verbose_name="Presentación de Negocio Realizada"
    )
    fecha_presentacion = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Presentación"
    )
    
    documentos_enviados = models.BooleanField(
        default=False, 
        verbose_name="Documentos Enviados"
    )
    fecha_envio_documentos = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Envío de Documentos"
    )
    
    contrato_enviado = models.BooleanField(
        default=False, 
        verbose_name="Contrato Enviado"
    )
    fecha_envio_contrato = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Envío de Contrato"
    )
    
    contrato_firmado = models.BooleanField(
        default=False, 
        verbose_name="Contrato Firmado"
    )
    fecha_firma_contrato = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Firma de Contrato"
    )
    
    capacitacion_realizada = models.BooleanField(
        default=False, 
        verbose_name="Capacitación Realizada"
    )
    fecha_capacitacion = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Capacitación"
    )
    
    usuario_creado = models.BooleanField(
        default=False, 
        verbose_name="Usuario Creado"
    )
    fecha_creacion_usuario = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Fecha de Creación de Usuario"
    )
    
    proceso_completo = models.BooleanField(
        default=False, 
        verbose_name="Proceso Completo"
    )
    
    # Información adicional
    asesor_asignado = models.CharField(
        max_length=200, 
        verbose_name="Asesor Asignado", 
        blank=True,
        help_text="Nombre del asesor que atendió este cliente"
    )
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad", blank=True)
    observaciones = models.TextField(verbose_name="Observaciones", blank=True)
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente',
        verbose_name="Estado"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Seguimiento de Socio"
        verbose_name_plural = "Seguimiento de Socios"
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"Seguimiento: {self.socio_potencial}"
    
    def get_absolute_url(self):
        return reverse('seguimiento:detalle', kwargs={'pk': self.pk})
    
    def porcentaje_completado(self):
        """Calcula el porcentaje de completado del proceso"""
        pasos = [
            self.presentacion_negocio,
            self.documentos_enviados,
            self.contrato_enviado,
            self.contrato_firmado,
            self.capacitacion_realizada,
            self.usuario_creado,
        ]
        completados = sum(pasos)
        return (completados / len(pasos)) * 100
    
    def save(self, *args, **kwargs):
        from datetime import date
        
        # Si es una actualización, obtener el objeto existente para preservar fechas
        if self.pk:
            try:
                existing = SeguimientoSocio.objects.get(pk=self.pk)
                # Preservar fechas existentes si el campo aún está marcado como True
                if self.presentacion_negocio and existing.fecha_presentacion:
                    self.fecha_presentacion = existing.fecha_presentacion
                if self.documentos_enviados and existing.fecha_envio_documentos:
                    self.fecha_envio_documentos = existing.fecha_envio_documentos
                if self.contrato_enviado and existing.fecha_envio_contrato:
                    self.fecha_envio_contrato = existing.fecha_envio_contrato
                if self.contrato_firmado and existing.fecha_firma_contrato:
                    self.fecha_firma_contrato = existing.fecha_firma_contrato
                if self.capacitacion_realizada and existing.fecha_capacitacion:
                    self.fecha_capacitacion = existing.fecha_capacitacion
                if self.usuario_creado and existing.fecha_creacion_usuario:
                    self.fecha_creacion_usuario = existing.fecha_creacion_usuario
                    
                # Limpiar fechas si el paso se desmarca
                if not self.presentacion_negocio:
                    self.fecha_presentacion = None
                if not self.documentos_enviados:
                    self.fecha_envio_documentos = None
                if not self.contrato_enviado:
                    self.fecha_envio_contrato = None
                if not self.contrato_firmado:
                    self.fecha_firma_contrato = None
                if not self.capacitacion_realizada:
                    self.fecha_capacitacion = None
                if not self.usuario_creado:
                    self.fecha_creacion_usuario = None
            except SeguimientoSocio.DoesNotExist:
                pass
        
        # Auto-asignar fechas cuando se marca como completado un paso (solo si no tiene fecha)
        if self.presentacion_negocio and not self.fecha_presentacion:
            self.fecha_presentacion = date.today()
        if self.documentos_enviados and not self.fecha_envio_documentos:
            self.fecha_envio_documentos = date.today()
        if self.contrato_enviado and not self.fecha_envio_contrato:
            self.fecha_envio_contrato = date.today()
        if self.contrato_firmado and not self.fecha_firma_contrato:
            self.fecha_firma_contrato = date.today()
        if self.capacitacion_realizada and not self.fecha_capacitacion:
            self.fecha_capacitacion = date.today()
        if self.usuario_creado and not self.fecha_creacion_usuario:
            self.fecha_creacion_usuario = date.today()
        
        # Auto-marcar proceso completo si todos los pasos están completados
        if all([
            self.presentacion_negocio,
            self.documentos_enviados,
            self.contrato_enviado,
            self.contrato_firmado,
            self.capacitacion_realizada,
            self.usuario_creado,
        ]):
            self.proceso_completo = True
            self.estado = 'completado'
        else:
            self.proceso_completo = False
            if self.estado == 'completado':
                self.estado = 'en_proceso'
        
        super().save(*args, **kwargs)
