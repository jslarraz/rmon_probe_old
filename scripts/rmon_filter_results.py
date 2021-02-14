import os
import subprocess
import sys

# Direccion IP
ip_addr = "192.168.1.200"

# Comunidad
community = "jorge"

# Numero de filtros
n = 32

texto=['ARP_pkts','TCP_pkts','UDP_pkts','ICMP_pkts','HTTP_pkts_dst','HTTPS_pkts_dst','DNS_pkts_dst','FTP21_pkts_dst','SSH_pkts_dst','SMTP_pkts_dst','POP3_pkts_dst','NTP_pkts_dst','NETBIOS137_pkts_dst','NETBIOS138_pkts_dst','NETBIOS139_pkts_dst','IMAP_pkts_dst','SNMP_pkts_dst','RDESKTOP_pkts_dst','HTTP_pkts_ori','HTTPS_pkts_ori','DNS_pkts_ori','FTP21_pkts_ori','SSH_pkts_ori','SMTP_pkts_ori','POP3_pkts_ori','NTP_pkts_ori','NETBIOS137_pkts_ori','NETBIOS138_pkts_ori', 'NETBIOS139_pkts_ori','IMAP_pkts_ori','SNMP_pkts_ori','RDESKTOP_pkts_ori']
for i in range(n):

    # Leer channelMatches
    r = subprocess.check_output(["snmpget", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.9." + str(i+1)])
    value = str(r).split(" ")[-1]
    print(texto[i] + ": " + value)