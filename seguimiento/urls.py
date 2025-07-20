from django.urls import path
from . import views

app_name = 'seguimiento'

urlpatterns = [
    path('', views.SeguimientoSocioListView.as_view(), name='lista'),
    path('crear/', views.SeguimientoSocioCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.SeguimientoSocioDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.SeguimientoSocioUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.SeguimientoSocioDeleteView.as_view(), name='eliminar'),
]
