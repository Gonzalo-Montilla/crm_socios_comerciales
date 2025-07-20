from django.db import models
from django.urls import reverse
from socios.models import SocioComercial
from django.core.validators import MinValueValidator
from decimal import Decimal

class Cliente(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    cedula = models.CharField(max_length=20, unique=True, verbose_name="Cédula")
    fecha_compra = models.DateField(verbose_name="Fecha de Compra")
    valor_compra = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor de la Compra"
    )
    socio_comercial = models.ForeignKey(
        SocioComercial, 
        on_delete=models.CASCADE, 
        verbose_name="Socio Comercial",
        related_name='clientes'
    )
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad", blank=True)
    observaciones = models.TextField(verbose_name="Observaciones", blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_compra']
    
    def __str__(self):
        return f"{self.nombre} - {self.cedula}"
    
    def get_absolute_url(self):
        return reverse('clientes:detalle', kwargs={'pk': self.pk})

class CupoCredito(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    valor_aprobado = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Valor Aprobado"
    )
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    fecha_aprobacion = models.DateField(verbose_name="Fecha de Aprobación")
    observaciones = models.TextField(verbose_name="Observaciones", blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cupo de Crédito"
        verbose_name_plural = "Cupos de Crédito"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.ciudad} - ${self.valor_aprobado}"
