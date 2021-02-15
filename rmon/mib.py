import proxy
import rmon_filter
import comunidades
import tools
import MySQLdb


class mib:

    def __init__(self, N_FILTROS, BBDD, SNMP, interfaces):
        # Creamos un cursor hacia la base de datos
        self.comunidades = comunidades.comunidades(BBDD)
        self.rmon_filter = rmon_filter.rmon_filter(N_FILTROS, BBDD, self.comunidades, interfaces)
        self.proxy = proxy.proxy(self.comunidades, SNMP)


    def get(self, oid):
        exito_resp = 0
        type1_resp = ''
        oid_resp = oid
        type2_resp = ''
        val_resp = ''

        if tools.menor_que(oid, '1.3.6.1.2.1.16.7'):
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.proxy.get(str(oid))

                
        elif tools.menor_que(oid, '1.3.6.1.2.1.16.8'):
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.rmon_filter.get(oid)
                
        #elif tools.menor_que(oid, '1.3.6.1.4.1.28309'):
        else:
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.comunidades.get(oid)
        
        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp


    def getnext(self, oid, comunidad):
        exito_resp = 0
        type1_resp = ''
        oid_resp = oid
        type2_resp = ''
        val_resp = ''

        if tools.menor_que(oid, '1.3.6.1.2.1.16.7'):
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.proxy.getnext(str(oid), comunidad)

        if tools.menor_que(oid, '1.3.6.1.2.1.16.8') and exito_resp == 0:
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.rmon_filter.getnext(oid, comunidad)

        if tools.menor_que(oid, '1.3.6.1.4.1.28309') and exito_resp == 0:
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.comunidades.getnext(oid, comunidad)

        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp





    def set(self, oid, val):
        
        if tools.menor_que(oid, '1.3.6.1.2.1.16.7'):
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.proxy.set(str(oid),val)

                
        elif tools.menor_que(oid, '1.3.6.1.2.1.16.8'):
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.rmon_filter.set(oid,val)
                
        #elif tools.menor_que(oid, '1.3.6.1.4'):
        else: 
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.comunidades.set(oid,val)    
        
        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp




    def backup(self, oid, almacen):
        
        if tools.menor_que(oid, '1.3.6.1.2.1.16.7'):
            almacen = self.proxy.backup(str(oid),almacen)

               
        elif tools.menor_que(oid, '1.3.6.1.2.1.16.8'):
            almacen = self.rmon_filter.backup(oid,almacen)
            
        #elif tools.menor_que(oid, '1.3.6.1.4'):
        else:
            almacen = self.comunidades.backup(oid,almacen)    

        return  almacen




    def rollback(self, triple):

        triple.reverse()
        for i in range(len(triple)-1):
            doble = triple[i+1]
            oid = doble[0][0]
        
            if tools.menor_que(oid, '1.3.6.1.2.1.16.7'):
                self.proxy.rollback(doble)
                    
            elif tools.menor_que(oid, '1.3.6.1.2.1.16.8'):
                self.rmon_filter.rollback(doble)
                
            #elif tools.menor_que(oid, '1.3.6.1.4'):
            else:
                self.comunidades.rollback(doble)    


