#!/bin/bash
cd /opt/ona/onadata
. /opt/ona/onadata/bin/activate
python manage.py createsuperuser --noinput --username=ona --email=ona-info@cadasta.org
