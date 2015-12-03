#!/bin/bash
export PGHOST=$1
export PGDATABASE=onadata
export PGUSER=onadata
psql -U postgres -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
psql -U postgres -c 'CREATE EXTENSION IF NOT EXISTS postgis_topology;'
cd /opt/ona/onadata
. /opt/ona/onadata/bin/activate
python manage.py syncdb  --noinput
python manage.py migrate
export SITE=$2
python manage.py shell <<EOF
from django.contrib.sites.models import *
s = Site.objects.get_current()
s.name = '$SITE'
s.domain = '$SITE'
s.save()
EOF
