# RMON probe
RMON probe implementation (rfc 2819) using python and libpcap. Only the filter group is implemented at this moment.

The easiest way to get started is to use this probe as a docker container. You can do this simply by running the 
following command.

```
sudo docker run -p 161:161/udp --net=host --name rmon_probe jslarraz/rmon_probe
```

In this project, the SNMP communities and, therefore, the access privileges, are managed through a new MIB defined for 
this purpose, the communityManagement MIB. The agent is initialized with a default master community, "admin", with read 
and write privileges on objects that belong to the communityManagement MIB and can be used to define new communities and 
assign privileges to them. Thus, first step to start using the probe is to create a new community with privileges on the 
filter group objects. The script "create_community.py" (under the scripts folder) shows how to modify the default master 
community, "admin", and how to use this new master community to create other communities with custom access privileges.



Code in this repository was initially developed as part of my Final undergraduate project, and full details about the 
system architecture, implementation decisions and performance test is available at project report (only Spanish).

https://zaguan.unizar.es/record/31543?ln=en

