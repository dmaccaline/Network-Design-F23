"""
TCP Server
Authors: Daniel Maccaline and Nathan Grady
  Based on code from phase 1 (Daniel Maccaline)
"""

import socket
from functions import *
import os



def TCPServer():

    #string of bytes to hold passed file
    frame=[]

    #Define server port number
    serverPort = 11000

    #Create UDP Socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Bind socket to port mumber
    serverSocket.bind(('', serverPort))
    #output message indicating ready to recieve
    print('The server is ready to recieve')

    count=0
    #Loop forever, continually read messages sent to socket
    while True:
        #

        rcvPacket, addr =rdt_rcv(serverSocket)
        print("recieved packet: ", count)
        count+=1

        #print(rcvPacket)
        #if passed sentence = stop code
        print(binary_array_to_byte_array(rcvPacket))
        if(binary_array_to_byte_array(rcvPacket)==b'stop'):
            count=0
            #store created output to bmp file and open the file

            #convert it back to bytes sigh
            bytedata=binary_array_to_byte_array(frame)

            f = open("temp.bmp", "wb")
            f.write(bytedata)
            f.close()
            os.startfile("temp.bmp")

            frame = []
            #Output completion statement
            print("Finished recieving file\nFile opened in seperate window")

        else:
            #if not at end of file, concatenate sentence to frame
            frame+=(rcvPacket)


#Main method used to start server
if __name__ == "__main__":
    TCPServer()
