"""
TCP Server
Authors: Daniel Maccaline and Nathan Grady
  Based on code from phase 1 (Daniel Maccaline)
"""

import socket
from PIL import Image
import io
import os



def TCPServer():
    frame=b""
    i=0
    #Define server port number
    serverPort = 11000

    #Create UDP Socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Bind socket to port mumber
    serverSocket.bind(('', serverPort))
    #output message indicating ready to recieve
    print('The server is ready to recieve')
    #Loop forever, continually read messages sent to socket
    f = open("demofileOut.bmp", "wb")
    while True:
        #Recieve message, store message in sentence, store address of client that sent message to clientAddress
        sentence, clientAddress = serverSocket.recvfrom(2048)
        #print(sentence)

        #add all the sentences together
        if(sentence==b'stop'):
            #print(frame)
            f.close()
            os.startfile("demofileOut.bmp")

            print("Number of packages recieved: " + str(i))
            return
        else:
            i = i + 1
            frame+=sentence
            f.write(sentence)


        #Print message recieved from client
        #modify message, used to test if message is being properly sent/recieved both ways

        #print()
        #print((sentence))

        #Send message to client
        serverSocket.sendto("Recieved".encode(), clientAddress)



#Main method used to start server
if __name__ == "__main__":
    TCPServer()




def Assemble_Packets(file, packet):
   
   file = file + packet
   
   return file