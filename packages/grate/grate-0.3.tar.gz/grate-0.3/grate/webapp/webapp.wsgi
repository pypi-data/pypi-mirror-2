import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(sys.path[0], '..')))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
