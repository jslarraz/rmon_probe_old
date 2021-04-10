#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importamos todas las librerias necesarias
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context, ntforg
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.proto.api import v2c
from pysnmp.smi import exval
from pysnmp.smi.error import GenError, AuthorizationError, NoAccessError
from pysnmp.proto import rfc1905, rfc1902

import MySQLdb
import mib
import signal
import re
import os
import subprocess

import tools
from agent_v3_tools import  usmVacmSetup, snmpSilentDrops, formato

import json

# Clase principal de nuestro agente
class agent_v3:
    ########################################################################################
    ### Variables que van a ser atributos de la clase, para
    ### ser accesibles desde cualquier método
    ########################################################################################


    def __init__(self, filename):


        # Leemos las opciones del fichero de configuracion
        self.load_config("/etc/rmon/rmon.conf")

        # Comprobamos la conectividad a Mysql y NetSNMP
        self.test_BBDD()
        self.test_SNMP()

        # Recogemos la informacion de los interfaces
        self.get_ifDescr()

        # Creamos la instancia de la mib
        self.mib = mib.mib(self.N_FILTROS, self.BBDD, self.SNMP, self.interfaces)

        # Configuramos la alarma
        signal.signal(signal.SIGALRM, self.update)
        signal.alarm(10)

        # Creo el SNMP engine
        snmpEngine = engine.SnmpEngine()
        self.snmpEngine = snmpEngine

        # Obtengo el SNMP context por defecto del SNMP engine
        snmpContext = context.SnmpContext(snmpEngine)

        # SNMPv3 VACM / USM setup
        usmVacmSetup(self, filename)


        # Configurar socket
        self.iniFile = json.loads(open(filename, 'rb').read())
        network = self.iniFile['network']
        interfaces = network['interfaces']
        interface = interfaces[0]
        ip_addr = interface['ip_addr']
        port = interface['port']

        config.addSocketTransport(
            snmpEngine,
            udp.domainName + (1,),
            udp.UdpTransport().openServerMode((ip_addr, int(port))),
        )


        # Configuraciones para la generacion de notificaciones
        nInterfaces = network['notificationInterfaces']
        nInterface = nInterfaces[0]
        ip_addr = nInterface['ip_addr']
        port = nInterface['port']

        config.addSocketTransport(
            snmpEngine,
            udp.domainName,
            udp.UdpSocketTransport().openClientMode()
        )
        config.addTargetAddr(
            snmpEngine, 'my-nms',
            udp.domainName, (ip_addr, int(port)),
            'my-creds',
            tagList='all-my-managers'
        )

        # Specify what kind of notification should be sent (TRAP or INFORM),
        # to what targets (chosen by tag) and what filter should apply to
        # the set of targets (selected by tag)
        config.addNotificationTarget(
            snmpEngine, 'my-notification', 'my-filter', 'all-my-managers', 'trap'
        )

        # Register SNMP Applications at the SNMP engine for particular SNMP context
        GCR = GetCommandResponder(snmpEngine, snmpContext, self.mib)
        SCR = SetCommandResponder(snmpEngine, snmpContext, self.mib)
        NCR = NextCommandResponder(snmpEngine, snmpContext, self.mib)
        #cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)
        #self.ntfOrg = ntforg.NotificationOriginator()




        # Register an imaginary never-ending job to keep I/O dispatcher running forever
        snmpEngine.transportDispatcher.jobStarted(1)

        # Run I/O dispatcher which would receive queries and send responses
        try:
            # Decimos agente ON
            print("SNMP Service ON")
            snmpEngine.transportDispatcher.runDispatcher()
        except:
            snmpEngine.transportDispatcher.closeDispatcher()
            raise



    # Load configuration from file
    def load_config(self, file):
        fd = open(file)
        line = fd.readline()
        while line:
            if '=' in line:
                substr = line.split('=')
                substr[1] = substr[1].split('\n')
                substr[1] = substr[1][0]

                if substr[0] == "IP_ADDR":
                    self.IP_ADDR = substr[1]
                elif substr[0] == "PORT":
                    self.PORT = int(substr[1])
                elif substr[0] == "BBDD_ADDR":
                    BBDD_ADDR = substr[1]
                elif substr[0] == "BBDD_USER":
                    BBDD_USER = substr[1]
                elif substr[0] == "BBDD_PASS":
                    BBDD_PASS = substr[1]
                elif substr[0] == "SNMP_ADDR":
                    SNMP_ADDR = substr[1]
                elif substr[0] == "SNMP_COMMUNITY":
                    SNMP_COMMUNITY = substr[1]
                elif substr[0] == "N_FILTROS":
                    self.N_FILTROS = int(substr[1])
                else:
                    print("Error al leer datos de configuracion")

            line = fd.readline()
        fd.close()

        try:
            self.BBDD = tools.BBDD(BBDD_ADDR, BBDD_USER, BBDD_PASS)
            self.SNMP = tools.SNMP_proxy(SNMP_ADDR, SNMP_COMMUNITY)
        except:
            print("Algunos parametros no estan definidos en el fichero de configuracíón rmon.conf")
            exit(-1)


    # Test database connectivity
    def test_BBDD(self):

        try:
            connection = MySQLdb.connect(host = self.BBDD.ADDR, user = self.BBDD.USER, passwd = self.BBDD.PASS)
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()

            if not('rmon' in str(databases)):
                statement = ""
                for line in open('/etc/rmon/mysql_config.sql'):
                    if re.match(r'--', line):
                        continue
                    if not re.search(r'[^-;]+;', line):
                        statement = statement + line
                    else:
                        statement = statement + line
                        try:
                            cursor.execute(statement)
                        except:
                            print("incorrect statement")
                        statement = ""
        except:
            print("Mysql is not running. Shutting down...")
            exit(-1)


    # Test SNMP proxy
    def test_SNMP(self):

        try:
            #Get SysUpTime to test if it is working
            aux = subprocess.check_output(["snmpget", "-v", "1", "-c", self.SNMP.COMMUNITY, "-Oben", self.SNMP.ADDR, "1.3.6.1.2.1.1.3.0"])

        except:
            print("NetSNMP is not running. Shutting down...")
            exit(-1)


    # Obtain interfaces names, avoid mistakes from net snmp in ifDesc
    def get_ifDescr(self):
        self.interfaces = {}
        for interface in os.listdir("/sys/class/net"):
            # Prevent bonding_masters to generate an exception
            if os.path.isdir("/sys/class/net/" + interface) and os.path.exists("/sys/class/net/" + interface + "/ifindex"):
                fd = open("/sys/class/net/" + interface + "/ifindex")
                try:
                    index = str(int(fd.readline()))
                except:
                    continue
                self.interfaces[index] = interface
                fd.close()


    # Check if the if description match the name of the interface
    def check_ifDescr(self, oid, val):
        # Check if the response oid matches the ifDescr
        suboid = str(oid).split(".")
        if (len(suboid) == 11) and (suboid[0:10] == ["1", "3", "6", "1", "2", "1", "2", "2", "1", "2"]):
            # Check if the requested ifIndex exists in our db
            ifIndex = suboid[10]
            if ifIndex in self.interfaces.keys():
                return self.interfaces[ifIndex]
        return val


    # Update packet matches
    def update(self, signum, frame):
        self.mib.rmon_filter.filtro.update()
        signal.alarm(10)




