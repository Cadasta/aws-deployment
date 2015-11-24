#!/bin/bash
export PGDATABASE=onadata
export PGHOST=localhost
export PGUSER=onadata
psql -U postgres -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
psql -U postgres -c 'CREATE EXTENSION IF NOT EXISTS postgis_topology;'
cd /opt/ona/onadata
. /opt/ona/onadata/bin/activate
python manage.py syncdb  --noinput
python manage.py migrate
