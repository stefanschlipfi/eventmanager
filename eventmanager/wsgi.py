"""
WSGI config for eventmanager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

path = '/opt/eventmanager/'
if not path in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventmanager.settings')

application = get_wsgi_application()
