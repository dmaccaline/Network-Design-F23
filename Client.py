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


def Make_Packets(file, packetFile):

    data = file.read()

    currentIndex = 1024

    packet = [data[0:1024]]

    while(currentIndex < len(data)):
        packet.append(data[currentIndex:currentIndex + 1024])
        currentIndex += 1024
    
    return packet

#Client Functionality (called from main)
def TCPClient(fileName):
    #from socket import *

    #packet size in bytes
    packetSize = 1024

    #output message to indicate client startup/message contents
    print('Starting Client to send image: ', fileName)

#read file in here
    try:
        file = open(fileName,"rb")
    except:
        print("File coould not be opened...")
        return
    
    
    if file.closed:
        print("File could not be opened")

    packet = Make_Packets(file, packetSize)

    file.close()


#Split into packages here
    #None functioning, need to send bytes, not lists
   # packets = Make_Packets(file)

#Transmit

    #set server name and port to expect server at
    serverName = 'localhost'
    serverPort = 11000

    #create UDP Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Number of packets to send: " + str(len(packet)))

    for i in range (0, len(packet)):
        print('Sending packet ' + str(i) + " of size " + str(len(packet[i])) + " Bytes ")
        #Non functioning, need to send bytes, not lists
        clientSocket.sendto(packet[i], (serverName, serverPort))


#not using recvfrom (no server response expected)
#recieve message being sent back to client
#    modifiedSentence, server = clientSocket.recvfrom(2048)

    #close socket
    clientSocket.close()

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
