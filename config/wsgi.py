import os

from django.core.wsgi import get_wsgi_application

env = os.getenv('ENV', "config.setting.local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env)

application = get_wsgi_application()
