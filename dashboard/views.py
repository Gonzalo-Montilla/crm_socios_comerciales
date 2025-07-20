from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from clientes.models import Cliente, CupoCredito
from socios.models import SocioComercial
from seguimiento.models import SeguimientoSocio
from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def home(request):
    # Obtener estadísticas del dashboard
    total_socios = SocioComercial.objects.count()
    socios_activos = SocioComercial.objects.filter(activo=True).count()
    total_clientes = Cliente.objects.count()
    
    # Ventas del último mes
    ultimo_mes = timezone.now() - timedelta(days=30)
    ventas_ultimo_mes = Cliente.objects.filter(
        fecha_compra__gte=ultimo_mes
    ).aggregate(total=Sum('valor_compra'))['total'] or 0
    
    # Ventas totales
    ventas_totales = Cliente.objects.aggregate(total=Sum('valor_compra'))['total'] or 0
    
    # Seguimientos pendientes
    seguimientos_pendientes = SeguimientoSocio.objects.filter(
        proceso_completo=False
    ).count()
    
    # Cupos de crédito
    total_cupos = CupoCredito.objects.count()
    valor_cupos = CupoCredito.objects.aggregate(total=Sum('valor_aprobado'))['total'] or 0
    
    # Últimas ventas
    ultimas_ventas = Cliente.objects.select_related('socio_comercial').order_by('-fecha_compra')[:5]
    
    # Mejores socios por ventas
    mejores_socios = SocioComercial.objects.annotate(
        total_ventas=Sum('clientes__valor_compra'),
        cantidad_ventas=Count('clientes')
    ).filter(total_ventas__isnull=False).order_by('-total_ventas')[:5]
    
    context = {
        'total_socios': total_socios,
        'socios_activos': socios_activos,
        'total_clientes': total_clientes,
        'ventas_ultimo_mes': ventas_ultimo_mes,
        'ventas_totales': ventas_totales,
        'seguimientos_pendientes': seguimientos_pendientes,
        'total_cupos': total_cupos,
        'valor_cupos': valor_cupos,
        'ultimas_ventas': ultimas_ventas,
        'mejores_socios': mejores_socios,
        'usuario': request.user,
    }
    
    return render(request, 'dashboard/home.html', context)
