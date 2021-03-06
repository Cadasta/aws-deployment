#!/bin/bash
cd /opt/cadasta/cadasta-db/sql
export PGHOST=$1
export PGUSER=cadasta
export PGDATABASE=cadasta
psql -U postgres -c 'CREATE EXTENSION postgis;'
psql -f 1_db.sql
psql -f 2_field-data-tables.sql
psql -f 3_db-functions.sql
psql -f 4_db-views.sql
psql -f 5_validation-functions.sql
