# -*- coding: utf-8 -*-
# Importamos todo lo necesario
import MySQLdb
import tools.tools


class comunidades:

    def __init__(self, BBDD):
        self.BBDD = BBDD

        
    def get(self, oid):   
        # Definimos las variables necesarias
        suboid = str(oid).split('.')
        type1_resp = "ObjectName"
        type2_resp = ""
        oid_resp = oid
        val_resp = "" 
        exito_resp = 1          # exito_resp indica si hemos podido encontrar el OID solicitado en la base de datos: 1 = true; 0 = false

        if (len(suboid) == 9)  or (len(suboid) > 11):
            # Si que es de mi arbol, asi que curso la peticion
            db_comunidades=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="comunidades")
            db_comunidades.autocommit(True)
            cursor = db_comunidades.cursor()

            cursor.execute("SELECT next_table, value FROM ts_comunidades WHERE orden = %s", (suboid[7],) )
            result = cursor.fetchone()
            if str(result) != "None":
                next_table = result[0]
                value = result[1]

                if str(next_table) == 'nextTable':
                    val_resp = value
                else:
                    # Construimos la pKey y la sKey
                    cname = []
                    pKey = suboid[10:len(suboid)-1]
                    for i in pKey:
                        cname.append(chr(int(i)))
                    cname = ''.join(cname)
                    sKey = suboid[len(suboid)-1]
                    pKey = '.'.join(pKey)
                    
                    cursor.execute("SELECT name, next_table, indices, type_value, access FROM " + next_table + " WHERE orden = %s", (suboid[9],) )
                    result = cursor.fetchone()
                    if str(result) != "None":
                        name = result[0]
                        next_table = result[1]
                        indice = result[2]
                        type2_resp = result[3]
                        access = result[4]
                            
                        if (access == 1) or (access == 3): 
                            cursor.execute("SELECT " + name + " FROM " + next_table + " WHERE communityIndex = %s and id = %s", (pKey,sKey,) )
                            result = cursor.fetchone()
                            if str(result) != "None":
                                val_resp = result[0]
                            else:
                                exito_resp = 0

                        else:
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
    ###########                                                GET NEXT                                           ###############
    #############################################################################################################################


    def getnext(self, oid):
        # Definimos las variables necesarias
        suboid = str(oid).split('.')
        type1_resp = "ObjectName"
        type2_resp = ""
        oid_resp = oid
        val_resp = ""
        exito_resp = 1           # exito_resp indica si hemos podido encontrar el OID solicitado en la base de datos: 1 = true; 0 = false

        # Si el oid es menor que nuestra raid
        if rmon.tools.menor_que(oid, '1.3.6.1.4.1.28308.1.0'):
            oid_resp = "1.3.6.1.4.1.28308.1.0"
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(oid_resp)

        else:
            if rmon.tools.menor_que(oid, '1.3.6.1.4.1.28308.2'):
                suboid = ['1','3','6','1','4','1','28308','2']
            
            # Si falta alguna parte del oid la completamos de forma coherente para que sea el siguiente
            if len(suboid) < 10:
                suboid = suboid + ['1']
                suboid = suboid + ['1']

            if len(suboid) < 11:
                suboid = suboid + ['0']

            if len(suboid) < 12:
                suboid = suboid + ['0']

            # Conexion a la base de datos
            db_comunidades=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="comunidades")
            db_comunidades.autocommit(True)
            cursor = db_comunidades.cursor()

            # Si que es de mi arbol, asi que curso la peticion
            while (oid_resp == oid) and (suboid != ['1','3','6','1','4','1','28309','0','0']):
                # Construimos la pKey y la sKey
                cname = []
                pKey = suboid[10:len(suboid)-1]
                for i in pKey:
                    cname.append(chr(int(i)))
                cname = ''.join(cname)
                sKey = suboid[len(suboid)-1]
                pKey = '.'.join(pKey)

                cursor.execute("SELECT next_table FROM ts_comunidades WHERE orden = %s", (suboid[7],) )
                result = cursor.fetchone()
                if str(result) != "None":
                    tc_table = result[0]

                    cursor.execute("SELECT next_table, indices FROM " + tc_table + " WHERE orden = %s", (suboid[9],) )
                    result = cursor.fetchone()
                    if str(result) != "None":
                        td_table = result[0]
                        indice = result[1]

                        cursor.execute("SELECT communityIndex, id FROM " + td_table + " WHERE communityName = %s and id > %s ORDER BY communityName ASC, id ASC", (cname,sKey,) )
                        result = cursor.fetchone()

                        if str(result) != "None":
                            suboid_resp = suboid[0:10] +  result[0].split('.') + [ str(int(result[1])) ]
                            oid_resp = '.'.join(suboid_resp)

                        else:
                            cursor.execute("SELECT communityIndex, id FROM " + td_table + " WHERE communityName > %s ORDER BY communityName ASC, id ASC", (cname,) )
                            result = cursor.fetchone()

                            if str(result) != "None":
                                suboid_resp = suboid[0:10] +  result[0].split('.') + [ str(int(result[1])) ]
                                oid_resp = '.'.join(suboid_resp)

                            else:
                                cursor.execute("SELECT next_oid FROM " + tc_table + " WHERE orden = %s", (suboid[9],) )
                                result = cursor.fetchone()

                                if str(result) != "None":
                                    suboid = str(result[0]).split('.') + ['0','0']


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

        # Si la longitud de la vista es 1 devuelvo error
        if len(suboid) > 9:
            if suboid[9] == '5':
                subval = str(val).split('.')
                if subval[0] == "":
                    subval = subval[1:len(suboid)]
                if len(subval) == 1:
                    exito_resp = 0

        if ((len(suboid) == 9)  or (len(suboid) > 11)) and exito_resp == 1:       
            # Si que es de mi arbol, asi que curso la peticion // !!En cada consulta capturar errores(not exist)  
            db_comunidades=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="comunidades")
            db_comunidades.autocommit(True)
            cursor = db_comunidades.cursor()
            
            cursor.execute("SELECT next_table FROM ts_comunidades WHERE orden = %s", (suboid[7],) )
            result = cursor.fetchone()
            if str(result) != "None":
                next_table = result[0]

                if str(next_table) == 'nextTable':
                    print("Escribo en master")
                    cursor.execute("UPDATE ts_comunidades SET value = \'" + str(val) + "\' WHERE orden = %s", (suboid[7],) )
                else:             
                    cursor.execute("SELECT name, next_table, indices, type_value, access FROM " + next_table + " WHERE orden = %s", (suboid[9],) )
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

                        # Construimos la pKey y la sKey
                        cname = []
                        pKey = suboid[10:len(suboid)-1]
                        for i in pKey:
                            cname.append(chr(int(i)))
                        cname = ''.join(cname)
                        sKey = suboid[len(suboid)-1]
                        pKey = '.'.join(pKey)
                           
                        # Verificamos que tenemos permisos de escritura
                        if access > 1:
                            # Miramos el valor del entryStatus para la instancia solicitada
                            cursor.execute("SELECT " + status_name  + " FROM " + next_table + " WHERE communityIndex = %s and id = %s", (pKey,sKey,) )
                            aux = cursor.fetchone()

                            # Si no existe
                            if str(aux) == "None":
                                # Estoy escribiendo en el campo EntryStatus
                                if name == status_name:
                                    # Si el gestor envia un 2, creo la fila y escribo un 3 (UnderCreation)
                                    if str(val) == "2":
                                        print("inserto un 3")
                                        cursor.execute("INSERT INTO " + next_table + "(communityIndex, communityName, id)" + " VALUES (\'" + str(pKey) + "\',\'" + str(cname) + "\'," + str(sKey) + ")" )
                                        cursor.execute("UPDATE " + next_table + " SET " + name + " = 3 WHERE communityIndex = %s and id = %s", (pKey,sKey,) )
                                    # Si no es un 2, error
                                    else:
                                        print("error")
                                        exito_resp = 0
                                # Si no es el campo EntryStatus, error
                                else:
                                    print("error")
                                    exito_resp = 0
                            # Si existe, cogemos el valor y consideramos los diferentes casos
                            else:
                                status_val = aux[0]
                                    
                                if str(status_val) == "1":
                                    if name == status_name:
                                        # Si el gestor envia un 1, no necesito hacer nada
                                        if val == 1:
                                            print("No hago nada")
                                        # Si el gestor envia un 3, lo escribo
                                        elif val == 3:
                                            print("Escribo un 3")
                                            cursor.execute("UPDATE " + next_table + " SET " + name + " = 3 WHERE communityIndex = %s and id = %s", (pKey,sKey,) )
                                        # Si el gestor envia un 4, borro la entrada
                                        elif val == 4:
                                            print("Borro la entrada")
                                            cursor.execute("DELETE FROM " + next_table + " WHERE communityIndex = %s and id = %s", (pKey,sKey,) )
                                        # Si no es ninguno de los anteriores, error
                                        else:
                                            print("error")
                                            exito_resp = 0
                                    # Si no es el campo EntryStatus, error
                                    else:
                                        print("error")

                                elif str(status_val) == "3":
                                    if name == status_name:
                                        # Si el gestor envia un 1, lo escribo y ejecuto el programa de captura
                                        if val == 1:
                                            print("Escribo un 1 y ejecuto el programa captura")
                                            cursor.execute("UPDATE " + next_table + " SET " + name + " = 1 WHERE communityIndex = %s and id = %s", (pKey,sKey,) )
                                        # Si el gestor envia un 3, no necesito hacer nada
                                        elif val == 3:
                                            print("No hago nada")
                                        # Si el gestor envia un 4, borro la entrada
                                        elif val == 4:
                                            print("Borro la entrada")
                                            cursor.execute("DELETE FROM " + next_table + " WHERE communityIndex = %s and id = %s", (pKey,sKey,) )
                                        # Si no es ninguno de los anteriores, error
                                        else:
                                            print("error")
                                            exito_resp = 0 
                                    # Si no es el campo EntryStatus, lo escribo
                                    else:
                                        # !!!!!!!!!!! CUIDADO CON EL TIPO DE DATOS QUE INTRODUCZCO 
                                        if rmon.tools.isType(val, type2_resp):
                                            print("escribo el valor recibido")
                                            cursor.execute("UPDATE " + next_table + " SET " + name + " = \'" + str(val) + "\' WHERE communityIndex = %s and id = %s", (pKey,sKey,) )
                                        else:
                                            print("El tipo introducido no coincide con el de la mib")
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
        




    def permiso(self, comunidad, oid):
        permisos = 0
        coincidencias = 0
        suboid = str(oid).split('.')

        if suboid[0] == "":
            suboid = suboid[1:len(suboid)]

        # Si que es de mi arbol, asi que curso la peticion // !!En cada consulta capturar errores(not exist)
        # Conexion a la base de datos
        db_comunidades=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="comunidades")
        db_comunidades.autocommit(True)
        cursor = db_comunidades.cursor()

        cursor.execute("SELECT value FROM ts_comunidades WHERE orden = 1" )
        result = cursor.fetchone()
        master = result[0]
        if (str(comunidad) == master) and (suboid[0:7] == ['1', '3', '6', '1', '4', '1', '28308']):
            permisos = 3

        else:          
            cursor.execute("SELECT * FROM td_communityManagement WHERE communityName = %s and communityStatus = 1", (comunidad,) )
            result = cursor.fetchall()
            if str(result) != "None":
                for entrada in result:

                    permisos_entrada = int(entrada[3])
                    oid_entrada = str(entrada[4])
                    suboid_entrada = oid_entrada.split('.')

                    if suboid_entrada[0] == "":
                           suboid_entrada = suboid_entrada[1:len(suboid_entrada)]

                    if suboid_entrada == suboid[0:len(suboid_entrada)]:
                        if len(suboid_entrada) > coincidencias:
                            coincidencias = len(suboid_entrada)
                            permisos = permisos_entrada

        return permisos  

