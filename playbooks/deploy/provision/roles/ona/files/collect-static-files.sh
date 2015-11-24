#!/bin/bash
cd /opt/ona/onadata
. /opt/ona/onadata/bin/activate
python manage.py collectstatic  --noinput
