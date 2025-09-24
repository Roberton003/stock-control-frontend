# Configuração de logging para o projeto Stock Control Lab
import os
from datetime import datetime

# Configuração de logging para o Django backend
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(module)s %(funcName)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'stock_control.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'errors.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'security.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'database_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'database.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'inventory': {  # Seu app principal
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'inventory.services': {  # Logs específicos para lógica de negócio
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'inventory.api': {  # Logs específicos para APIs
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['database_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'custom_security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# Para ambiente de produção, adicione também:
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'sentry_sdk.integrations.logging.SentryHandler',
        'formatter': 'verbose',
    }
    
    LOGGING['loggers']['inventory']['handlers'].append('sentry')
    LOGGING['loggers']['django']['handlers'].append('sentry')