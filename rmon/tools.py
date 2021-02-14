from pysnmp.proto import api
import MySQLdb
import subprocess
import os
import signal

def mayor_que(oid1, oid2):
    resultado = 0
    suboid1 = str(oid1).split('.')
    suboid2 = str(oid2).split('.')

    for i in range(min(len(suboid1),len(suboid2))):
        if int(suboid1[i]) > int(suboid2[i]):
            resultado = 1
            break
        elif int(suboid1[i]) == int(suboid2[i]):
            if (i == len(suboid2)-1) and (len(suboid1) > len(suboid2)):
                resultado = 1
        else:
            break
        
    return resultado    
    
def menor_que(oid1, oid2):
    resultado = 0
    suboid1 = str(oid1).split('.')
    suboid2 = str(oid2).split('.')

    for i in range(min(len(suboid1),len(suboid2))):
        if int(suboid1[i]) > int(suboid2[i]):
            break
        elif int(suboid1[i]) == int(suboid2[i]):
            if (i == len(suboid1)-1) and (len(suboid1) < len(suboid2)):
                resultado = 1
        else:
            resultado = 1
            break       
        
    return resultado

def igual_que(oid1, oid2):
    resultado = 0
    if oid1 == oid2:
        resultado = 1
        
    return resultado


def formato(varBinds, oid_resp, val_resp, type2_resp, msgVer):
    if type2_resp == "INTEGER":
        varBinds.append((oid_resp, api.protoModules[msgVer].Integer(int(val_resp))))
    elif type2_resp == "TimeTicks":
        varBinds.append((oid_resp, api.protoModules[msgVer].TimeTicks(int(val_resp))))
    elif type2_resp == "Counter":
        varBinds.append((oid_resp, api.protoModules[msgVer].Counter(int(val_resp))))
    elif type2_resp == "OctetString":
        varBinds.append((oid_resp, api.protoModules[msgVer].OctetString(str(val_resp))))
    elif type2_resp == "OID":
        varBinds.append((oid_resp, api.protoModules[msgVer].ObjectIdentifier(str(val_resp))))        
    else:
        varBinds.append((oid_resp, api.protoModules[msgVer].OctetString(str(val_resp))))  

    return varBinds

class BBDD:
    def __init__(self, ADDR, USER, PASS):
        self.ADDR = ADDR
        self.USER = USER
        self.PASS = PASS

def isINTEGER(val):
    try:
        int(val)
        return True
    except:
        return False

def isTimeTicks(val):
    if isinstance(val, int):
        return True
    else:
        return False

def isCounter32(val):
    if isinstance(val, int):
        return True
    else:
        return False

def isSTRING(val):
    return True

def isOID(val):
    val = str(val)
    # Comprobamos que no acaba en '.'
    if val.split('.')[len(val.split('.'))-1] != "":
        # Comprobamos que tiene al menos dos "suboid"
        if (val.split('.')[0] != "" and len(val.split('.')) > 1 ) or (len(val.split('.')) > 2):
            return True
        else:
            return False
    else:
        return False


def isType(val, tipo):
    if tipo != "OctetString" and tipo != "OID":
        return isINTEGER(val)
    elif tipo == "OID":
        return isOID(val)
    else:
        return isSTRING(val)



#
#
# def permiso(self, comunidad, oid):
#     permisos = 0
#     coincidencias = 0
#     suboid = str(oid).split('.')
#
#     # Si que es de mi arbol, asi que curso la peticion // !!En cada consulta capturar errores(not exist)
#     # Conexion a la base de datos
#     db=MySQLdb.connect(host="localhost",user="root",passwd="AquaDarknes",db="comunidades")
#     cursor = db.cursor()
#
#     cursor.execute("SELECT value FROM ts_comunidades WHERE orden = 1" )
#     result = cursor.fetchone()
#     master = result[0]
#     if (comunidad == master) and (suboid[0:7] == ['1', '3', '6', '1', '4', '1', '28308']):
#         permisos = 3
#
#     else:
#         cursor.execute("SELECT * FROM td_communityManagement WHERE communityName = %s", (comunidad,) )
#         result = cursor.fetchall()
#         if str(result) != "None":
#             for entrada in result:
#                 permisos_entrada = int(entrada[3])
#                 oid_entrada = str(entrada[4])
#                 suboid_entrada = oid_entrada.split('.')
#                 if suboid_entrada == suboid[0:len(suboid_entrada)]:
#                     if len(suboid_entrada) > coincidencias:
#                         coincidencias = len(suboid_entrada)
#                         permisos = permisos_entrada
#
#     return permisos
#
