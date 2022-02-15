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

# Install MySQL client
RUN apt-get -y install mariadb-client

# Install NetSNMP
RUN apt-get -y install snmp

# Install dependencies for RMON
RUN apt-get -y install procps
RUN apt-get -y install gcc
RUN apt-get -y install tcpdump
RUN apt-get -y install libpcap-dev
RUN apt-get -y install python-libpcap

RUN apt-get -y install python
RUN apt-get -y install python-pip
RUN apt-get -y install python-mysqldb


# Install requirements
ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# Copy project files to working directory
WORKDIR /etc/rmon
ADD rmon .


EXPOSE 161/udp
CMD ["python", "agentV3_r1.py"]
