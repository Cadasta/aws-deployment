

### Deployment information

Inputs:

I1. AWS credentials and region for setup
I2. Deployment name (must be unique)
I3. EC2 instance type
I4. RDS instance type and storage space

Derived information:

D1. Main and survey URLs (defaults: can override)
D2. EC2 name (fixed pattern based on deployment name)
D3. RDS name (fixed pattern based on deployment name)
D4. S3 name (fixed pattern based on deployment name)
D5. Names for other AWS resources (IAM roles, instance profiles, key
    pairs, etc.)
D6. Database access details (host, users, passwords, etc.)
D7. Rollbar secret key (just generate one?)
D8. RDS admin user credentials

Fixed information:

F1. Host IP address (should probably be set to localhost, since we're
    putting everything on one EC2 instance).
F2. ONA endpoint

References:

private-settings/cadasta-api/settings.js: D7
private-settings/cadasta-api/environment- settings.js: D4, D6, F1, F2
CKAN database creation: D3, D8
CKAN config file creation: D3, I2, D1
Solr database creation: D3, D8
Cadasta database creation: D3, D8
ONA database setup: D3, D8
Other ONA setup: ?

Fixed AWS resources:

 * IAM policies: EC2 trust policy, policy for instance profile

AWS resources:

 * VPC
 * Public subnet (EC2 instance)
 * Private subnet (RDS instance)


### Required code changes

Change L12-13 of cadasta-api/app/routes/resources.js from:

var AWS = require('aws-sdk');
AWS.config.update({accessKeyId: settings.s3.awsAccessKey, secretAccessKey: settings.s3.awsSecretKey});

to:

var AWS = require('aws-sdk');
if (settings.s3.hasOwnProperty('useEC2MetadataCredentials') &&
    settings.s3.useEC2MetadataCredentials)
  AWS.config.credentials = new AWS.EC2MetadataCredentials();
else
  AWS.config.update({ accessKeyId: settings.s3.awsAccessKey,
                      secretAccessKey: settings.s3.awsSecretKey });


### Ports

 * ONA: 8000
 * CKAN: 5000
 * Cadasta API: 3000
 * Solr: 8983

 * Postgres: 5432
 * Apache: 8080
 * nginx: proxy EXT_PORT -> 8080  (EXT_PORT=80 for deployment)


### Ansible variables for deployment step

db_host: PostgreSQL host
db_password: PostgreSQL "postgres" user password
deployment_name: Simple name for deployment (letters, digits, underscore only)
main_url: Main "front page" endpoint
survey_url: ONA endpoint
ckan_app_secret: Secret token for CKAN cookies
ckan_app_uid: UUID for CKAN config file
api_use_rollbar: Boolean - use rollbar.com for logging or not
api_rollbar_key: Secret token for Rollbar in API
s3_bucket: S3 bucket name
aws_region: AWS region
ona_app_secret: Secret token for ONA cookies
server_ip: Public-facing IP address of ONA server
domain_name: Public-facing FQDN of ONA server

import random
import string
import uuid

app_instance_secret = ''.join([random.choice(string.ascii_letters + string.digits)
                               for n in range(25)])
ona_app_secret = ''.join([random.choice(string.ascii_letters + string.digits)
                               for n in range(25)])
app_instance_uuid = str(uuid.uuid4())


### Web server setup

The way this is set up is that there is an `nginx` front end listening
on port 80, proxying requests to local port 8080 and providing front
end caching.

There's an Apache server listening on port 8080 with two virtual
hosts, one for the main CKAN application and one for ONA.

Both CKAN and ONA are WSGI applications, run as follows:

##### CKAN

/etc/ckan/default/apache.wsgi file:

```
import os
activate_this = os.path.join('/usr/lib/ckan/default/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from paste.deploy import loadapp
config_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'production.ini')
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)
application = loadapp('config:%s' % config_filepath)
```

##### ONA

(I've modified this: by default, ONA uses `uwsgi`.)

/etc/ona/onadata/apache.wsgi file:

```
import os
activate_this = os.path.join('/opt/ona/onadata/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```


### AWS resources

Need to create:

1. VPC
2. Public subnet in the VPC
3. Private subnet in the VPC
4. Elastic IP address
5. Internet gateway
6. RDS database
7. S3 bucket
8. EC2 instance
