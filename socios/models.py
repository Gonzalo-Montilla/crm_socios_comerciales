from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse

class SocioComercial(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Socio")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso al Convenio")
    ciudad_sede = models.CharField(max_length=100, verbose_name="Ciudad de la Sede")
    documento_contrato = models.FileField(
        upload_to='contratos/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        verbose_name="Documento del Contrato",
        blank=True,
        null=True
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Socio Comercial"
        verbose_name_plural = "Socios Comerciales"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('socios:detalle', kwargs={'pk': self.pk})
    
    def total_ventas(self):
        """Calcula el total de ventas del socio"""
        from clientes.models import Cliente
        ventas = Cliente.objects.filter(socio_comercial=self)
        return sum([venta.valor_compra for venta in ventas])
    
    def cantidad_ventas(self):
        """Cuenta la cantidad de ventas del socio"""
        from clientes.models import Cliente
        return Cliente.objects.filter(socio_comercial=self).count()
