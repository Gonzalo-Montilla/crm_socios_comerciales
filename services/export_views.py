from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
import csv
from datetime import datetime
from clientes.models import Cliente
from socios.models import SocioComercial
from seguimiento.models import SeguimientoSocio


@method_decorator(login_required, name='dispatch')
class ExportClientesCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="clientes_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        # Encabezados
        writer.writerow([
            'ID',
            'Nombre',
            'Cédula', 
            'Fecha de Compra',
            'Valor de Compra',
            'Socio Comercial',
            'Teléfono',
            'Email',
            'Ciudad',
            'Observaciones',
            'Fecha de Creación',
            'Fecha de Actualización'
        ])
        
        # Datos
        clientes = Cliente.objects.select_related('socio_comercial').all()
        for cliente in clientes:
            writer.writerow([
                cliente.id,
                cliente.nombre,
                cliente.cedula,
                cliente.fecha_compra.strftime('%Y-%m-%d') if cliente.fecha_compra else '',
                cliente.valor_compra,
                cliente.socio_comercial.nombre if cliente.socio_comercial else '',
                cliente.telefono,
                cliente.email,
                cliente.ciudad,
                cliente.observaciones,
                cliente.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if cliente.fecha_creacion else '',
                cliente.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if cliente.fecha_actualizacion else ''
            ])
        
        return response


@method_decorator(login_required, name='dispatch')
class ExportSociosCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="socios_comerciales_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        # Encabezados
        writer.writerow([
            'ID',
            'Nombre',
            'Fecha de Ingreso',
            'Ciudad Sede',
            'Asesor Asignado',
            'Activo',
            'Teléfono',
            'Email',
            'Total Ventas',
            'Cantidad Ventas',
            'Fecha de Creación',
            'Fecha de Actualización'
        ])
        
        # Datos
        socios = SocioComercial.objects.all()
        for socio in socios:
            writer.writerow([
                socio.id,
                socio.nombre,
                socio.fecha_ingreso.strftime('%Y-%m-%d') if socio.fecha_ingreso else '',
                socio.ciudad_sede,
                socio.asesor_asignado,
                'Sí' if socio.activo else 'No',
                socio.telefono,
                socio.email,
                socio.total_ventas(),
                socio.cantidad_ventas(),
                socio.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if socio.fecha_creacion else '',
                socio.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if socio.fecha_actualizacion else ''
            ])
        
        return response


@method_decorator(login_required, name='dispatch')
class ExportSeguimientosCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="seguimientos_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        # Encabezados
        writer.writerow([
            'ID',
            'Socio Potencial',
            'Socio Comercial Asociado',
            'Asesor Asignado',
            'Estado',
            'Porcentaje Completado (%)',
            'Teléfono',
            'Email',
            'Ciudad',
            'Presentación Negocio',
            'Fecha Presentación',
            'Documentos Enviados',
            'Fecha Envío Documentos',
            'Contrato Enviado',
            'Fecha Envío Contrato',
            'Contrato Firmado',
            'Fecha Firma Contrato',
            'Capacitación Realizada',
            'Fecha Capacitación',
            'Usuario Creado',
            'Fecha Creación Usuario',
            'Proceso Completo',
            'Observaciones',
            'Fecha de Creación',
            'Fecha de Actualización'
        ])
        
        # Datos
        seguimientos = SeguimientoSocio.objects.select_related('socio_comercial').all()
        for seg in seguimientos:
            writer.writerow([
                seg.id,
                seg.socio_potencial,
                seg.socio_comercial.nombre if seg.socio_comercial else '',
                seg.asesor_asignado,
                dict(seg.ESTADO_CHOICES).get(seg.estado, seg.estado),
                round(seg.porcentaje_completado(), 1),
                seg.telefono,
                seg.email,
                seg.ciudad,
                'Sí' if seg.presentacion_negocio else 'No',
                seg.fecha_presentacion.strftime('%Y-%m-%d') if seg.fecha_presentacion else '',
                'Sí' if seg.documentos_enviados else 'No',
                seg.fecha_envio_documentos.strftime('%Y-%m-%d') if seg.fecha_envio_documentos else '',
                'Sí' if seg.contrato_enviado else 'No',
                seg.fecha_envio_contrato.strftime('%Y-%m-%d') if seg.fecha_envio_contrato else '',
                'Sí' if seg.contrato_firmado else 'No',
                seg.fecha_firma_contrato.strftime('%Y-%m-%d') if seg.fecha_firma_contrato else '',
                'Sí' if seg.capacitacion_realizada else 'No',
                seg.fecha_capacitacion.strftime('%Y-%m-%d') if seg.fecha_capacitacion else '',
                'Sí' if seg.usuario_creado else 'No',
                seg.fecha_creacion_usuario.strftime('%Y-%m-%d') if seg.fecha_creacion_usuario else '',
                'Sí' if seg.proceso_completo else 'No',
                seg.observaciones,
                seg.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if seg.fecha_creacion else '',
                seg.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if seg.fecha_actualizacion else ''
            ])
        
        return response
