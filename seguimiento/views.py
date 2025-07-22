from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SeguimientoSocio
from .forms import SeguimientoSocioForm
from django.db.models import Q, Count, Avg
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
import csv

class SeguimientoSocioListView(LoginRequiredMixin, ListView):
    model = SeguimientoSocio
    template_name = 'seguimiento/lista.html'
    context_object_name = 'seguimientos'
    paginate_by = 20
    
    def export_seguimientos_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="seguimientos.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Socio Potencial', 'Estado', 'Fecha de Creación', 'Fecha de Actualización', 'Asesor Asignado'])
        seguimientos = SeguimientoSocio.objects.all().values_list('id', 'socio_potencial', 'estado', 'fecha_creacion', 'fecha_actualizacion', 'asesor_asignado')
        for seguimiento in seguimientos:
            writer.writerow(seguimiento)
        return response
    
    def get_queryset(self):
        queryset = SeguimientoSocio.objects.select_related('socio_comercial').order_by('-fecha_actualizacion')
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(socio_potencial__icontains=query) | 
                Q(ciudad__icontains=query)
            )
        
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
            
        proceso = self.request.GET.get('proceso')
        if proceso == 'completo':
            queryset = queryset.filter(proceso_completo=True)
        elif proceso == 'pendiente':
            queryset = queryset.filter(proceso_completo=False)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['estado'] = self.request.GET.get('estado', '')
        context['proceso'] = self.request.GET.get('proceso', '')
        context['estados'] = SeguimientoSocio.ESTADO_CHOICES
        
        # Calcular estadísticas
        context.update(self.get_estadisticas())
        
        return context
    
    def get_estadisticas(self):
        """Calcula las estadísticas para el dashboard"""
        # Obtener todos los seguimientos (sin filtros aplicados)
        todos_seguimientos = SeguimientoSocio.objects.all()
        total = todos_seguimientos.count()
        
        if total == 0:
            return {
                'estadisticas': {
                    'total': 0,
                    'por_estado': {},
                    'por_etapa': {},
                    'tendencias': {},
                    'metricas_tiempo': {}
                }
            }
        
        # 1. Contadores por estado
        estados = todos_seguimientos.values('estado').annotate(count=Count('id'))
        por_estado = {}
        for estado in estados:
            estado_nombre = dict(SeguimientoSocio.ESTADO_CHOICES).get(estado['estado'], estado['estado'])
            por_estado[estado['estado']] = {
                'nombre': estado_nombre,
                'count': estado['count'],
                'porcentaje': round((estado['count'] / total) * 100, 1)
            }
        
        # 2. Progreso por etapa
        por_etapa = {
            'presentacion_negocio': {
                'nombre': 'Presentación de Negocio',
                'count': todos_seguimientos.filter(presentacion_negocio=True).count(),
                'icono': '📋'
            },
            'documentos_enviados': {
                'nombre': 'Documentos Enviados',
                'count': todos_seguimientos.filter(documentos_enviados=True).count(),
                'icono': '📄'
            },
            'contrato_enviado': {
                'nombre': 'Contrato Enviado',
                'count': todos_seguimientos.filter(contrato_enviado=True).count(),
                'icono': '📝'
            },
            'contrato_firmado': {
                'nombre': 'Contrato Firmado',
                'count': todos_seguimientos.filter(contrato_firmado=True).count(),
                'icono': '✅'
            },
            'capacitacion_realizada': {
                'nombre': 'Capacitación Realizada',
                'count': todos_seguimientos.filter(capacitacion_realizada=True).count(),
                'icono': '🎓'
            },
            'usuario_creado': {
                'nombre': 'Usuario Creado',
                'count': todos_seguimientos.filter(usuario_creado=True).count(),
                'icono': '👤'
            }
        }
        
        # Agregar porcentajes a cada etapa
        for etapa in por_etapa.values():
            etapa['porcentaje'] = round((etapa['count'] / total) * 100, 1)
        
        # 3. Tendencias recientes
        ahora = timezone.now()
        hace_una_semana = ahora - timedelta(days=7)
        hace_un_mes = ahora - timedelta(days=30)
        
        tendencias = {
            'esta_semana': {
                'nuevos': todos_seguimientos.filter(fecha_creacion__gte=hace_una_semana).count(),
                'completados': todos_seguimientos.filter(
                    proceso_completo=True,
                    fecha_actualizacion__gte=hace_una_semana
                ).count(),
                'contratos_firmados': todos_seguimientos.filter(
                    contrato_firmado=True,
                    fecha_firma_contrato__gte=hace_una_semana.date()
                ).count()
            },
            'este_mes': {
                'nuevos': todos_seguimientos.filter(fecha_creacion__gte=hace_un_mes).count(),
                'completados': todos_seguimientos.filter(
                    proceso_completo=True,
                    fecha_actualizacion__gte=hace_un_mes
                ).count(),
                'tasa_conversion': 0  # Calcularemos después
            }
        }
        
        # Calcular tasa de conversión del mes
        nuevos_mes = tendencias['este_mes']['nuevos']
        if nuevos_mes > 0:
            tendencias['este_mes']['tasa_conversion'] = round(
                (tendencias['este_mes']['completados'] / nuevos_mes) * 100, 1
            )
        
        # 4. Métricas de tiempo
        completados = todos_seguimientos.filter(proceso_completo=True)
        metricas_tiempo = {
            'promedio_dias': 0,
            'vencidos': 0,
            'proximos_vencer': 0
        }
        
        if completados.exists():
            # Calcular promedio de días para completar
            dias_totales = 0
            count_con_fechas = 0
            for seguimiento in completados:
                if seguimiento.fecha_presentacion and seguimiento.fecha_creacion_usuario:
                    dias = (seguimiento.fecha_creacion_usuario - seguimiento.fecha_presentacion).days
                    dias_totales += dias
                    count_con_fechas += 1
            
            if count_con_fechas > 0:
                metricas_tiempo['promedio_dias'] = round(dias_totales / count_con_fechas, 1)
        
        # Seguimientos "vencidos" (en proceso por más de 45 días)
        hace_45_dias = ahora - timedelta(days=45)
        metricas_tiempo['vencidos'] = todos_seguimientos.filter(
            estado='en_proceso',
            fecha_creacion__lt=hace_45_dias
        ).count()
        
        # Próximos a vencer (en proceso por más de 30 días)
        hace_30_dias = ahora - timedelta(days=30)
        metricas_tiempo['proximos_vencer'] = todos_seguimientos.filter(
            estado='en_proceso',
            fecha_creacion__lt=hace_30_dias,
            fecha_creacion__gte=hace_45_dias
        ).count()
        
        return {
            'estadisticas': {
                'total': total,
                'por_estado': por_estado,
                'por_etapa': por_etapa,
                'tendencias': tendencias,
                'metricas_tiempo': metricas_tiempo
            }
        }

class SeguimientoSocioCreateView(LoginRequiredMixin, CreateView):
    model = SeguimientoSocio
    form_class = SeguimientoSocioForm
    template_name = 'seguimiento/crear.html'
    success_url = reverse_lazy('seguimiento:lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Seguimiento creado exitosamente.')
        return super().form_valid(form)

class SeguimientoSocioDetailView(LoginRequiredMixin, DetailView):
    model = SeguimientoSocio
    template_name = 'seguimiento/detalle.html'
    context_object_name = 'seguimiento'

class SeguimientoSocioUpdateView(LoginRequiredMixin, UpdateView):
    model = SeguimientoSocio
    form_class = SeguimientoSocioForm
    template_name = 'seguimiento/editar.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Seguimiento actualizado exitosamente.')
        return super().form_valid(form)

class SeguimientoSocioDeleteView(LoginRequiredMixin, DeleteView):
    model = SeguimientoSocio
    template_name = 'seguimiento/eliminar.html'
    success_url = reverse_lazy('seguimiento:lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Seguimiento eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
