#!/bin/bash

# Script de deployment para Hostinger
# Configuración de variables de entorno para producción

echo "=== Iniciando deployment del CRM Socios Comerciales ==="

# Activar entorno virtual (si existe)
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Entorno virtual activado"
fi

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Configurar variables de entorno (estas se configurarán en Hostinger)
export DJANGO_SETTINGS_MODULE="crm_socios_comerciales.production_settings"

# Generar archivos estáticos
echo "Generando archivos estáticos..."
python manage.py collectstatic --noinput

# Aplicar migraciones
echo "Aplicando migraciones de base de datos..."
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (opcional, solo la primera vez)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@reportescredisensa.com', 'tu_password_seguro')" | python manage.py shell

echo "=== Deployment completado ==="
echo "La aplicación está lista para ejecutarse con:"
echo "gunicorn -c gunicorn.conf.py crm_socios_comerciales.wsgi:application"
