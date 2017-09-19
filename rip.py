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
        for n in range(0, len(self.vector)):
            if self.vector[n] != 999:
                self.neighbour.append(n)
