import subprocess
import sys

# Direccion IP
ip_addr = "192.168.1.200"

# Comunidad
community = "jorge"



##########################
# Creamos la comunidad   #
##########################

subprocess.call(["snmpset", "-v", "1", "-c", "admin", ip_addr, "1.3.6.1.4.1.28308.2.1.6.\'"+community+"\'.1", "i", "2"])

subprocess.call(["snmpset", "-v", "1", "-c", "admin", ip_addr, "1.3.6.1.4.1.28308.2.1.4.\'"+community+"\'.1", "i", "3"])

subprocess.call(["snmpset", "-v", "1", "-c", "admin", ip_addr, "1.3.6.1.4.1.28308.2.1.5.\'"+community+"\'.1", "s", "1.3"])

subprocess.call(["snmpset", "-v", "1", "-c", "admin", ip_addr, "1.3.6.1.4.1.28308.2.1.6.\'"+community+"\'.1", "i", "1"])
