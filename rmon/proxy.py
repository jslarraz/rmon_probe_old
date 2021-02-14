import tools
import subprocess
from pysnmp.proto import api

class proxy:

    def __init__(self, comunidades):
        self.comunidades = comunidades

    def procesa_resp(self, aux):
        aux = aux.split(":")
        aux1 = aux[0]
        aux2 = aux[1]
        aux1 = aux1.split(" ")
        oid_resp = aux1[0]
        suboid_resp = oid_resp.split(".")
        if suboid_resp[0] == "":
            suboid_resp = suboid_resp[1:len(suboid_resp)]
            oid_resp = '.'.join(suboid_resp)
        type2_resp = aux1[2]
        if type2_resp == "STRING":
            aux2 = aux2.split("\"")
            val_resp = aux2[1]
        else:
            aux2 = aux2.split(" ")
            aux2 = aux2[1]
            aux2 = aux2.split("\n")
            val_resp = aux2[0]
        return oid_resp, type2_resp, val_resp


    #############################################################################################################################
    ###########                                                GET                                                ###############
    #############################################################################################################################

    def get(self, oid):
        oid_resp = oid
        val_resp = api.v1.Null('')
        type1_resp = "OID"
        type2_resp = ""
        exito_resp = 1

        try:
            aux = subprocess.check_output(["snmpget", "-v", "1", "-c", "public", "-Oben", "localhost:162", str(oid)])
            oid_resp, type2_resp, val_resp = self.procesa_resp(aux)

        except:
            exito_resp = 0
        
        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp


    #############################################################################################################################
    ###########                                              GET NEXT                                             ###############
    #############################################################################################################################


    def getnext(self, oid, comunidad):   
        oid_resp = oid
        val_resp = api.v1.Null('')
        type1_resp = "OID"
        type2_resp = ""
        exito_resp = 1
        permisos = 0

        while ((permisos != 1) and (permisos != 3)) and exito_resp == 1:
            try:
                aux = subprocess.check_output(["snmpgetnext", "-v", "1", "-c", "public", "-Oben", "localhost:162", str(oid_resp)])
                oid_resp, type2_resp, val_resp = self.procesa_resp(aux)

            except:
                exito_resp = 0

            permisos = self.comunidades.permiso(comunidad, oid_resp)

        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp



    #############################################################################################################################
    ###########                                                SET                                                ###############
    #############################################################################################################################


    def set(self, oid, val):
        oid_resp = oid
        val_resp = val
        type1_resp = "OID"
        type2_resp = ""
        exito_resp = 1

        try:
            aux = subprocess.check_output(["snmpset", "-v", "1", "-c", "public", "-Oben", "localhost:162", str(oid)])
            oid_resp, type2_resp, val_resp = self.procesa_resp(aux)

        except:
            exito_resp = 0

        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp


        

    #############################################################################################################################
    ###########                                              BACKUP                                               ###############
    #############################################################################################################################

    def backup(self, oid, triple):
        suboid = str(oid).split('.')
        doble = []
        uni = []
        # Escalar
        if suboid[len(suboid)-1] == '0':
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(oid)
            uni.append(oid)
            uni.append(val_resp)
            doble.append(uni)

        # Tabla
        else:
            indice = 1
            suboid[len(suboid)-2] = str(indice)
            oid_temp = '.'.join(suboid)
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(str(oid_temp))
            while exito_resp != 0:
                uni.append(oid_temp)
                uni.append(val_resp)
                doble.append(uni)
                uni = []
                indice = indice + 1
                suboid[len(suboid)-2] = str(indice)
                oid_temp = '.'.join(suboid)
                exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(str(oid_temp))

            uni = []
            if len(doble) > 0:
                uni.append(doble[len(doble)-1][0])
                uni.append('2')
            else:
                uni.append(oid)
                uni.append('4')

            doble.insert(0,uni)

        triple.append(doble)

        return triple

    #############################################################################################################################
    ###########                                              ROLLBACK                                               ###############
    #############################################################################################################################


    def rollback(self, doble):
        for i in range(len(doble)):
            set(str(doble[i][0]),str(doble[i][1]))
        



