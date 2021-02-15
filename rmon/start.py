#!/usr/bin/python
# -*- coding: utf-8 -*-
# Iniciamos el agente
import agente
import subprocess
import time

# Start mysql
subprocess.call(["service", "mysql", "restart"])
time.sleep(3)


# Start snmpd
subprocess.call(["service", "snmpd", "restart"])
time.sleep(3)

# Start rmon agent
miAgente = agente.agente()