# RFC 3416
# RFC 3413
# RFC 1905
# RFC 3415

#################################################################################################################
###############          Clase que procesará las peticiones de tipo GET-REQUEST          ########################
#################################################################################################################
class GetCommandResponder (cmdrsp.GetCommandResponder):

    # Función de inicialización de la clase. Se ejecutará cuando se cree la instancia de la clase
    def __init__(self, snmpEngine, snmpContext, mib):

        # Se ejecuta la función de inicialización de la clase que estamos extendiendo
        cmdrsp.CommandResponderBase.__init__(self,snmpEngine,snmpContext)

        # Creamos las variables pduType y mib, y las asignamos como globales para tener acceso en toda la clase
        self.pduType = ( rfc1905.GetRequestPDU.tagSet, )
        self.mib = mib

    # Función que se encargara de procesar las peticiones. Esta función es llamada cada vez que llegue una petición
    def handleMgmtOperation(self, snmpEngine, stateReference, contextName, PDU, acInfo):


        # Extraemos las variable binding del paquete
        varBinds = v2c.apiPDU.getVarBinds(PDU)
        # Creamos un paquete de repuesta vacio que iremos completando.
        varBindsRsp = []

        # Inicializamos por defecto los campos errorStatus y errorIndex a 0
        errorStatus = 0
        errorIndex = 0

        # Comenzamos el procesado de las variable binding
        for varBind in varBinds:

            # Extraemos el Object Identifier por el que nos estan preguntando
            oid_o = str(varBind[0])

            # Check if the request have permissions
            verifyAccess = acInfo[0]
            acCtx = acInfo[1]
            try:
                access = verifyAccess(v2c.ObjectIdentifier(oid_o), None, 0, 'read', acCtx)

            except AuthorizationError:
                # El varBind de respuesta sera el mismo que el de la peticion
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 16
                break

            except GenError:
                # El varBind de respuesta sera el mismo que el de la peticion
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 5
                break

            # Process the OID
            try:
                # En el caso de que se haya producido un error "notInView", añadimos en el campo value del varBind correspondiente
                # "noSuchObject"
                if access == 1:
                    # En el caso de que si se haya producido el error "notInView"
                    result = [oid_o, '', 'noSuchObject']

                # En el caso de que no se haya producido ningun error, comenzamos a procesar el paquete.
                else:
                    # result = [oid, value, type] de respuesta
                    result = self.mib.get(oid_o)

                # Añadimos la repuesta al varBind con el formato oportuno
                varBindsRsp = formato(varBindsRsp, result)

            # Si falla cualquier otra cosa se envia "genErr"
            except:
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 5
                errorIndex = 0
                break


        # Intentamos enviar el paquete de respuesta
        try:

            # Envío de la respuesta
            self.sendRsp(
                snmpEngine, stateReference,  errorStatus,
                errorIndex, varBindsRsp
            )

        # Si falla el envio habiendo funcionado lo anterio, asumimos que el error sera que el paquete excede el tamaño permitido
        except:

            # Ponemos le campo varBind vacio e introducimos el codigo de error "tooBig"
            varBindsRsp = []
            errorStatus = 1

            # Tratamos de enviar la peticion de nuevo
            try:

                self.sendRsp(
                    snmpEngine, stateReference,  errorStatus,
                    errorIndex, varBindsRsp
                )

            # en el caso de que vuelva a fallar incrementaremos el contador "snmpSilentDrops"
            except:
                snmpSilentDrops(self)



