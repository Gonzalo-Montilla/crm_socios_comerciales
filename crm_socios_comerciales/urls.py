"""
URL configuration for crm_socios_comerciales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from services.export_views import ExportClientesCSV, ExportSociosCSV, ExportSeguimientosCSV

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('clientes/', include('clientes.urls')),
    path('socios/', include('socios.urls')),
    path('seguimiento/', include('seguimiento.urls')),
    # URLs para exportación
    path('exports/clientes/', ExportClientesCSV.as_view(), name='export_clientes_csv'),
    path('exports/socios/', ExportSociosCSV.as_view(), name='export_socios_csv'),
    path('exports/seguimientos/', ExportSeguimientosCSV.as_view(), name='export_seguimientos_csv'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
