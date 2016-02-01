#!/bin/bash
. /usr/lib/ckan/default/bin/activate
cd /opt/cadasta/cadasta-api
npm -f install
pip install -r requirements.txt
grunt updateDocs