#################################################################################################################
#############          Clase que procesará las peticiones de tipo GETNEXT-REQUEST          ######################
#################################################################################################################
class NextCommandResponder (cmdrsp.NextCommandResponder):

    # Función de inicialización de la clase. Se ejecutará cuando se cree la instancia de la clase
    def __init__(self, snmpEngine, snmpContext, mib):
        # Se ejecuta la función de inicialización de la clase que estamos extendiendo
        cmdrsp.CommandResponderBase.__init__(self,snmpEngine,snmpContext)

        # Creamos las variables pduType y mib, y las asignamos como globales para tener acceso en toda la clase
        self.pduType = ( rfc1905.GetNextRequestPDU.tagSet, )
        self.mib = mib

    # Función que se encargara de procesar las peticiones. Esta función es llamada cada vez que llegue una petición
    def handleMgmtOperation(self, snmpEngine, stateReference, contextName, PDU, acInfo):


        # Extraemos las variable binding del paquete
        varBinds = v2c.apiPDU.getVarBinds(PDU)
        # Creamos un paquete de repuesta vacio que iremos completando.
        varBindsRsp = []

        # Inicializamos por defecto los campos errorStatus y errorIndex a 0
        errorStatus = 0
        errorIndex = 0

        # Comenzamos el procesado de las variable binding
        for varBind in varBinds:

            # Extraemos el Object Identifier por el que nos estan preguntando
            oid_o = str(varBind[0])

            # Inicializamos la variable result para ser coherentes con la estructura del bucle
            result = [oid_o, ' ', ' ']

            # Check if the request have permissions
            verifyAccess = acInfo[0]
            acCtx = acInfo[1]
            try:
                access = verifyAccess(v2c.ObjectIdentifier(oid_o), None, 0, 'read', acCtx)

            except AuthorizationError:
                # El varBind de respuesta sera el mismo que el de la peticion
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 16
                break

            except GenError:
                # El varBind de respuesta sera el mismo que el de la peticion
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 5
                break

            try:

                # Inicializamos access = 1 (No hay permisos), para forzar que entre al bucle al menos la primera vez
                access = 1
                # Mientras sigan quedando variables en la MIB, y la variable actual no tenga permisos de lectura seguimos buscando
                while (access == 1) and (result[2] != 'endOfMibView'):

                    # result = [oid, value, type] de respuesta
                    result = self.mib.getnext(result[0])

                    # En el caso de que el error sea "notInView" la función devolverá 1 y seguiremos iterando
                    access = verifyAccess(v2c.ObjectIdentifier(result[0]), None, 0, 'read', acCtx)

                # Si hay endOfMibView el oid sera el mismo que en la peticion
                if result[2] == 'endOfMibView':
                    result[0] = oid_o

                formato(varBindsRsp, result)


            # En el caso de que se genere un "genErr"
            except:
                # El varBind de respuesta sera el mismo que el de la peticion
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 5
                errorIndex = 0


        # Intentamos enviar el paquete de respuesta
        try:

            # Envío de la respuesta
            self.sendRsp(
                snmpEngine, stateReference,  errorStatus,
                errorIndex, varBindsRsp
            )

        # Si falla el envio habiendo funcionado lo anterio, asumiremos que el error sera que el paquete excede el tamaño permitido
        except:
            # Ponemos le campo varBind vacio e introducimos el codigo de error "tooBig"
            varBindsRsp = []
            errorStatus = 1

            # Tratamos de enviar la peticion de nuevo
            try:

                self.sendRsp(
                    snmpEngine, stateReference,  errorStatus,
                    errorIndex, varBindsRsp
                )

            # En el caso de que vuelva a fallar incrementaremos el contador "snmpSilentDrops"
            except:
                snmpSilentDrops(self)



