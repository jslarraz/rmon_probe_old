from snmp_requests import snmp_engine
import time

# Direccion IP
ip_addr = ""

# Interface
interface_name = "eth0"

# Comunidad
community = ""

# Numero de filtros
n = 32


# User with authPriv settings
user = {
	"username": "Jorge",
	"level": "authPriv",
	"authKey": "ABCDEFGHIJK",
	"authAlg": "MD5",
	"privKey": "ABCDEFGHIJK",
	"privAlg": "DES"
}


# Create the requests engine
#eng = snmp_engine('3', user, '192.168.1.200', 161)
eng = snmp_engine('1', 'private', '192.168.1.200', 161)

t_start = time.time()

#################################
# Buscamos el OID del interface #
#################################

oid_interface = None
varBinds = eng.snmpwalk("1.3.6.1.2.1.2.2.1.2")
print (varBinds)
for varBind in varBinds:
	if interface_name == str(varBind[1][1]):
		oid_interface = str(varBind[0]).split('.')[-1]
		try:
			oid_interface = str(int(oid_interface))
		except:
			exit(0)

if oid_interface == None:
	print("OID_interface is None, shutting down.")
	exit(0)

print(oid_interface)


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
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.11." + str(i+1), ("INTEGER", 2)]])
	# Le indico a que canal pertenece con filterChannelIndex
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.2." + str(i+1), ("INTEGER", i+1)]])
	# Le indico el offset del paquete con filterPktDataOffset 14 de ethernet
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.3." + str(i+1), ("INTEGER", offset[i])]])
	# Le indico los datos que me interesan
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.4." + str(i+1), ("hexValue", proto[i])]])
	# Le indico la mascara de los datos con filterPktDataMask
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.5." + str(i+1), ("hexValue", "F"*len(proto[i]))]])
	# Le indico la mascara de los datos con filterPktDataNotMask
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.6." + str(i+1), ("hexValue", "0"*len(proto[i]))]])
	# Le indico el estado que me interesan
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.7." + str(i+1), ("INTEGER", 0)]])
	# Le indico la mascara de los datos con filterPktDataMask
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.8." + str(i+1), ("INTEGER", 7)]])
	# Le indico la mascara de los datos con filterPktDataNotMask
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.9." + str(i+1), ("INTEGER", 0)]])
	# Le indico el propietario con filterOwner
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.10." + str(i+1), ("STRING", "Jorge")]])
	# Activo la entrada con filterStatus
	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.11." + str(i+1), ("INTEGER", 1)]])

	# Ahora tengo que crear el canal
	# Creo la entrada con channelStatus
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.12." + str(i+1), ("INTEGER", 2)]])
	# Controlo el interfaz por el que filtro con channelIfIndex
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.2." + str(i+1), ("INTEGER", oid_interface)]])
	# Controlo la accion asociada con este canal con channelAcceptType
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.3." + str(i+1), ("INTEGER", 1)]])
	# Controlo si el canal esta activado o no con channelDataControl
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.4." + str(i+1), ("INTEGER", 1)]])
	# Controla el evento que se va a hacer que el canal se active, en caso de no estarlo (0 es que no hay)
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.5." + str(i+1), ("INTEGER", 0)]])
	# Controla el evento que se va a hacer que el canal se desactive, en caso de no estarlo (0 es que no hay)
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.6." + str(i+1), ("INTEGER", 0)]])
	# Controla el evento que se va a disparar el canal, en caso de no estarlo (0 es que no hay)
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.7." + str(i+1), ("INTEGER", 0)]])
	# Controla la forma en que se dispara eventos
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.8." + str(i+1), ("INTEGER", 2)]])
	# Le doy una descriptcion textual
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.10." + str(i+1), ("STRING", texto[i])]])
	# Le indico el propietario con channelOwner
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.11." + str(i+1), ("STRING", "Jorge")]])
	# Activo la entrada con channelStatus
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.12." + str(i+1), ("INTEGER", 1)]])

	print("Filtro " + str(i+1))

print(time.time()-t_start)