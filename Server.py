"""
TCP Server
Authors: Daniel Maccaline and Nathan Grady
  Based on code from phase 1 (Daniel Maccaline)
"""

import socket
import os



def TCPServer():

    #string of bytes to hold passed file
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

        #if passed sentence = stop code
        if(sentence==b'stop'):
            #store created output to bmp file and open the file
            f = open("temp.bmp", "wb")
            f.write(frame)
            f.close()
            os.startfile("temp.bmp")

            frame = b""
            #Output completion statement
            print("Finished recieving file\nFile opened in seperate window")

        else:
            #if not at end of file, concatenate sentence to frame
            frame+=sentence


#Main method used to start server
if __name__ == "__main__":
    TCPServer()
