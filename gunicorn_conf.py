# Gunicorn config file
import os

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))
worker_class = "uvicorn.worker.UvicornWorker"

# Logging
loglevel = os.environ.get('GUNICorn_LOGLEVEL', 'info')
accesslog = '-' # Log to stdout
errorlog = '-'  # Log to stderr

# Timeouts
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))
keepalive = int(os.environ.get('GUNICORN_KEEPALIVE', '5'))

# For Render deployment, trust the headers sent by the proxy
forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-FORWARDED-PROTO': 'https' }
