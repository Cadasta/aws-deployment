#!/usr/bin/env python

from os.path import normpath, join, dirname, abspath, exists
import json


config_dir = normpath(join(dirname(abspath(__file__)), '../deployments'))

file = None

vals = {
    'deployment_name':    None,
    'db_host':            None,
    'db_password':        None,
    'ckan_main_url':      None,
    'apache_main_url':    None,
    'ona_survey_url':     None,
    'ona_admin_password': None,
    'apache_survey_url':  None,
    'ckan_app_secret':    None,
    'ckan_app_uuid':      None,
    'api_use_rollbar':    '"false"',
    'api_rollbar_key':    '""',
    'aws_region':         None,
    's3_bucket':          None,
    'ona_app_secret':     None,
    'server_ip':          '0.0.0.0',
    'ona_domain_name':    None,
    'ec2_instance_type':  't2.micro',
    'rds_instance_type':  'db.t2.micro',
    'rds_storage':        10,
    'public_ip':          None
}

def set(name=None):
    global file
    if name:
        vals['deployment_name'] = name
    file = join(config_dir, vals['deployment_name'] + '.json')

def write():
    with open(file, 'w', encoding='utf-8') as fp:
        json.dump(vals, fp, sort_keys=True, indent=4)

def read():
    global vals
    if exists(file):
        with open(file, encoding='utf-8') as fp:
            vals = json.load(fp)

def get(key, prompt, help, default=None, values=None, check=None):
    v = None
    if not default and vals[key]: default = vals[key]
    while not v:
        v = input(prompt +
                  (' [' + default +']' if default else '') + ': ')
        if v == '?':
            print()
            print(help, end='\n\n')
            v = None
        if v == '' and default: v = default
        if v and values and v not in values:
            msg = textwrap.fill('Invalid selection.  Must be one of: ' +
                                ', '.join(values))
            print('\n' + msg + '\n')
            v = ''
        if v and check and not check(v): v = ''
    vals[key] = v
