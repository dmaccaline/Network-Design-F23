"""
TCP Client
Authors: Daniel Maccaline and Nathan
  Based on code from phase 1 (Daniel Maccaline)
"""

#import socket library
import socket
#import system for command line arguments
import sys

#import file dialog stuff
import tkinter as tk
from tkinter import filedialog

#Client Functionality (called from main)
def TCPClient(file):
    #from socket import *

    #output message to indicate client startup/message contents
    print('Starting Client to send image: ', file)

#read file in here

#Split into packages here
    #None functioning, need to send bytes, not lists
    packets = Make_Packets(file)





#Transmit

    #set server name and port to expect server at
    serverName = 'localhost'
    serverPort = 11000

    #create UDP Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    #im just going to transmit dummy packets for now so that way i have something
    #to work with on the server side.
    for i in range (0, len(packets)):
        print('Sending: ' + str(packets[i]))

        #convert list to byte array
        values = bytearray(packets[i])

        #Non functioning, need to send bytes, not lists


        clientSocket.sendto(values, (serverName, serverPort))

    #Send message to server at port defined earlier
    #clientSocket.sendto(input.encode(), (serverName, serverPort))


#not using recvfrom (no server response expected)
#recieve message being sent back to client
#    modifiedSentence, server = clientSocket.recvfrom(2048)

    #close socket
    clientSocket.close()


def Make_Packets(file):
    packets = [[1, 0, 0, 1], [1, 1, 1, 0], [0, 1]]
    return packets

#Main, used to start TCPClient and send name of passed file
if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    #check if input argument provided
    if len(file_path) <= 1:
        #output error if no input file provided
        print("Error: No input file specified")
    else:
        #pass input file name to client
        TCPClient(file_path)


