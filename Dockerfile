# Seleccionamos la imagen base
FROM debian:buster

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
RUN apt-get -y install snmp

# Change snmp default port
RUN sed -i -e"s/^agentAddress\s*udp:127.0.0.1:161/agentAddress  udp:127.0.0.1:162/" /etc/snmp/snmpd.conf
RUN sed -i -e"s/^view\s*systemonly\s*included\s*.1.3.6.1.2.1.1/view systemonly included .1.3.6.1.2.1/" /etc/snmp/snmpd.conf


# Install dependencies for RMON
RUN apt-get -y install procps
RUN apt-get -y install gcc
RUN apt-get -y install tcpdump
RUN apt-get -y install libpcap-dev
#RUN ln /usr/lib/x86_64-linux-gnu/libpcap.so.0.8 /usr/lib/x86_64-linux-gnu/libpcap.so.1
RUN apt-get -y install python-libpcap

RUN apt-get -y install python
RUN apt-get -y install python-pip
RUN apt-get -y install python-mysqldb



RUN pip install -r requirements.txt

# Install RMON
RUN cp -r rmon /etc
RUN cp service/rmon /etc/init.d/rmon

EXPOSE 161/udp

#CMD ["sh /usr/bin/mysqld_safe & sleep 10 && python3 /etc/rmon/start.py"]
WORKDIR /etc/rmon
CMD ["python", "start.py"]