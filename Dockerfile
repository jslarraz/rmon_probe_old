# Seleccionamos la imagen base
FROM debian

# Set some environment vars
ENV DEBIAN_FRONTEND noninteractive

# Supress Upstart errors/warning
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl

# Update repository
RUN apt-get update

# Install apt-utils
RUN apt-get -y install apt-utils

# Copy project and change directory
ADD . /tmp
WORKDIR /tmp

# Install MySQL database
RUN apt-get -y install mariadb-server mariadb-client libmariadb3 mariadb-backup mariadb-common

# Load database and create user
RUN /usr/bin/mysqld_safe & \
    sleep 10s &&\
    mysql < rmon/mysql_config.sql

# Install NetSNMP rmon and manager
RUN apt-get -y install snmpd

# Change snmp default port
RUN sed -i -e"s/^agentAddress\s*udp:127.0.0.1:161/agentAddress  udp:127.0.0.1:162/" /etc/snmp/snmpd.conf

# Install dependencies for RMON
RUN apt-get -y install gcc
RUN apt-get -y install tcpdump
RUN apt-get -y install libpcap-dev

RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-mysqldb

RUN ln /usr/lib/x86_64-linux-gnu/libpcap.so.0.8 /usr/lib/x86_64-linux-gnu/libpcap.so.1

RUN pip3 install -r requirements.txt

# Install RMON
RUN cp -r rmon /etc
# RUN cp service/rmon /etc/init.d/rmon

EXPOSE 161/udp

CMD ["sh /usr/bin/mysqld_safe & sleep 10 && python3 /etc/rmon/start.py"]
