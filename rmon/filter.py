import MySQLdb
from scapy.all import *
from multiprocessing import Process, Value, Array
import pcap

class filter:

    ######################
    # Funciones Publicas #
    ######################
    
    def __init__(self, N_FILTROS, BBDD, interfaces):
        # Creamos las variables
        self.N_FILTROS = N_FILTROS
        self.BBDD = BBDD
        self.interfaces = interfaces
        self.matches = Array('i', [0]*self.N_FILTROS)
        self.process = [0]*self.N_FILTROS
        self.indices = [0]*self.N_FILTROS


    def start(self):
        # Cargamos los filtros
        db_rmon=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="rmon")
        db_rmon.autocommit(True)
        cursor = db_rmon.cursor()

        cursor.execute("SELECT channelIndex FROM td_channelEntry WHERE channelStatus = \'1\'" )
        result = cursor.fetchall()
        if str(result) != "None":
            for canal in result:
                # Comprobamos que hay sitio en la memoria compartida
                self.ind = self.busca_memoria()
                if self.ind != None:
                    status, match, interfaz, filtro = self.genera_filtro(str(canal[0]))
                    if status == 1:
                        self.indices[self.ind] = canal[0]
                        self.matches[self.ind] = match
                        self.process[self.ind] = Process(target=self.captura, args=(interfaz, filtro))
                        self.process[self.ind].start()

                    else:
                        print("Formato de filtro erroneo")

                else:
                    print("No hay espacio en memoria para el filtro")

        else:
            print("No hay ningun filtro declarado")





    def add(self, index):
        self.ind = self.busca_memoria()
        if self.ind != None:
            status, match, interfaz, filtro = self.genera_filtro(str(index))
            if status == 1:
                self.indices[self.ind] = int(index)
                self.matches[self.ind] = match
                self.process[self.ind] = Process(target=self.captura, args=(interfaz, filtro))
                self.process[self.ind].start()
                print(filtro)

            else:
                print("Formato de filtro erroneo")

        else:
            print("No hay espacio en memoria para el filtro")


    def delete(self, index):

        ind = None
        for i in range(len(self.indices)):
            if self.indices[i] == int(index):
                ind = i

                if ind != None:
                    self.indices[ind] = 0
                    self.matches[ind] = 0
                    self.process[ind].terminate()

                else:
                    print("El filto no existia")


    def kill(self):
        for i in range(len(self.indices)):
            if self.indices[i] != 0:
                self.process[i].terminate()


    def update(self):
        db_rmon=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="rmon")
        db_rmon.autocommit(True)
        cursor = db_rmon.cursor()

        for i in range(len(self.indices)):
            if self.indices[i] != 0:
                cursor.execute("UPDATE td_channelEntry SET channelMatches = " + str(self.matches[i]) + " WHERE channelIndex = %s", (str(self.indices[i]),) )
                #print str(self.indices[i]) + ": " + str(self.matches[i])



    ######################
    # Funciones Privadas #
    ######################


    def busca_memoria(self):
        ind = None
        for i in range(len(self.indices)):
            if self.indices[i] == 0:
                ind = i
                break
        return ind

    def genera_filtro(self, index):

        filterIndex = []            
        filterPktDataOffset = []
        filterPktData = []
        filterPktDataMask = []
        filterPktDataNotMask = []
        filterPktStatus = []
        filterPktStatusMask = []
        filterPktStatusNotMask = []
        filtro = ""
        interfaz = ""
        status = 1

        db_rmon=MySQLdb.connect(host=self.BBDD.ADDR,user=self.BBDD.USER,passwd=self.BBDD.PASS, db="rmon")
        db_rmon.autocommit(True)
        cursor = db_rmon.cursor()

        cursor.execute("SELECT * FROM td_channelEntry WHERE channelIndex = %s", (index,) )
        result = cursor.fetchone()
        if str(result) != "None":
            channelIfIndex = result[1]
            channelAcceptType = result[2]
            channelMatches = result[8]
            try:
                interfaz = self.interfaces[str(channelIfIndex)]
                # interfaz = subprocess.check_output(["snmpget", "-v", "1", "-c", "public", "localhost:162", "1.3.6.1.2.1.2.2.1.2." + str(channelIfIndex)])
                # interfaz = interfaz.split("\"")
                # interfaz = interfaz[1]
            except:
                status = 0
                print("Error al conseguir el interfaz")

            cursor.execute("SELECT * FROM td_filterEntry WHERE filterChannelIndex = %s and filterStatus = \'1\'", (index,) )
            result = cursor.fetchall()
            if str(result) != "()":

                if channelAcceptType == 1:

                    for i in range(len(result)):
                    
                        filterIndex.append(result[i][0])
                        filterPktDataOffset.append(result[i][2])
                        filterPktData.append(result[i][3])
                        filterPktDataMask.append(result[i][4])
                        filterPktDataNotMask.append(result[i][5])
                        filterPktStatus.append(result[i][6])
                        filterPktStatusMask.append(result[i][7])
                        filterPktStatusNotMask.append(result[i][8])

                        filtro = filtro + "("

                        for j in range(len(result[i][4])):
                            data = int(ord(result[i][3][j]))
                            mask = int(ord(result[i][4][j]))
                            notMask = int(ord(result[i][5][j]))
                            resultado = (data & ~notMask) | (~data & notMask)

                            filtro = filtro + "((ether[" + str(int(filterPktDataOffset[i]) + j ) + "] & " + str(mask) + ") == " + str(resultado) + ")"
                            if j != len(result[i][4])-1:
                                filtro = filtro + " and "
                            
                        if i != len(result)-1:
                            filtro = filtro + ") or "

                    filtro = filtro + ")"

                elif channelAcceptType == 2:

                    for i in range(len(result)):
                    
                        filterIndex.append(result[i][0])
                        filterPktDataOffset.append(result[i][2])
                        filterPktData.append(result[i][3])
                        filterPktDataMask.append(result[i][4])
                        filterPktDataNotMask.append(result[i][5])
                        filterPktStatus.append(result[i][6])
                        filterPktStatusMask.append(result[i][7])
                        filterPktStatusNotMask.append(result[i][8])

                        filtro = filtro + "("

                        for j in range(len(result[i][4])):
                            data = int(ord(result[i][3][j]))
                            mask = int(ord(result[i][4][j]))
                            notMask = int(ord(result[i][5][j]))
                            resultado = (data & ~notMask) | (~data & notMask)

                            filtro = filtro + "((ether[" + str(int(filterPktDataOffset[i]) + j ) + "] & " + str(mask) + ") != " + str(resultado) + ")"
                            if j != len(result[i][4])-1:
                                filtro = filtro + " or "
                            
                        if i != len(result)-1:
                            filtro = filtro + ") and "

                    filtro = filtro + ")"

                else:
                    status = 0
                    print("channelAcceptType no valido")
                                               
            else:
                status = 0
                print("No hay ningun filtro configurado")

        else:
            status = 0
            print("Error al acceder a la base de datos 1")

        return status, channelMatches, interfaz, filtro



#    def callback(self, pkt):
    def callback(self, self_pc, hdr, data):
        self.matches[self.ind] += 1
        
    def captura(self, interfaz, filtro):  
#        sniff(iface=interfaz, filter=filtro, prn=self.callback)
        pc = pcap.pcapObject()
        pc.open_live(interfaz, 1, True, 1000)
        pc.setfilter(filtro, True, 0)
        pc.loop(-1, self.callback)
