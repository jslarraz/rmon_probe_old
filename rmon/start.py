#!/usr/bin/python
# -*- coding: utf-8 -*-
# Iniciamos el agente
import subprocess
import time

# Start mysql
subprocess.call(["service", "mysql", "restart"])
time.sleep(3)


# Start snmpd
subprocess.call(["service", "snmpd", "restart"])
time.sleep(3)


# Start rmon agent
#import agente
#agente.agente()

# Start rmon agent3
import agentV3_r1
agentV3_r1.agent_v3('config.json')
