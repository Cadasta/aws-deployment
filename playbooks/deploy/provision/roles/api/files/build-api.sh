#!/bin/bash
. /usr/lib/ckan/default/bin/activate
cd /opt/cadasta/cadasta-api
npm install
pip install -r requirements.txt
grunt updateDocs
