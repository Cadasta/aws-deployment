#!/usr/bin/env python

import os.path
import json
import textwrap

# S3 bucket for storing secrets.
s3_bucket = 'cadasta-secrets'
s3_folder = 'ckan-deployments/'

# S3 bucket and key.
bucket = None
key = None

# Deployment options.
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


def set_session(aws=None):
    global bucket
    bucket = aws.resource('s3').Bucket(s3_bucket)


def list():
    return [os.path.basename(o.key)
            for o in bucket.objects.filter(Prefix=s3_folder)
            if o.key.endswith('.json')]


def exists(name=None):
    if name is None:
        name = vals['deployment_name']
    return name + '.json' in list()


def set(name=None):
    global key
    if name:
        vals['deployment_name'] = name
    key = os.path.join(s3_folder, vals['deployment_name'] + '.json')


def write():
    body = json.dumps(vals, sort_keys=True, indent=4)
    bucket.put_object(Body=body.encode(),
                      ContentType='application/json',
                      Key=key)


def read():
    global vals
    body = bucket.Object(key).get()['Body'].read()
    vals = json.loads(body.decode())


def get(key, prompt, help, default=None, values=None, check=None):
    v = None
    if not default and vals[key]:
        default = vals[key]
    while not v:
        v = input(prompt + (' [' + default + ']' if default else '') + ': ')
        if v == '?':
            print()
            print(help, end='\n\n')
            v = None
        if v == '' and default:
            v = default
        if v and values and v not in values:
            msg = textwrap.fill('Invalid selection.  Must be one of: ' +
                                ', '.join(values))
            print('\n' + msg + '\n')
            v = ''
        if v and check and not check(v):
            v = ''
    vals[key] = v
