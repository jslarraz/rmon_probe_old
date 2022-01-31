# Choose base image
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
WORKDIR /tmp/rmon
ADD rmon .


# Install MySQL database
RUN apt-get -y install mariadb-client

# Install NetSNMP rmon and manager
RUN apt-get -y install snmp

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
RUN cp -r /tmp/rmon /etc


EXPOSE 161/udp

#CMD ["sh /usr/bin/mysqld_safe & sleep 10 && python3 /etc/rmon/start.py"]
WORKDIR /etc/rmon
CMD ["python", "agenteV3_r1.py"]