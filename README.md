# AWS deployment scripts for Cadasta platform v1

There are three steps to this, accessible via the `make-base-ami`,
`create-deployment` and `deploy` scripts in the `scripts` directory.
However, it is also possible to use the same Ansible playbooks used
for setup on AWS in Vagrant for debugging purposes.  See the section
*Using Vagrant* below.


### Generating AMIs

An Ansible playbook driven by the `make-base-ami` script is used to
set up the base "fixed" parts of the installation (i.e. operating
system package installation, etc.), using an EC2 instance to generate
an Amazon Machine Image for later deployment.

The rationale for this is that there are a *lot* of operating system
dependencies that need to be installed, and these are likely to change
far less frequently than the platform code itself.  Breaking the
deployment into two steps (OS package installation and project code
installation and configuration) means that the most frequent actions
should be relatively quick.

The AMIs generated by this process are registered in a
`machine-images.csv` file since they are AWS region-specific.  The
easiest way to do a deployment in a new region is simply to copy the
deployment AMI from an existing region using the AWS console or
command line and then to add an appropriate line to the
`machine-images.csv` file.

The `make-base-ami` script takes the following parameters:

1. The name of an AWS configuration profile to use for accessing
   credentials to connect to AWS.  (Set one of these up using the `aws
   configure` command.)

2. The path to a private key file used for connecting to the sandbox
   EC2 instance used for generating the AMI.  (You'll need to use the
   `cadasta-utility` key pair for this.  Just ask me [Ian] and I can
   give it to you.  If I've left or been eaten by a grue, just destroy
   and recreate the `cadasta-utility` key pair and save the PEM file
   somewhere.)

So, if you have an AWS profile called `cadasta` that has permissions
to manipulate AWS entities belonging to the Cadasta account, you can
create a fresh base AMI like this:

```
./scripts/make-base-ami cadasta ~/.ssh/cadasta-utility.pem
```

The base AMI is built from the standard Ubuntu 14.04 LTS AMI for the
region being used and contains all of the operating system and
"external" software packages needed to support the Cadasta platform
code.  The base AMI should not need to be changed for code changes to
the Cadasta platform unless package dependencies change.


### Creating a deployment

The `create-deployment` script is a quick and simple thing to generate
a configuration file for a new deployment.  These files are JSON and
live in the `deployments` directory.

When you run `create-deployment`, you'll need to provide:

 * A unique alphanumeric deployment name.
 * An endpoint URL for the platform front page (by default this is
   `foo.cadasta.org` for a deployment `foo`).
 * An endpoint URL for the ONA instance (by default this is
   `foo-survey.cadasta.org` for a deployment `foo`).
 * An AWS EC2 instance type to use for running all the plaform
   processes.
 * An AWS RDS instance type to use for running the Postgres database.

There are some other things you can change in the deployment file
(notably the amount of storage allocated for the RDS instance, which
defaults to 10 Gb), but most of the defaults should be good.


### Deploying

Once you've created a deployment with `create-deployment`, you can
deploy it to AWS using the `deploy` script, which you invoke with an
AWS profile name, a path to an SSH key file and a deployment name, for
example:

```
./scripts/deploy cadasta ~/.ssh/cadasta-utility.pem uat
```

The `deploy` script works in two stages:

1. First, it uses AWS CloudFormation to set up all the AWS resources
   needed (EC2 instance, RDS instance, S3 bucket, networking
   infrastructure).  For a deployment `foo`, the CloudFormation stack
   that's created is called `foo-stack`.  The `deploy` script will
   *not* allow you to overwrite an existing stack of the same name!
   If you want to do a fresh deployment, delete the stack from the AWS
   CloudFormation console.  If you want to do a *re*deployment, use
   the `redeploy` script (**not yet written**).

2. The EC2 instance created as part of the CloudFormation stack is
   provisioned using an Ansible playbook that installs all the
   platform-specific code, sets up database infrastructure, and sets
   up an Apache+nginx configuration suitable for serving both the main
   platform and ONA from the same EC2 instance.

This all takes a little while, but once the deployment process is
complete, you can look in the JSON deployment file for your deployment
to find the public IP address of the EC2 instance, and can then set up
DNS entries to point from (for example) `foo.cadasta.org` and
`foo-survey.cadasta.org` to that IP address.  (**This will be
automated soon.**)


### AWS prerequisites

The AMI setup steps make use of some pre-existing AWS entities I
defined for utility purposes.  If these get deleted by accident,
you'll need to recreate them to be able to use these scripts:

 * A VPC subnet called `ami-builders` on the default VPC for the
   Cadasta AWS account.  Doesn't matter what CIDR (I used
   172.31.64.0/20).
 * A VPC security group called `cadasta-utility` with an inbound rule
   permitting SSH connections.
 * A key pair called `cadasta-utility` (you'll need the PEM file for
   this).


### Using Vagrant

As well as making AMIs and deploying to an AWS EC2 instance, you can
also run all the Ansible provisioning steps within Vagrant, which is
handy for debugging.

To bring up a VM provisioned with the base image, go to
`playbooks/make-base-ami` and do `vagrant up --provision`.
Eventually, you'll end up with a running VM containing all the base
prerequisites for the Cadasta platform.  You can save this as a
Vagrant box for use later by doing

```
vagrant package --output /big/cadasta/cadasta-deploy.box
vagrant box add --name cadasta-base /big/cadasta/cadasta-deploy.box
```

Once you've done this, you can test the deployment playbook in
`playbooks/deploy`.  First do `vagrant up --no-provision` to get the
VM running, then do the following to allow the VM access to your local
Postgres server (since we're not going to run Postgres on the VM, you
need a Postgres server locally):

```
vagrant ssh -- -R127.0.0.1:5432:/var/run/postgresql/.s.PGSQL.5432
```

Leave that SSH session active, and you can now do a `vagrant
provision`.

There's some URL rewriting trickery in the nginx setup to make the
main platform site appear at `http://localhost:7000/` once everything
is up and running.
