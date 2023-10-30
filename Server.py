"""
TCP Server
Authors: Daniel Maccaline and Nathan Grady
  Based on code from phase 1 (Daniel Maccaline)
"""
import socket
from send_receive import *
import os


def UDPServer():

    #string of bytes to hold passed file
    frame=b''

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

        rcvPacket, addr =rdt_rcv(serverSocket)
        if(printflag):  print("recieved packet: ", count)
        if(printflag):  print()
        count+=1

        #if passed sentence = stop code
        if(rcvPacket==b'stop'):
            count=0
            #store created output to bmp file and open the file

            f = open("temp.bmp", "wb")
            f.write(frame)
            f.close()
            os.startfile("temp.bmp")

            #clear the frame
            frame = b''
            #Output completion statement
            print("Finished recieving file\nFile opened in seperate window")

        else:
            #if not at end of file, concatenate sentence to frame
            frame+=(rcvPacket)


#Main method used to start server
if __name__ == "__main__":
    UDPServer()
