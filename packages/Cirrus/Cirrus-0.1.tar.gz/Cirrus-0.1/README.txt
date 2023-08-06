======
Cirrus
======

This project leverages boto and simple yaml config to create and 
maintain an AWS cloud configuration.

Running with your defined config will by default check the existing 
cloud setup and make it match your config.

There are two main scripts dns_setup.py and ec2_setup.py. Each read a 
yaml file for configuration including amazon aws credentials. Example 
yaml files are are in the examples dir.

dns_setup reads a simple yaml file that only defines credentials, 
domains and bind style zone files used to define the domains.

ec2_setup tries to do everything needed to get an ec2 infrastructure 
running. This includes load balancers, security groups and ec2 
instances.


NOTE
====
* As of 12-23-2010 the latest released version of boto is 
2.0b3, it does not contain route 53 code so a package must be build from
source.
