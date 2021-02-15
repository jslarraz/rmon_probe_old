import os
import subprocess
import sys

# Direccion IP
ip_addr = "192.168.1.200"

# Interface
interface_name = "enp3s0"

# Comunidad
community = "jorge"

# Numero de filtros
n = 32


#################################
# Buscamos el OID del interface #
#################################

oid_interface = None
r = subprocess.check_output(["snmpwalk", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.2.2.1.2"])
for line in str(r).split('\\n'):
	if interface_name in line:
		oid_interface = line.split('=')[0].split('.')[-1]
		try:
			oid_interface = str(int(oid_interface))
		except:
			exit(0)

if oid_interface == None:
	exit(0)

##########################
# Insertamos los filtros #
##########################

proto=['0806','06','11','01','0050','01BB','0035','0015','0016','0019','006E','007B','0089','008A','008B','008F','00A1','0D3D','0050','01BB','0035','0015','0016','0019','006E','007B','0089','008A','008B','008F','00A1','0D3D']
texto=['ARP_pkts','TCP_pkts','UDP_pkts','ICMP_pkts','HTTP_pkts_dst','HTTPS_pkts_dst','DNS_pkts_dst','FTP21_pkts_dst','SSH_pkts_dst','SMTP_pkts_dst','POP3_pkts_dst','NTP_pkts_dst','NETBIOS137_pkts_dst','NETBIOS138_pkts_dst','NETBIOS139_pkts_dst','IMAP_pkts_dst','SNMP_pkts_dst','RDESKTOP_pkts_dst','HTTP_pkts_ori','HTTPS_pkts_ori','DNS_pkts_ori','FTP21_pkts_ori','SSH_pkts_ori','SMTP_pkts_ori','POP3_pkts_ori','NTP_pkts_ori','NETBIOS137_pkts_ori','NETBIOS138_pkts_ori', 'NETBIOS139_pkts_ori','IMAP_pkts_ori','SNMP_pkts_ori','RDESKTOP_pkts_ori']
offset=['12']*1 + ['23']*3 + ['36']*14 + ['34']*14

#for i in range(len(proto)):	
for i in range(n):
	# Grupo filter
	# Primero creo el filtro
	# Creo la entrada con filterStatus
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.11." + str(i+1), "i", "2"])
	# Le indico el propietario con filterOwner
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.10." + str(i+1), "s", "Jorge"])
	# Le indico a que canal pertenece con filterChannelIndex
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.2." + str(i+1), "i", str(i+1)])
	# Le indico el offset del paquete con filterPktDataOffset 14 de ethernet
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.3." + str(i+1), "i", offset[i] ])
	# Le indico los datos que me interesan
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.4." + str(i+1), "x", proto[i] ])
	# Le indico la mascara de los datos con filterPktDataMask
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.5." + str(i+1), "x", "F"*len(proto[i]) ])
	# Le indico la mascara de los datos con filterPktDataNotMask
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.6." + str(i+1), "x", "0"*len(proto[i]) ])
	# Le indico el estado que me interesan
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.7." + str(i+1), "i", "0"])
	# Le indico la mascara de los datos con filterPktDataMask
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.8." + str(i+1), "i", "7"])
	# Le indico la mascara de los datos con filterPktDataNotMask
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.9." + str(i+1), "i", "0"])
	# Activo la entrada con filterStatus
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.11." + str(i+1), "i", "1"])
	
	# Ahora tengo que crear el canal
	# Creo la entrada con channelStatus
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.12." + str(i+1), "i", "2"])
	# Le indico el propietario con channelOwner
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.11." + str(i+1), "s", "Jorge"])
	# Le doy una descriptcion textual
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.10." + str(i+1), "s", texto[i] ])
	# Controlo el interfaz por el que filtro con channelIfIndex
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.2." + str(i+1), "i", oid_interface])
	# Controlo la accion asociada con este canal con channelAcceptType
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.3." + str(i+1), "i", "1"])
	# Controlo si el canal esta activado o no con channelDataControl
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.4." + str(i+1), "i", "1"])
	# Controla el evento que se va a hacer que el canal se active, en caso de no
	# estarlo (0 es que no hay)
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.5." + str(i+1), "i", "0"])
	# Controla el evento que se va a hacer que el canal se desactive, en caso de no
	# estarlo (0 es que no hay)
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.6." + str(i+1), "i", "0"])
	# Controla el evento que se va a disparar el canal, en caso de no
	# estarlo (0 es que no hay)
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.7." + str(i+1), "i", "0"])
	# Controla la forma en que se dispara eventos
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.8." + str(i+1), "i", "2"])
	# Activo la entrada con channelStatus
	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.12." + str(i+1), "i", "1"])
	

