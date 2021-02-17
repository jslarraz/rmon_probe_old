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




# Función encargada de verificar si un determinado usuario tiene permisos para leer o escribir un determinado OID
# def verifyAccess(self, name, syntax, idx, viewType, acCtx):
#     (snmpEngine, securityModel, securityName, securityLevel,
#     contextName, pduType) = acCtx
#
#     # Llamamos a la función que controla los permisos
#     try:
#         statusInformation = snmpEngine.accessControlModel[self.acmID].isAccessAllowed(
#         snmpEngine, securityModel, securityName,
#         securityLevel, viewType, contextName, name
#         )
#
#     # Map ACM errors onto SMI ones
#     except error.StatusInformation, statusInformation:
#         errorIndication = statusInformation['errorIndication']
#
#         # En el caso de que se haya producido un error de tipo "noSuchView", "noAccessEntry" o "noGroupName", devolveremos
#         # "authorizationError" para tratarlo en la case superior
#         if errorIndication == errind.noSuchView or \
#         errorIndication == errind.noAccessEntry or \
#         errorIndication == errind.noGroupName:
#            return "authorizationError"
#
#         # En el caso de que devuelva "otherError", enviamos un mensaje "genErr"
#         elif errorIndication == errind.otherError:
#             raise pysnmp.smi.error.GenError(name=name, idx=idx)
#
#         # En el caso de qeu no exista el contexto, enviaremos "genErr"
#         elif errorIndication == errind.noSuchContext:
#             snmpUnknownContexts, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('__SNMP-TARGET-MIB', 'snmpUnknownContexts')
#             snmpUnknownContexts.syntax = snmpUnknownContexts.syntax + 1
#             # Request REPORT generation
#             raise pysnmp.smi.error.GenError(
#             name=name, idx=idx,
#             oid=snmpUnknownContexts.name,
#             val=snmpUnknownContexts.syntax
#             )
#
#         # En el caso de que si se haya producido el error "notInView",devolveremos "noAccess" para tratarlo en la case superior
#         elif errorIndication == errind.notInView:
#             return "noAccess"
#
#         else:
#             raise error.ProtocolError(
#             'Unknown ACM error %s' % errorIndication
#             )
#
#     # En el caso de que no se haya producido ningun error
#     else:
#         # En el caso de que la peticion sea snmp V1 y nos pidan un counter64 en un getNext devolveremos "noAccess" rfc2576: 4.1.2.1
#         if securityModel == 1 and \
#         syntax is not None and \
#         self._counter64Type == syntax.getTagSet() and \
#         self._getNextRequestType == pduType:
#             # This will cause MibTree to skip this OID-value
#             return "noAccess"
#
#         # En cualquier otro cosa devolveremos un 0 en señal de que si que hay permisos
#         else:
#             return 0


    # def __verifyAccess(self, name, syntax, idx, viewType, acCtx):
    #     snmpEngine = acCtx
    #     execCtx = snmpEngine.observer.getExecutionContext('rfc3412.receiveMessage:request')
    #     (securityModel, securityName, securityLevel, contextName,
    #      pduType) = (execCtx['securityModel'], execCtx['securityName'],
    #                  execCtx['securityLevel'], execCtx['contextName'],
    #                  execCtx['pdu'].getTagSet())
    #     try:
    #         snmpEngine.accessControlModel[self.acmID].isAccessAllowed(
    #             snmpEngine, securityModel, securityName,
    #             securityLevel, viewType, contextName, name
    #         )
    #     # Map ACM errors onto SMI ones
    #     except error.StatusInformation:
    #         statusInformation = sys.exc_info()[1]
    #         debug.logger & debug.flagApp and debug.logger(
    #             '__verifyAccess: name %s, statusInformation %s' % (name, statusInformation))
    #         errorIndication = statusInformation['errorIndication']
    #         # 3.2.5...
    #         if (errorIndication == errind.noSuchView or
    #                 errorIndication == errind.noAccessEntry or
    #                 errorIndication == errind.noGroupName):
    #             raise pysnmp.smi.error.AuthorizationError(name=name, idx=idx)
    #         elif errorIndication == errind.otherError:
    #             raise pysnmp.smi.error.GenError(name=name, idx=idx)
    #         elif errorIndication == errind.noSuchContext:
    #             snmpUnknownContexts, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols(
    #                 '__SNMP-TARGET-MIB', 'snmpUnknownContexts')
    #             snmpUnknownContexts.syntax += 1
    #             # Request REPORT generation
    #             raise pysnmp.smi.error.GenError(name=name, idx=idx,
    #                                             oid=snmpUnknownContexts.name,
    #                                             val=snmpUnknownContexts.syntax)
    #         elif errorIndication == errind.notInView:
    #             return 1
    #         else:
    #             raise error.ProtocolError('Unknown ACM error %s' % errorIndication)
    #     else:
    #         # rfc2576: 4.1.2.1
    #         if (securityModel == 1 and syntax is not None and
    #                 self._counter64Type == syntax.getTagSet() and
    #                 self._getNextRequestType == pduType):
    #             # This will cause MibTree to skip this OID-value
    #             raise pysnmp.smi.error.NoAccessError(name=name, idx=idx)





