from snmp_requests import snmp_engine

# Read config
import os

ip_addr = os.environ.get('ip_addr', 'localhost')			# Direccion IP
port = os.environ.get('port', 161)							# Puerto
community = os.environ.get('community', 'public')			# Comunidad
eng = snmp_engine('1', community, ip_addr, port)             # Create engine

# Numero de filtros
n = 32

texto=['ARP_pkts','TCP_pkts','UDP_pkts','ICMP_pkts','HTTP_pkts_dst','HTTPS_pkts_dst','DNS_pkts_dst','FTP21_pkts_dst','SSH_pkts_dst','SMTP_pkts_dst','POP3_pkts_dst','NTP_pkts_dst','NETBIOS137_pkts_dst','NETBIOS138_pkts_dst','NETBIOS139_pkts_dst','IMAP_pkts_dst','SNMP_pkts_dst','RDESKTOP_pkts_dst','HTTP_pkts_ori','HTTPS_pkts_ori','DNS_pkts_ori','FTP21_pkts_ori','SSH_pkts_ori','SMTP_pkts_ori','POP3_pkts_ori','NTP_pkts_ori','NETBIOS137_pkts_ori','NETBIOS138_pkts_ori', 'NETBIOS139_pkts_ori','IMAP_pkts_ori','SNMP_pkts_ori','RDESKTOP_pkts_ori']
for i in range(n):

    # Leer channelMatches
    r = eng.snmpget([["1.3.6.1.2.1.16.7.2.1.9." + str(i+1)]])
    print(texto[i] + ": " + r[0][1][1])