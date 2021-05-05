from snmp_requests import snmp_engine

# Read config
import os

ip_addr = os.environ.get('ip_addr', 'localhost')			# Direccion IP
port = os.environ.get('port', 161)							# Puerto
community = os.environ.get('community', 'public')			# Comunidad
eng = snmp_engine('1', community, ip_addr, port)             # Create engine

for i in range(32):

	eng.snmpset([["1.3.6.1.2.1.16.7.1.1.11." + str(i+1), ("INTEGER", 4)]])
	eng.snmpset([["1.3.6.1.2.1.16.7.2.1.12." + str(i+1), ("INTEGER", 4)]])
