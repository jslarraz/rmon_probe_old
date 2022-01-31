# RMON probe
RMON probe implementation (rfc 2819) using python and libpcap. Only the filter group is implemented at this moment.

## Getting started

The easiest way to get started is to use this probe as a standalone docker container. You can do this simply by running 
the following command.

```
docker run -p 161:161/udp --net=host --name rmon_probe jslarraz/rmon_probe_standalone
```

## Better alternatives

You can also run the probe with as a set of containers using docker compose, which is a more reliable alternative. There
are two ways to manage secrets between container, using docker secrets or environment variables. 

### Create secrets

#### Docker secrets

This is the preferred way to manage your secrets within the docker environment. You should start creating the required 
docker secrets using your docker cli. 

```
printf "my_root_pass" | docker secret create rmon-db-root -
printf "my_db_name" | docker secret create rmon-db-name -
printf "my_user" | docker secret create rmon-db-user -
printf "my_pass" | docker secret create rmon-db-pass -
```

#### Environment variables

This method is not current supported in this version but is planned to be supported for development environments in the 
future. 

### Run the docker-compose

## Workaround for windows containers

If you want to run it on Docker for windows you will need the following workaround. The idea is to allow the rmon_probe
container to capture packages on the host using  tshark (which is distributed as part of wireshark) over ssh, and the 
use tcpreplay to send them over the interface of the docker container. This could be achieved by running the following 
command on the rmon_probe container. 

```
ssh win_user@win_host tshark -w - 'not port 22' | tcpreplay -i eth0 -
```

You need to increase the MTU of the docker network. It can be done by including the following option in the docker 
daemon config file.

```
"mtu": 9000"
```

## Community management

In this project, the SNMP communities and, therefore, the access privileges, are managed through a new MIB defined for 
this purpose, the communityManagement MIB. The agent is initialized with a default master community, "admin", with read 
and write privileges on objects that belong to the communityManagement MIB and can be used to define new communities and 
assign privileges to them. Thus, first step to start using the probe is to create a new community with privileges on the 
filter group objects. The script "create_community.py" (under the scripts folder) shows how to modify the default master 
community, "admin", and how to use this new master community to create other communities with custom access privileges.

## References

Code in this repository was initially developed as part of my Final undergraduate project, and full details about the 
system architecture, implementation decisions and performance test is available at project report (only Spanish).

https://zaguan.unizar.es/record/31543?ln=en

