from django.urls import path
from . import views

app_name = 'socios'

urlpatterns = [
    path('', views.SocioComercialListView.as_view(), name='lista'),
    path('crear/', views.SocioComercialCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.SocioComercialDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.SocioComercialUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.SocioComercialDeleteView.as_view(), name='eliminar'),
    path('<int:pk>/contrato/', views.ver_contrato, name='ver_contrato'),
]
