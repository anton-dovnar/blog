import socket

from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-3] + "0.1" for ip in ips]

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

# django-debug-toolbar
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE


# Logging with python rich package
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"rich": {"datefmt": "[%X]"}},
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "level": "DEBUG",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"]
        }
    },
}
