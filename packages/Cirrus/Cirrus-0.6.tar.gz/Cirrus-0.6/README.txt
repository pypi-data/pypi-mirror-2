======
Cirrus
======

dns_setup reads a simple yaml file that only defines credentials, 
domains and bind style zone files used to define the domains.

update_host.py will update a single host entry in an route 53 domain. It 
relies on environment variables and command line arguments rather than 
yaml. I use it to accomplish dynamic dns for ec2 with the simple init 
script found in contrib. Since this will potentially be on many many 
machines for security I suggest you use a dns subdomain and different 
AWS credentials with this script.
