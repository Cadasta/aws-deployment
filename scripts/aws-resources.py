#!/usr/bin/env python

import sys
import aws

#----------------------------------------------------------------------
#
#  USER AWS CREDENTIALS
#

# One of: ID and secret key environment variables; profile from
# command line or environment variable.  Don't proceed unless one of
# these is set up.

default_region = None
aws_profile = None
if len(sys.argv) == 3 and sys.argv[1] == '--profile':
    try:
        aws_profile = sys.argv[2]
        aws = boto3.session.Session(profile_name=aws_profile)
    except:
        print('FAILED TO CREATE AWS SESSION USING PROFILE "' +
              sys.argv[2] + '"')
        sys.exit(1)
    print('USING AWS CREDENTIAL PROFILE "' + sys.argv[2] + '"')
elif ('AWS_ACCESS_KEY_ID' in os.environ and
    'AWS_SECRET_ACCESS_KEY' in os.environ):
    print('USING AWS CREDENTIALS FROM ENVIRONMENT')
    try:
        aws = boto3.session.Session()
    except:
        print('FAILED TO CREATE AWS SESSION USING AWS_ACCESS_KEY_ID AND ' +
              'AWS_SECRET_ACCESS_KEY ENVIRONMENT VARIABLES')
        sys.exit(1)
elif 'AWS_PROFILE' in os.environ:
    try:
        aws_profile = os.environ['AWS_PROFILE']
        aws = boto3.session.Session(profile_name=aws_profile)
    except:
        print('FAILED TO CREATE AWS SESSION USING PROFILE "' +
              os.environ['AWS_PROFILE'] + '"')
        sys.exit(1)
    print('USING AWS CREDENTIAL PROFILE "' + os.environ['AWS_PROFILE'] + '"')
else:
    print("""
AWS CREDENTIALS ARE NOT SET UP

You need to create AWS credentials and either:

 - set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment
   variables, or

 - create a credentials profile using the AWS command line ("aws
   configure") and then either set the AWS_PROFILE environment
   variable or specify the environment on the command line using the
   '--profile' option.
""")
    sys.exit(1)

def usage():
    print("Usage: aws-resources.py [--profile <aws-profile>]")
    print("                        {create|destroy} <deployment-name>")
    sys.exit(1)

def main(argv):
    if len(argv) != 3: usage()
    if argv[1] == "create":
        create(argv[2])
    elif argv[1] == "destroy":
        destroy(argv[2])
    else:
        usage()

def vpc_name(name): return name + '-vpc.cadasta-v1'

def create(name):
    vpc_id = create_vpc(vpc_name(name))
