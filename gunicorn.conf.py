import multiprocessing

# Configuración del servidor
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Configuración de archivos
keepalive = 2
timeout = 120
preload_app = True

# Configuración de logs
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Configuración del usuario (Hostinger usará su propio usuario)
# user = "www-data"
# group = "www-data"

# Configuración del proceso
daemon = False
pidfile = "/var/run/gunicorn/crm.pid"
tmp_upload_dir = None
