from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cliente, CupoCredito
from .forms import ClienteForm, CupoCreditoForm
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime
from django.db import models

# Vistas para Clientes
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/lista.html'
    context_object_name = 'clientes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Cliente.objects.select_related('socio_comercial').order_by('-fecha_compra')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(cedula__icontains=query) |
                Q(socio_comercial__nombre__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        
        # Estadísticas de ventas
        now = timezone.now()
        current_month = now.month
        current_year = now.year
        
        # Total de clientes que han comprado (históricamente)
        total_clientes_compras = Cliente.objects.count()
        
        # Clientes que han comprado este mes
        clientes_mes_actual = Cliente.objects.filter(
            fecha_compra__year=current_year,
            fecha_compra__month=current_month
        ).count()
        
        # Valor total de ventas este mes
        ventas_mes_actual = Cliente.objects.filter(
            fecha_compra__year=current_year,
            fecha_compra__month=current_month
        ).aggregate(
            total=Sum('valor_compra')
        )['total'] or 0
        
        # Valor total de ventas (históricamente)
        ventas_totales = Cliente.objects.aggregate(
            total=Sum('valor_compra')
        )['total'] or 0
        
        context['total_clientes_compras'] = total_clientes_compras
        context['clientes_mes_actual'] = clientes_mes_actual
        context['ventas_mes_actual'] = ventas_mes_actual
        context['ventas_totales'] = ventas_totales
        context['nombre_mes_actual'] = now.strftime('%B %Y')
        
        return context

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear.html'
    success_url = reverse_lazy('clientes:lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado exitosamente.')
        return super().form_valid(form)

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/detalle.html'
    context_object_name = 'cliente'

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/editar.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado exitosamente.')
        return super().form_valid(form)

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/eliminar.html'
    success_url = reverse_lazy('clientes:lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cliente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# Vistas para Cupos de Crédito
class CupoCreditoListView(LoginRequiredMixin, ListView):
    model = CupoCredito
    template_name = 'clientes/cupos_credito.html'
    context_object_name = 'cupos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CupoCredito.objects.order_by('-fecha_creacion')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(ciudad__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class CupoCreditoCreateView(LoginRequiredMixin, CreateView):
    model = CupoCredito
    form_class = CupoCreditoForm
    template_name = 'clientes/crear_cupo.html'
    success_url = reverse_lazy('clientes:cupos_credito')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cupo de crédito creado exitosamente.')
        return super().form_valid(form)
