import os
activate_this = os.path.join('/opt/ona/onadata/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
