import os
activate_this = os.path.join('/opt/ona/onadata/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'onadata.settings.common'
application = get_wsgi_application()
