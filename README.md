# AWS deployment scripts for Cadasta platform v1

This comes in three parts:

1. An Ansible playbook to set up the "fixed" parts of the
   installation, using Vagrant for debugging and then, once it's
   working correctly, an EC2 instance to generate an Amazon Machine
   Image for later deployment.

2. A script to collect deployment details for a new platform instance.

3. An Ansible playbook to perform the configuration and deployment
   steps for the platform, based on per-instance information collected
   in step #2.  This playbook can deploy either into Vagrant or onto
   an AWS EC2 instance using the AMI generated in step #1.


### AMI generation

```
cd ami-setup
ansible-playbook ...
```
