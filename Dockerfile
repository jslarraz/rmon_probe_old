# Choose base image
FROM jslarraz/netsnmp:latest

# Update repository
RUN apt-get update

# Install apt-utils
RUN apt-get -y install apt-utils

# Install MySQL client
RUN apt-get -y install mariadb-client

# Install NetSNMP
RUN apt-get -y install snmp

# Install dependencies for RMON
RUN apt-get -y install python
RUN apt-get -y install python-pip

RUN apt-get -y install libpcap-dev
RUN apt-get -y install python-libpcap
RUN apt-get -y install python-mysqldb


# Install requirements
ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# Copy project files to working directory
WORKDIR /etc/rmon
ADD rmon .

EXPOSE 161/udp
CMD snmpd && python agentV3_r1.py
