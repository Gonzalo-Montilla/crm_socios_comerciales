from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    # URLs para Clientes
    path('', views.ClienteListView.as_view(), name='lista'),
    path('crear/', views.ClienteCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='eliminar'),
    
    # URLs para Cupos de Crédito
    path('cupos/', views.CupoCreditoListView.as_view(), name='cupos_credito'),
    path('cupos/crear/', views.CupoCreditoCreateView.as_view(), name='crear_cupo'),
]
