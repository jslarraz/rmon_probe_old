from pysnmp.proto import api


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

class SNMP_proxy:
    def __init__(self, ADDR, COMMUNITY):
        self.ADDR = ADDR
        self.COMMUNITY = COMMUNITY


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


