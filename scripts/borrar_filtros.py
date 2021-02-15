import os
import subprocess

# Direccion IP
ip_addr = "192.168.1.200"

# Comunidad
community = "jorge"

for j in range(32):
	i = j+1

	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.1.1.11." + str(i), "i", "4"])

	subprocess.call(["snmpset", "-v", "1", "-c", community, ip_addr, "1.3.6.1.2.1.16.7.2.1.12." + str(i), "i", "4"])
