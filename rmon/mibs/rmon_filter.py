# -*- coding: utf-8 -*-
# Importamos todo lo necesario
import MySQLdb
from tools import tools
from functional import filter



class rmon_filter:

    def __init__(self, N_FILTROS, BBDD, interfaces):
        self.filtro = filter.filter(N_FILTROS, BBDD, interfaces)
        self.filtro.start()
        self.BBDD = BBDD


    def get(self, oid):   
        # Definimos las variables necesarias
        suboid = str(oid).split('.')
        type1_resp = "ObjectName"
        type2_resp = ""
        oid_resp = oid
        val_resp = "" 
        exito_resp = 1          # exito_resp indica si hemos podido encontrar el OID solicitado en la base de datos: 1 = true; 0 = false
        
        if len(suboid) == 12:
            # Si que es de mi arbol, asi que curso la peticion
            db_rmon=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="rmon")
            db_rmon.autocommit(True)
            cursor = db_rmon.cursor()
            
            cursor.execute("SELECT next_table FROM ts_filter WHERE orden = %s", (suboid[8],) )
            result = cursor.fetchone()
            if str(result) != "None":
                next_table = result[0]

                cursor.execute("SELECT name, next_table, indices, type_value, access FROM " + next_table + " WHERE orden = %s", (suboid[10],) )
                result = cursor.fetchone()
                if str(result) != "None":
                    name = result[0]
                    next_table = result[1]
                    indice = result[2]
                    type2_resp = result[3]
                    access = result[4]
                        
                    if (access == 1) or (access == 3): 
                        cursor.execute("SELECT " + name + " FROM " + next_table + " WHERE " + indice + " = %s", (suboid[11],) )
                        result = cursor.fetchone()
                        if str(result) != "None":
                            val_resp = result[0]
                        else:
                            # No existe la instancia, devuelvo noSuchInstance
                            type2_resp = 'noSuchInstance'
                            exito_resp = 0

                    else:
                        # El tipo de acceso no coincide, (se deberia cumplir siempre)
                        type2_resp = 'genErr'
                        exito_resp = 0

                else:
                    # Alguna parte del arbol no existe, devuelvo noSuchObject
                    type2_resp = 'noSuchObject'
                    exito_resp = 0

            else:
                # Alguna parte del arbol no existe, devuelvo noSuchObject
                type2_resp = 'noSuchObject'
                exito_resp = 0
                    
        else:
            # Es de mi arbol pero falta alguna parte, devuelvo noSuchObject
            type2_resp = 'noSuchObject'
            exito_resp = 0
                

        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp





    #############################################################################################################################
    ###########                                                GET NEXT                                           ###############
    #############################################################################################################################


    def getnext(self, oid):

        # Definimos las variables necesarias
        suboid = str(oid).split('.')
        type1_resp = "ObjectName"
        type2_resp = ""
        oid_resp = oid
        val_resp = ""
        exito_resp = 1          # exito_resp indica si hemos podido encontrar el OID solicitado en la base de datos: 1 = true; 0 = false


        # Si el oid es menor que nuestra raid
        if tools.menor_que(oid, '1.3.6.1.2.1.16.7'):
            suboid = ['1','3','6','1','2','1','16','7']
        
        # Si falta alguna parte del oid la completamos de forma coherente para que sea el siguiente
        if len(suboid) < 9:
            suboid = suboid + ['1']

        if len(suboid) < 11:
            suboid = suboid + ['1']
            suboid = suboid + ['1']

        if len(suboid) < 12:
            suboid = suboid + ['0']

        # Si que es de mi arbol, asi que curso la peticion
        # Conexion a la base de datos
        db_rmon=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="rmon")
        db_rmon.autocommit(True)
        cursor = db_rmon.cursor()


        while (oid_resp == oid) and (suboid != ['1','3','6','1','2','1','16','8','1','1','1','0']):

            cursor.execute("SELECT next_table FROM ts_filter WHERE orden = %s", (suboid[8],) )
            result = cursor.fetchone()
            if str(result) != "None":
                tc_table = result[0]

                cursor.execute("SELECT next_table, indices FROM " + tc_table + " WHERE orden = %s", (suboid[10],) )
                result = cursor.fetchone()
                if str(result) != "None":
                    td_table = result[0]
                    indice = result[1]

                    cursor.execute("SELECT " + indice + " FROM " + td_table + " WHERE " + indice + " > %s ORDER BY " + indice + " ASC", (suboid[11],)  )
                    result = cursor.fetchone()

                    if str(result) != "None":
                        suboid_resp = suboid[0:11] +  [ str(int(result[0])) ]
                        oid_resp = '.'.join(suboid_resp)

                    else:
                        cursor.execute("SELECT next_oid FROM " + tc_table + " WHERE orden = %s", (suboid[10],) )
                        result = cursor.fetchone()

                        if str(result) != "None":
                            suboid = str(result[0]).split('.') + ['0']



        if oid_resp == oid:
            exito_resp = 0
        else:
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(oid_resp)


        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp





    #############################################################################################################################
    ###########                                                SET                                                ###############
    #############################################################################################################################


    def set(self, oid, val):
        # Definimos las variables necesarias
        suboid = str(oid).split('.')
        type1_resp = "ObjectName"
        type2_resp = ""
        oid_resp = oid
        val_resp = val
        exito_resp = 1          # exito_resp indica si hemos podido encontrar el OID solicitado en la base de datos: 1 = true; 0 = false
        
        if len(suboid) == 12:       
            # Si que es de mi arbol, asi que curso la peticion // !!En cada consulta capturar errores(not exist)
            # Conexion a la base de datos
            db_rmon=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="rmon")
            db_rmon.autocommit(True)
            cursor = db_rmon.cursor()
                
            cursor.execute("SELECT next_table FROM ts_filter WHERE orden = %s", (suboid[8],) )
            result = cursor.fetchone()
            if str(result) != "None":
                next_table = result[0]
                
                cursor.execute("SELECT name, next_table, indices, type_value, access FROM " + next_table + " WHERE orden = %s", (suboid[10],) )
                result = cursor.fetchone()
                if str(result) != "None":                    
                    cursor.execute("SELECT name FROM " + next_table + " WHERE orden = (SELECT MAX(orden) FROM " + next_table + ")" )
                    aux = cursor.fetchone()
                    status_name = aux[0]

                    name = result[0]
                    next_table = result[1]
                    indice = result[2]
                    type2_resp = result[3]
                    access = result[4]
                       
                    # Verificamos que tenemos permisos de escritura
                    if access > 1:
                        # Miramos el valor del entryStatus para la instancia solicitada
                        cursor.execute("SELECT " + status_name  + " FROM " + next_table + " WHERE "  + indice + " = %s", (suboid[11],) )
                        aux = cursor.fetchone()

                        # Si no existe
                        if str(aux) == "None":
                            # Estoy escribiendo en el campo EntryStatus
                            if name == status_name:
                                # Si el gestor envia un 2, creo la fila y escribo un 3 (UnderCreation)
                                if val == 2:
                                    print ("inserto un 3")
                                    cursor.execute("INSERT INTO " + next_table + "(" + indice + ")" + " VALUES (" + suboid[11] + ")" )
                                    cursor.execute("UPDATE " + next_table + " SET " + name + " = 3 WHERE " + indice + " = %s", (suboid[11],) )
                                # Si no es un 2, error
                                else:
                                    print ("error 1")
                                    exito_resp = 0
                            # Si no es el campo EntryStatus, error
                            else:
                                print ("error 2")
                                exito_resp = 0
                        # Si existe, cogemos el valor y consideramos los diferentes casos
                        else:
                            status_val = aux[0]
                                
                            if str(status_val) == "1":
                                if name == status_name:
                                    # Si el gestor envia un 1, no necesito hacer nada
                                    if val == 1:
                                        print ("No hago nada")
                                    # Si el gestor envia un 3, lo escribo
                                    elif val == 3:
                                        print ("Escribo un 3")
                                        cursor.execute("UPDATE " + next_table + " SET " + name + " = 3 WHERE " + indice + " = %s", (suboid[11],) )
                                        # Paramos el programa de filtrado
                                        if name == "channelStatus":
                                            print ("Pauso el filtro " + str(suboid[11]))
                                            self.filtro.delete(suboid[11])
                                    # Si el gestor envia un 4, borro la entrada
                                    elif val == 4:
                                        print ("Borro la entrada")
                                        cursor.execute("DELETE FROM " + next_table + " WHERE " + indice + " = %s", (suboid[11],) )
                                        # Paramos el programa de filtrado
                                        if name == "channelStatus":
                                            print ("Borro el filtro " + str(suboid[11]))
                                            self.filtro.delete(suboid[11])
                                    # Si no es ninguno de los anteriores, error
                                    else:
                                        print ("error 3")
                                        exito_resp = 0
                                # Si no es el campo EntryStatus, error
                                else:
                                    exito_resp = 0
                                    print ("error 4")

                            elif str(status_val) == "3":
                                if name == status_name:
                                    # Si el gestor envia un 1, lo escribo y ejecuto el programa de captura
                                    if val == 1:
                                        cursor.execute("UPDATE " + next_table + " SET " + name + " = 1 WHERE " + indice + " = %s", (suboid[11],) )
                                        # Ejecutamos el programa de filtrado
                                        if name == "channelStatus":
                                            print ("Lanzo el filtro " + str(suboid[11]))
                                            self.filtro.add(suboid[11])
                                    # Si el gestor envia un 3, no necesito hacer nada
                                    elif val == 3:
                                        print ("No hago nada")
                                    # Si el gestor envia un 4, borro la entrada
                                    elif val == 4:
                                        print ("Borro la entrada")
                                        cursor.execute("DELETE FROM " + next_table + " WHERE " + indice + " = %s", (suboid[11],) )
                                    # Si no es ninguno de los anteriores, error
                                    else:
                                        print ("error 5")
                                        exito_resp = 0 
                                # Si no es el campo EntryStatus, lo escribo
                                else:
                                    # !!!!!!!!!!! CUIDADO CON EL TIPO DE DATOS QUE INTRODUCZCO 
                                    if tools.isType(val, type2_resp):
                                        print ("escribo el valor recibido: " + str(val))
                                        cursor.execute("UPDATE " + next_table + " SET " + name + " = \'" + str(val) + "\' WHERE " + indice + " = %s", (suboid[11],) )
                                    else:
                                        print ("El tipo introducido no coincide con el de la mib")
                                        exito_resp = 0

                    else:
                        # No permiso de escritura
                        exito_resp = 0
                            
                else:
                    exito_resp = 0
                    
            else:
                exito_resp = 0
                
        else:
            # Es de mi arbol pero falta alguna parte
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
        if suboid[len(suboid)-1] == 0:
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
        