#################################################################################################################
###############          Clase que procesará las peticiones de tipo SET-REQUEST          ########################
#################################################################################################################
class SetCommandResponder (cmdrsp.SetCommandResponder):

    # Función de inicialización de la clase. Se ejecutará cuando se cree la instancia de la clase
    def __init__(self, snmpEngine, snmpContext, mib):

        # Se ejecuta la función de inicialización de la clase que estamos extendiendo
        cmdrsp.CommandResponderBase.__init__(self,snmpEngine,snmpContext)

        # Creamos las variables pduType y mib, y las asignamos como globales para tener acceso en toda la clase
        self.pduType = ( rfc1905.SetRequestPDU.tagSet, )
        self.mib = mib

    # Función que se encargara de procesar las peticiones. Esta función es llamada cada vez que llegue una petición
    def handleMgmtOperation(self, snmpEngine, stateReference, contextName, PDU, acInfo):

        # initialize variable for backups
        almacen = []

        # Extraemos las variable binding del paquete
        varBinds = v2c.apiPDU.getVarBinds(PDU)

        # Creamos un paquete de repuesta que va a ser igual que el de pregunta.
        varBindsRsp = varBinds

        # Creamos un indice para poder indentificar la variable que ha generado un error y poder añadirlo como errorIndex
        index = 0

        # Inicializamos por defecto los campos errorStatus y errorIndex a 0
        errorStatus = 0
        errorIndex = 0

        # Comenzamos el procesado de las variable binding
        for varBind in varBinds:

            # Incrementamos el valor del indice que identificara el paquete que ha generado un error
            index = index + 1

            # Extraemos el Object Identifier, el valor y de que tipo es el valor
            oid_o = str(varBind[0])
            value = varBind[1]
            type = str(varBind).split(' ')[1]
            type = type.split('(')[0]

            # Inicializamos la variable result
            result = [' ', ' ', ' ']

            # Check if the request have permissions
            verifyAccess = acInfo[0]
            acCtx = acInfo[1]
            try:
                access = verifyAccess(v2c.ObjectIdentifier(oid_o), None, 0, 'write', acCtx)

            except AuthorizationError:
                # El varBind de respuesta sera el mismo que el de la peticion
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 16
                break

            except GenError:
                # El varBind de respuesta sera el mismo que el de la peticion
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 5
                break

            try:

                 # En el caso de que si se haya producido el error "notInView"
                if access == 1:
                    errorStatus = 6
                    errorIndex = index

                    try:
                        self.mib.rollback(almacen)
                        break
                    except:
                        result[2] = "undoFailed"


                # En el caso de que no se haya producido ningun error
                else:

                    # result = [oid, value, type] de respuesta
                    almacen = self.mib.backup(oid_o,  almacen)
                    result = self.mib.set(oid_o, value, type)

                    # Error "notWritable"
                    if result[2] == 'notWritable':
                        errorStatus = 17
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                    # Error "wrongType"
                    elif result[2] == 'wrongType':
                        errorStatus = 7
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                    # Error "wrongLength"
                    elif result[2] == 'wrongLength':
                        errorStatus = 8
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                    # Error "wrongEncoding"
                    elif result[2] == 'wrongEncoding':
                        errorStatus = 9
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                    # Error "wrongValue"
                    elif result[2] == 'wrongValue':
                        errorStatus = 10
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                    # Error "noCreation"
                    elif result[2] == 'noCreation':
                        errorStatus = 11
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                    # Error "inconsistentName"
                    elif result[2] == 'inconsistentName':
                        errorStatus = 18
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                    # Error "inconsistentValue"
                    elif result[2] == 'inconsistentValue':
                        errorStatus = 12
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"


                    elif result[2] == 'resourceUnavailable':
                        errorStatus = 13
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                    # Error "comitFailed"
                    elif result[2] == 'comitFailed':
                        errorStatus = 14
                        errorIndex = index

                        try:
                            self.mib.rollback(almacen)
                            break
                        except:
                            result[2] = "undoFailed"

                # Error "undoFailed"
                if result[2] == 'undoFailed':
                    errorIndex = 0
                    errorStatus = 15
                    break


            # En el caso de que se genere un "genErr"
            except:
                # El varBind de respuesta sera el mismo que el de la peticion
                varBindsRsp = v2c.apiPDU.getVarBinds(PDU)
                errorStatus = 5
                errorIndex = 0

                try:
                    self.mib.rollback(almacen)
                except:
                    errorStatus = 15

        # Intentamos enviar el paquete de respuesta
        try:

            # Envío de la respuesta
            self.sendRsp(
                snmpEngine, stateReference,  errorStatus,
                errorIndex, varBindsRsp
            )

        # Si falla el envio habiendo funcionado lo anterio, asumiremos que el error sera que el paquete excede el tamaño permitido
        except:
            # Ponemos le campo varBind vacio e introducimos el codigo de error "tooBig"
            varBindsRsp = []
            errorStatus = 1

            # Tratamos de enviar la peticion de nuevo
            try:

                self.sendRsp(
                    snmpEngine, stateReference,  errorStatus,
                    errorIndex, varBindsRsp
                )

            # En el caso de que vuelva a fallar incrementaremos el contador "snmpSilentDrops"
            except:
                snmpSilentDrops(self)



local_agent_v3 = agent_v3("config.json")

