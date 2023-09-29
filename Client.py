"""
TCP Client
Created 9/13/2023
Author: Daniel Maccaline
Based on code from presentation slides:
    Vokkarane, V, Python Socket Programming 101 - Python.pptx. University of Massachusetts Lowell, EECE.5830
"""

#import socket library
import socket

#Client Functionality (called from main)
def TCPClient(input):
    #from socket import *

    #output message to indicate client startup/message contents
    print('Starting Client with message: ', input)

    #set server name and port to expect server at
    serverName = 'localhost'
    serverPort = 11000

    #create UDP Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Send message to server at port defined earlier
    clientSocket.sendto(input.encode(), (serverName, serverPort))
    #recieve message being sent back to client
    modifiedSentence, server = clientSocket.recvfrom(2048)

    #print returned message
    print('from Server: ', modifiedSentence.decode())
    print('Server socket number: ' + str(server[1]))

    #close socket
    clientSocket.close()

#Main, used to start TCPClient
if __name__ == "__main__":
    TCPClient('Hello')