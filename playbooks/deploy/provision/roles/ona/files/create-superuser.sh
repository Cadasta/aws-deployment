#!/bin/bash
PWD=$1
cd /opt/ona/onadata
. /opt/ona/onadata/bin/activate
python manage.py shell <<EOF
from django.contrib.auth.models import User
u, created = User.objects.get_or_create(username='admin')
u.set_password('$PWD')
u.is_superuser = True
u.is_staff = True
u.save()
EOF
