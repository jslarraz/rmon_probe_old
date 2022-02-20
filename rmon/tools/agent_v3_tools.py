#!/usr/bin/python
# -*- coding: utf-8 -*-

# Información sobre XML en python en https://docs.python.org/2/library/xml.dom.html#module-xml.dom

# Importamos todas la librerias necesarias
from pysnmp.proto import error, rfc1902, errind
import pysnmp.smi.error
from pysnmp.entity import engine, config
import ast
import json


# Dar formato a la respuesta

from pysnmp.proto.api import v2c
from pysnmp.smi import exval

def formato(varBinds, result):

    # Insertamos en el campo value "noSuchObject"
    if result[2] == 'noSuchObject':
        varBinds.append((v2c.ObjectIdentifier(result[0]),
                            exval.noSuchObject))

    # Insertamos en el campo value "noSuchInstance"
    elif result[2] == 'noSuchInstance':
        varBinds.append((v2c.ObjectIdentifier(result[0]),
                            exval.noSuchInstance))

    elif result[2] == 'endOfMibView':
        varBinds.append((v2c.ObjectIdentifier(result[0]),
                            exval.endOfMibView))

    # El oid por el que nos han preguntado tenia valor
    else:

        if result[2] == "INTEGER":
            varBinds.append((v2c.ObjectIdentifier(result[0]),
                             v2c.Integer(int(result[1]))))
        elif result[2] == "Timeticks":
            varBinds.append((v2c.ObjectIdentifier(result[0]),
                             v2c.TimeTicks(int(result[1]))))
        elif result[2] == "Counter32":
            varBinds.append((v2c.ObjectIdentifier(result[0]),
                             v2c.Counter32(int(result[1]))))
        elif result[2] == "OctetString":
            varBinds.append((v2c.ObjectIdentifier(result[0]),
                             v2c.OctetString(str(result[1]))))
        elif result[2] == "OID":
            varBinds.append((v2c.ObjectIdentifier(result[0]),
                             v2c.ObjectIdentifier(str(result[1]))))
        else:
            varBinds.append((v2c.ObjectIdentifier(result[0]),
                             v2c.OctetString(str(result[1]))))

    return varBinds



# Función encargada de incrementar el contador "snmpSilentDrops" en el caso correspondiente
def snmpSilentDrops(self):
    # snmpSilentDrops OID
    oid = 'o1o3o6o1o2o1o11o31o0'

    # Definimos la sentencia xpath y la utilizamos para realizar la busqueda en el xml
    find_oid_get = ET.XPath("//"+oid+'[@SYNTAX!="none" and @MAX-ACCESS!="not-accessible"]')
    node_O = find_oid_get(self.mib)

    # Intentamos tomar el primer objeto que coincida con nuestra busqueda.
    try:
        node_X = node_O[0]

    # En caso de que falle te aguantas...
    except:
        pass

    else:
        actual = int(node_X.text)
        if actual < 4294967295:
            node_X.text = str(actual + 1)
        else:
            node_X.text = 0



# https://stackoverflow.com/questions/6289646/python-function-as-a-function-argument
# https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-from-a-string-with-the-functions-name-in-python
def usmVacmSetup(self,filename):


    ### Recuperamos el usuario que recibira las notificaciones
    self.iniFile = json.loads(open(filename, 'rb').read())

    network = self.iniFile['network']
    nInterfaces = network['notificationInterfaces']
    nInterface = nInterfaces[0]
    nName = nInterface['securityName']

    ### Usuarios
    users = self.iniFile['users']
    for user in users:
        # find encuentra el primer hijo con ese nombre
        name = user['securityName']
        level = user['level']
        if level == 'noAuthNoPriv':
            config.addV3User(self.snmpEngine, name)
        elif level == 'authNoPriv':
            authAlg = user['authAlg']
            authKey = user['authKey']
            config.addV3User(self.snmpEngine, name, getattr(config, authAlg), authKey,)
        elif level == 'authPriv':
            privAlg = user['privAlg']
            privKey = user['privKey']
            authAlg = user['authAlg']
            authKey = user['authKey']
            config.addV3User(self.snmpEngine, name,getattr(config, authAlg), authKey, getattr(config, privAlg), privKey,)

        if name == nName:
            config.addTargetParams(self.snmpEngine, 'my-creds', name, level)

        config.addVacmUser(self.snmpEngine, 3, name, level)

    ### Grupos
    groups = self.iniFile['groups']
    for group in groups:
        # find encuentra el primer hijo con ese nombre
        groupName = group['groupName']
        users = group['securityName']
        for user in users:
            securityName = user
            config.addVacmGroup(self.snmpEngine, groupName, 3, securityName)

    ### Vistas
    views = self.iniFile['views']
    for view in views:
        viewName = view['viewName']
        oid = view['OID']
        oid = oid.replace('.',',')
        oid = '(' + oid[1:] + ')'
        config.addVacmView(self.snmpEngine, viewName, "included", ast.literal_eval(oid), "")

    ### Access
    access = self.iniFile['access']
    for group in access:
        groupName = group['groupName']
        level = group['level']
        read = group['read']
        write = group['write']
        notify = group['notify']
        config.addVacmAccess(self.snmpEngine, groupName, "", 3, level, "exact", read, write, notify)



    # V1 Security model test
    # SecurityName <-> CommunityName mapping.
    # Here we configure two distinct CommunityName's to control read and write
    # operations.

    config.addV1System(self.snmpEngine, 'my-read-area', 'public')
    config.addV1System(self.snmpEngine, 'my-write-area', 'private')

    # Allow full MIB access for this user / securityModels at VACM
    config.addVacmUser(self.snmpEngine, 2, 'my-read-area', 'noAuthNoPriv', (1, 3, 6, 1, 2, 1))
    config.addVacmUser(self.snmpEngine, 2, 'my-write-area', 'noAuthNoPriv', (1, 3, 6, 1, 2, 1), (1, 3, 6, 1, 2, 1))


    # Allow full MIB access for this user / securityModels at VACM
    config.addVacmUser(self.snmpEngine, 1, 'my-read-area', 'noAuthNoPriv', (1, 3, 6, 1, 2, 1))
    config.addVacmUser(self.snmpEngine, 1, 'my-write-area', 'noAuthNoPriv', (1, 3, 6, 1, 2, 1), (1, 3, 6, 1, 2, 1))