def set_snmp(self,oid_o, value, type):
    # Necesito que devuelva un OID, un valor, un tipo de datos y los errores

    # En un set, el OID que devuelvo es el mismo que por el que pregunto
    oid_s = oid_o

    # Necesito que devuelva un OID, un valor, un tipo de datos y los errores

    # En el caso de que el primer caracter no sea un punto, se lo añadimos
    if oid_o[0] != '.':
        oid_o = '.' + oid_o


    # Comprobamos si existe su nodo padre
    suboid = oid_o.split('.')
    oid_aux = 'o'.join(suboid[:len(suboid)-1])
    find_oid_get = ET.XPath("//"+oid_aux)
    node_O = find_oid_get(self.mib)

    try:
        node_X = node_O[0]

    except:
        # Este nodo no esta en nuestra MIB, devolvemos "notWritable", corresponde con el caso 2 (No existe ninguna variable
        # en nuestra mib que tenga el mismo profijo que el oid por el que preguntamos (entendiendo por prefijo el OID sin
        # .0 o .index) y que pueda ser creada o modificada.
        value = 'notWritable'
        type_v = 'notWritable'

    else:
        # Compruebo que sus hijos sean instancias, en nuestro caso name!=""
        name = node_X.get('NAME')
        if name != "":
            # En este caso el OID por el que nos preguntan será una instancia
            find_descendant = ET.XPath('descendant::*[@SYNTAX!="none" and @MAX-ACCESS!="not-accessible"]')
            node_d = find_descendant(node_X)

            # Seleccionamos una instancia cualquiera que comparta prefijo con la variable que nos han pedido.
            try:
                node_X = node_d[0]

            except:
                # Aqui. en el caso de que no exista ninguna instancia, deberiamos comparar entre "notWritable" y "noCreation",
                # En nuestro agente no se va a dar nunca este caso, ya que tanto la tabla como los objetos escalares aparecin
                # inicializados por defecto,
                value = 'notWritable'
                type_v = 'notWritable'

            else:
                # Todas las instancias que comparten prefijo, tambien comparten la sintaxis y el max-access
                type_v = node_X.get('SYNTAX')
                access = node_X.get('MAX-ACCESS')

                # Si el nivel de acceso no es "read-write", devolveremos "notWritable, caso 2
                if access != 'read-write':
                    value = 'notWritable'
                    type_v = 'notWritable'

                # Si la variable es de lectura y escritura
                else:

                    # Comprobamos si la sintaxis es correcta
                    if not(((type_v == "OCTET-STRING") and (type == "OctetString")) or  ((type_v == "INTEGER") and (type == "Integer"))):
                        # La sintaxis no es correcta, enviamos wrongType, caso 3
                        value = 'wrongType'
                        type_v = 'wrongType'


                    else:
                        # La sintaxis es correcta, seguimos procesando
                        # En los octec-string comprobamos si la longitud es valida
                        if type_v == "OCTET-STRING":
                            min = int(node_X.get('MIN-LENGTH'))
                            max = int(node_X.get('MAX-LENGTH'))

                            if not((min <= len(value)) and (max >= len(value))):
                                # No cumple con la longitud, devolvemos wrongLength, caso 4
                                value = 'wrongLength'
                                type_v = 'wrongLength'
                                return [oid_s, value, type_v]

                        # En los enteros comprovamos que es el rango
                        elif type_v == "INTEGER":
                            min = int(node_X.get('MIN-VALUE'))
                            max = int(node_X.get('MAX-VALUE'))
                            if not((min <= int(value)) and (max >= int(value))):
                                # No esta dento del rango, devolvemos wrongValue, caso 6
                                value = 'wrongValue'
                                type_v = 'wrongValue'
                                return [oid_s, value, type_v]

                        # Comprobamos si el OID por el que nos pregunta existe o podria existir
                        for node_X in node_d:
                            oid_aux = node_X.tag.replace('o','.')[0:]
                            if oid_o == oid_aux:
                                # En el caso de que si que exista, intentamos asignarle el valor
                                try:
                                    node_X.text = str(value)

                                # SI no podemos, "comitFailed"
                                except:
                                    value = 'comitFailed'
                                    type_v = 'comitFailed'
                                return [oid_s, value, type_v]


                        # Si no esta entre los descendientes devolveremos "noCreation", en nuestro caso si no existe, nunca
                        # podra existir, ya que inicializamos le agente con todas la posible instancias ya creadas, caso 7
                        value = 'noCreation'
                        type_v = 'noCreation'

        else:
            # En este caso el nodo por el que me han preguntado no va a ser una instancia, es dicir sera un nodo del arbol,
            # y será "not-accessible", También corresponde con el caso 2 (No existe ninguna variable
            # en nuestra mib que tenga el mismo profijo que el oid por el que preguntamos (entendiendo por prefijo el OID sin
            # .0 o .index) y que pueda ser creada o modificada.
            value = 'notWritable'
            type_v = 'notWritable'

    return [oid_s, value, type_v]


def rollback():
    pass


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
    config.addVacmUser(self.snmpEngine, 1, 'my-read-area', 'noAuthNoPriv', (1, 3, 6, 1, 2, 1))
    config.addVacmUser(self.snmpEngine, 1, 'my-write-area', 'noAuthNoPriv', (1, 3, 6, 1, 2, 1), (1, 3, 6, 1, 2, 1))
    ###