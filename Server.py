"""
TCP Server
Authors: Daniel Maccaline and Nathan Grady
  Based on code from phase 1 (Daniel Maccaline)
"""

import socket
from PIL import Image
import io




def TCPServer():
    frame=b""
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
        #print(sentence)

        #add all the sentences together
        if(sentence==b'stop'):
            #print(frame)
            image_stream = io.BytesIO(frame)
            #Open the image using Pillow
            image = Image.open(image_stream)
            image.show()
            frame=b''
        frame+=sentence




        #Print message recieved from client
        #modify message, used to test if message is being properly sent/recieved both ways

        print()
        print((sentence))

        #Send message to client
        #serverSocket.sendto("Recieved".encode(), clientAddress)



#Main method used to start server
if __name__ == "__main__":
    TCPServer()




def Assemble_Packets(file, packet):
   
   file = file + packet
   
   return file