"""
TCP Server
Authors: Daniel Maccaline and Nathan
  Based on code from phase 1 (Daniel Maccaline)
"""

import socket

def TCPServer():
    #from socket import *

    #Define server port number
    serverPort = 11000

    #Create UDP Socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Bind socket to port mumber
    serverSocket.bind(('', serverPort))
    #output message indicating ready to recieve
    print('The server is ready to recieve')

    #Loop forever, continually read messages sent to socket
    while True:

        #Recieve message, store message in sentence, store address of client that sent message to clientAddress
        sentence, clientAddress = serverSocket.recvfrom(2048)
        print(sentence)

        #Print message recieved from client
        #print("from connected user: " + str(sentence.decode()))
        #print('Client socket number: ' + str(clientAddress[1]))
        #modify message, used to test if message is being properly sent/recieved both ways
        modifiedSentence = sentence.decode() + '!'

        #Send message to client
        #serverSocket.sendto(modifiedSentence.encode(), clientAddress)


#Main method used to start server
if __name__ == "__main__":
    TCPServer()




def Assemble_Packets(file, packet):
   
   file = file + packet
   
   return file