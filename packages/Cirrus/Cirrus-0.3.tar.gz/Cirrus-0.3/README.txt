======
Cirrus
======

This project leverages boto and simple yaml config to create and 
maintain an AWS cloud configuration.

Running with your defined config will by default check the existing 
cloud setup and make it match your config.

dns_setup.py and ec2_setup.py each read a yaml file for configuration 
including amazon aws credentials. Example yaml files are are in the 
examples dir.

dns_setup reads a simple yaml file that only defines credentials, 
domains and bind style zone files used to define the domains.

ec2_setup tries to do everything needed to get an ec2 infrastructure 
running. This includes load balancers, security groups and ec2 
instances.

update_host.py will update a single host entry in an route 53 domain. It 
relies on environment variables and command line arguments rather than 
yaml. I use it to accomplish dynamic dns for ec2 with the simple init 
script found in contrib. Since this will potentially be on many many 
machines for security I suggest you use a dns subdomain and different 
AWS credentials with this script.
