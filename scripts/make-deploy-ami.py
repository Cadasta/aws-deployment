#!/usr/bin/env python

import boto3
import os, sys, subprocess
from os.path import normpath, join, dirname, abspath
from datetime import datetime, timezone, timedelta

from ami import get_ami, set_ami

if len(sys.argv) != 3:
    print('Usage: make-deploy-ami.py aws-profile private-key-file')
    sys.exit(1)

# AWS profile and private key file to use.
aws_profile = sys.argv[1]
private_key_file = sys.argv[2]

# Make sure profile works and look up region from profile.
try:
    aws = boto3.session.Session(profile_name=aws_profile)
except:
    print('FAILED TO CREATE AWS SESSION USING PROFILE "' + aws_profile + '"')
    sys.exit(1)
aws_region = aws._session.get_config_variable('region')

# Look up base AMI for region.
base_ami = get_ami('base', aws_region)

# Look up VPC subnet ID (by name: "ami-builders").  Everything else is
# fixed and referenced by name (key pair: cadasta-utility, security
# group: cadasta-utility).
ec2 = aws.client('ec2')
vpc_subnet_id = None
for sn in ec2.describe_subnets()['Subnets']:
    if 'Tags' in sn:
        n = list(filter(lambda t: t['Key'] == 'Name', sn['Tags']))[0]['Value']
        if n == 'ami-builders':
            vpc_subnet_id = sn['SubnetId']
            break
if not vpc_subnet_id:
    print("Couldn't find 'ami-builders' VPC subnet!")
    sys.ext(1)

# Generate a name for the new AMI.
tstamp = datetime.now(tz=timezone(timedelta(0))).strftime("%Y%m%d%H%M%SZ")
deploy_ami_name = "cadasta-v1.deploy." + tstamp

# Set up command.
work_dir = normpath(join(dirname(abspath(__file__)),
                         '../playbooks/make-deploy-ami/provision'))
extra_vars = [('aws_profile', aws_profile),
              ('aws_region',  aws_region),
              ('base_ami', base_ami),
              ('vpc_subnet_id', vpc_subnet_id),
              ('deploy_ami_name', deploy_ami_name)]
extra_vars = ' '.join(map(lambda p: p[0] + '=' + p[1], extra_vars))
cmd = ['ansible-playbook',
        '--private-key=' + private_key_file,
        '--extra-vars', extra_vars,
       'make-deploy-ami.yml']

# Run playbook.
os.chdir(work_dir)
os.environ['ANSIBLE_HOST_KEY_CHECKING'] = 'false'
if subprocess.call(cmd) != 0:
    print('ansible-playbook TERMINATED INCORRECTLY!')
    sys.exit(1)


# Find and save new AMI ID.
images = ec2.describe_images(Owners=['self'],
                             Filters=[{'Name': 'name',
                                       'Values': [base_ami_name]}])
if len(images) != 1:
    print("Oops.  Can't find deploy image ID!")
    sys.exit(1)
deploy_ami = images['Images'][0]['ImageId']
print("WRITING AMI ID '{}' FOR TYPE 'deploy', REGION '{}'".
      format(deploy_ami, aws_region))
set_ami('deploy', aws_region, deploy_ami)
