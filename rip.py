#!/usr/bin/python3

import sys
import random
import socket
import os
import time
import json

class Node():
    def __init__(self, ID):
        self.ID = ID # identificador do nó
        self.neighbour = list() # lista de vizinhos
        self.vector = list() # vetor de custos
        self.nodesqt = 0 # quantidade de nós

    def sendVector(self):
        global timer

        for n in range (0, len(self.neighbour)):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('localhost', 52000 + self.neighbour[n])
                sock.connect(server_address)
                msg = "[" + str(self.ID) + "," + json.dumps(vector) + "]"
                sock.send(msg.encode())
                timer = random.randrange(4, 9)
                print ("Enviei minha tabela para: " + self.neighbour[n])
            except Exception as e:
                print(e)

    def updateVector(self, nbvector):
        # flag de controle de atualização
        updated = 0

        # precisa receber ID do vizinho
        print("Recebi uma atualização do nó " + nbID)
        print("Vetor atual do nó " + self.ID)
        self.printVector()

        # recebe a distancia ate o vizinho
        distnode = nbvector[self.ID]

        for n in range(0, len(nbvector)):
            # se a (distancia ate o vizinho + a distancia do vizinho ate o nó n) for menor
            # que a distancia guardada na tabela, substitue. se não, mantém.
            if (distnode + nbvector[n]) < self.vector[n]:
                self.vector[n] = distnode + nbvector[n]
                updated++

        if updated > 0:
            print ("Vetor de " + self.ID + " atualizado")
            self.printVector()
            # aqui chama o envia tabela? ou manda mesmo quando não tiver atualizada?
        else:
            print ("Vetor de " + self.ID + " não teve atualização")

        # Initialization:
            # for all destinations y in N:
                # D x (y) = c(x,y)
                # /* if y is not a neighbor then c(x,y) = ∞ */
            # for each neighbor w
                # D w (y) = ? for all destinations y in N
            # for each neighbor w
                # send distance vector D x = [D x (y): y in N] to w
        #  loop
            # wait (until I see a link cost change to some neighbor w or
                # until I receive a distance vector from some neighbor w)
            # for each y in N:
                # D x (y) = min v {c(x,v) + D v (y)}
            # if D x (y) changed for any destination y
                # send distance vector D x = [D x (y): y in N] to all neighbors

    def initVector(self):
        with open('topology.json') as data_file:
            data = json.load(data_file)
        self.vector = data[self.ID]
    	print ("Tabela do nó " + self.ID + " inicializada")
        # preenche lista de vizinhos (não precisa ser atualizada nunca)
        for n in range(0, len(self.vector)):
            if self.vector[n] != 999:
                self.neighbour.append(n)
        # dispara timer para enviar o update

    def printVector(self):
        print "Distâncias:\n"
        for n in range(0, len(self.vector)):
            print("Nó " + n + ": " + self.vector[n])

class Listener():
    def __init__(self):
