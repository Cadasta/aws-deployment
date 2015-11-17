#!/usr/bin/env python

import boto3
import os, sys, subprocess
from os.path import normpath, join, dirname, abspath
from datetime import datetime, timezone, timedelta

from ami import get_ami, set_ami

if len(sys.argv) != 3:
    print('Usage: make-base-ami.py aws-profile private-key-file')
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

# Look up Ubuntu AMI for region.
ubuntu_ami = get_ami('ubuntu', aws_region)

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
base_ami_name = "cadasta-v1.base." + tstamp

# Set up command.
work_dir = normpath(join(dirname(abspath(__file__)),
                         '../playbooks/make-base-ami/provision'))
extra_vars = [('aws_profile', aws_profile),
              ('aws_region',  aws_region),
              ('ubuntu_ami', ubuntu_ami),
              ('vpc_subnet_id', vpc_subnet_id),
              ('base_ami_name', base_ami_name)]
extra_vars = ' '.join(map(lambda p: p[0] + '=' + p[1], extra_vars))
cmd = ['ansible-playbook',
        '--private-key=' + private_key_file,
        '--extra-vars', extra_vars,
       'make-base-ami.yml']

# Run playbook.
os.chdir(work_dir)
os.environ['ANSIBLE_HOST_KEY_CHECKING'] = 'false'
if subprocess.call(cmd) != 0:
    print('ansible-playbook TERMINATED INCORRECTLY!')
    sys.exit(1)


# Find and save new AMI ID.
images = ec2.describe_images(Owners=['self'],
                             Filters=[{'Name': 'name',
                                       'Values': [base_ami_name]}])['Images']
if len(images) != 1:
    print("Oops.  Can't find base image ID!")
    sys.exit(1)
base_ami = images[0]['ImageId']
print("WRITING AMI ID '{}' FOR TYPE 'base', REGION '{}'".
      format(base_ami, aws_region))
set_ami('base', aws_region, base_ami)
