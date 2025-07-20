from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import SocioComercial
from .forms import SocioComercialForm
from django.db.models import Q, Sum, Count
from django.utils import timezone
from clientes.models import Cliente
import os
import mimetypes

class SocioComercialListView(LoginRequiredMixin, ListView):
    model = SocioComercial
    template_name = 'socios/lista.html'
    context_object_name = 'socios'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = SocioComercial.objects.annotate(
            total_ventas=Sum('clientes__valor_compra'),
            cantidad_ventas=Count('clientes')
        ).order_by('-fecha_creacion')
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(ciudad_sede__icontains=query)
            )
        
        activo = self.request.GET.get('activo')
        if activo == 'true':
            queryset = queryset.filter(activo=True)
        elif activo == 'false':
            queryset = queryset.filter(activo=False)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['activo'] = self.request.GET.get('activo', '')
        
        # Estadísticas de socios comerciales
        now = timezone.now()
        current_month = now.month
        current_year = now.year
        
        # Total de socios registrados
        total_socios_registrados = SocioComercial.objects.count()
        
        # Socios activos (que han realizado al menos una venta)
        socios_con_ventas = SocioComercial.objects.filter(
            clientes__isnull=False
        ).distinct().count()
        
        # Socios que han realizado ventas en el mes actual
        socios_ventas_mes_actual = SocioComercial.objects.filter(
            clientes__fecha_compra__year=current_year,
            clientes__fecha_compra__month=current_month
        ).distinct().count()
        
        # Valor total de ventas de todos los socios (históricamente)
        ventas_totales_socios = Cliente.objects.aggregate(
            total=Sum('valor_compra')
        )['total'] or 0
        
        context['total_socios_registrados'] = total_socios_registrados
        context['socios_con_ventas'] = socios_con_ventas
        context['socios_ventas_mes_actual'] = socios_ventas_mes_actual
        context['ventas_totales_socios'] = ventas_totales_socios
        context['nombre_mes_actual'] = now.strftime('%B %Y')
        
        return context

class SocioComercialCreateView(LoginRequiredMixin, CreateView):
    model = SocioComercial
    form_class = SocioComercialForm
    template_name = 'socios/crear.html'
    success_url = reverse_lazy('socios:lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Socio comercial creado exitosamente.')
        return super().form_valid(form)

class SocioComercialDetailView(LoginRequiredMixin, DetailView):
    model = SocioComercial
    template_name = 'socios/detalle.html'
    context_object_name = 'socio'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        socio = self.get_object()
        context['clientes'] = Cliente.objects.filter(socio_comercial=socio).order_by('-fecha_compra')[:10]
        context['total_ventas'] = socio.total_ventas()
        context['cantidad_ventas'] = socio.cantidad_ventas()
        return context

class SocioComercialUpdateView(LoginRequiredMixin, UpdateView):
    model = SocioComercial
    form_class = SocioComercialForm
    template_name = 'socios/editar.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Socio comercial actualizado exitosamente.')
        return super().form_valid(form)

class SocioComercialDeleteView(LoginRequiredMixin, DeleteView):
    model = SocioComercial
    template_name = 'socios/eliminar.html'
    success_url = reverse_lazy('socios:lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Socio comercial eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

@login_required
def ver_contrato(request, pk):
    """Vista para servir archivos de contrato de socios comerciales"""
    socio = get_object_or_404(SocioComercial, pk=pk)
    
    # Verificar si el socio tiene contrato
    if not socio.documento_contrato or not socio.documento_contrato.name:
        raise Http404("El socio no tiene contrato adjunto.")
    
    # Obtener la ruta del archivo
    file_path = socio.documento_contrato.path
    
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        raise Http404("El archivo de contrato no se encontró.")
    
    # Determinar el tipo de contenido
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = 'application/octet-stream'
    
    # Leer y servir el archivo
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        
        # Siempre mostrar inline (no permitir descarga)
        if content_type == 'application/pdf':
            response['Content-Disposition'] = 'inline'
        else:
            response['Content-Disposition'] = 'inline'
        
        # Prevenir descarga con headers adicionales
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response
