#!/usr/bin/python3

import sys
import random
import socket
import os
import time
import json
from threading import Thread
from threading import Lock
import colorama
from colorama import Fore, Style, Back
#globais
timer = random.randrange(8,10)
lock = Lock()


class Node():
    def __init__(self, ID):
        self.ID = ID # identificador do nó
        self.neighbour = list() # lista de vizinhos
        self.vector = list() # vetor de custos
        self.nodesqt = 0 # quantidade de nós
        self.initVector()
        self.count = 1

    def sendVector(self):
        global timer

        for n in range (0, len(self.neighbour)):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('localhost', 52000 + self.neighbour[n])
                sock.connect(server_address)
                msg = "[" + str(self.ID) + "," + json.dumps(self.vector) + "]"
                sock.send(msg.encode())
                print ("\nEnviei minha tabela para: " + str(self.neighbour[n]))
            except Exception as e:
                print ("\n",Fore.WHITE,Back.RED,e,Style.RESET_ALL)


    def updateVector(self, nbvector):  #[id, [] ]
        # flag de controle de atualização
        updated = False

        print("\n\n",Back.WHITE,Fore.BLUE,"#" + str(self.count) + " - Recebi uma atualização do nó " + str(nbvector[0]), Style.RESET_ALL)
        self.count = self.count + 1
        print("\nMeu vetor de distâncias atual:")
        self.printVector()

        # recebe a distancia ate o vizinho
        distnode = nbvector[1][self.ID]

        for n in range(0, len(self.vector)):
            # se a (distancia ate o vizinho + a distancia do vizinho ate o nó n) for menor
            # que a distancia guardada na tabela, substitue. se não, mantém.
            if (distnode + nbvector[1][n]) < self.vector[n]:
                self.vector[n] = distnode + nbvector[1][n]
                updated = True

        if updated == True:
            print (Fore.GREEN,"\nVetor de " + str(self.ID) + " atualizado",Style.RESET_ALL)
            self.printVector()
        else:
            print ("\n",Fore.RED,Back.WHITE,"Vetor de " + str(self.ID) + " não teve atualização",Style.RESET_ALL,"\n")


    def initVector(self):
        with open('topology.json') as data_file:
            data = json.load(data_file)
        self.vector = data[self.ID]
        self.nodesqt = len(data)
        print ("\nTabela do nó " + Fore.BLUE,Back.YELLOW, str(self.ID),Style.RESET_ALL + " inicializada")
        # preenche lista de vizinhos (não precisa ser atualizada nunca)
        for n in range(0, len(self.vector)):
            if self.vector[n] != 999 and n != self.ID:
                self.neighbour.append(n)
        # dispara timer para enviar o update

    def printVector(self):
        print ("\nDistâncias:")
        for n in range(0, len(self.vector)):
            print("Nó " + str(n) + ": " + str(self.vector[n]))


class TicTacker(Thread): # decrementa o timer, e ao zerar, chama o enviar mensagem
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global timer
        global lock

        time.sleep(0.100)
        while 1:
            with lock:
                if(timer > 0):
                    timer = timer - 1
                else:
                    n.sendVector()
                    timer = random.randrange(4, 9)
            print(Fore.YELLOW,(str(timer) + " "), Style.RESET_ALL, sep=' ', end='', flush=True)
            time.sleep(1)

class Listener(Thread):
    def __init__(self, ID, nodesqt):
        self.port = 52000 + int(ID)
        self.nodesqt = int(nodesqt)
        Thread.__init__(self)

    def run(self):
        serverPort = self.port
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            serverSocket.bind(('',serverPort))
            serverSocket.listen(1)
            print ('*** Subindo o nó de número ', Fore.MAGENTA,Back.WHITE, self.port - 52000,Style.RESET_ALL,' no total de ', Fore.MAGENTA,Back.WHITE,self.nodesqt,Style.RESET_ALL,'***')
            print('*** No ar através da porta: ', self.port,' ***' )

            while 1:
                connectionSocket, addr = serverSocket.accept()
                c = ClientHandler(connectionSocket, addr)
                c.start()

        except Exception as e :
                print (Fore.WHITE,Back.RED,e,Style.RESET_ALL)



class ClientHandler(Thread):
    def __init__(self,connectionSocket, addr):
        self.addr = addr
        self.connectionSocket = connectionSocket
        Thread.__init__(self)

    def run(self):
        global n
        global timer
        global lock
        try:
            msg = self.connectionSocket.recv(512) #[id, [vector]]
            msg = msg.decode('utf-8')
            #print ("Recebi da rede: ", msg)
            data = json.loads(str(msg))
            n.updateVector(data)
            with lock:
                timer = random.randrange(4,9)

        except Exception as e :
            exec_type, exec_obj, exec_tb = sys.exc_info()
            print ("Erro:", exec_type, exec_tb.tb_lineno,"\n",e)
            sys.exit(2)



def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    if( len(sys.argv)!=2):
        print("Chamada inválida use: $ python3 rip.py NUM_NO")
        sys.exit(1)
    global n

    n = Node(int(sys.argv[1]))
    nodesqt = n.nodesqt
    listener = Listener(int(sys.argv[1]), nodesqt)
    t = TicTacker()

    listener.start()
    t.start()

if __name__ == "__main__":
    main()
