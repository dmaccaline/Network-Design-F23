"""
TCP Client
Authors: Daniel Maccaline and Nathan Grady
  Based on code from phase 1 (Daniel Maccaline)
"""
import time
#import socket library
import socket
#import system for command line arguments
import sys
from functions import *
import random

#import file dialog stuff
import tkinter as tk
from tkinter import filedialog


def Make_Packets(file, packetFile, corruptpercent):
    #keep track of how many corrupt and non corrupt packets there are
    corruptPacketsCount=0
    cleanPakcetsCount=0


    #read in file
    data = file.read()
    currentIndex = 0

    #create packet list
    packet = []

    while(currentIndex < len(data)):

        #extract just the data from the packet
        rawPacket=data[currentIndex:currentIndex + 1024]

        #add the header Hpacket=packet with header
        Hpacket=addPacketHeader(rawPacket)


        # determine if the packet will be corrupt
        randomNum = random.randint(1, 100)

        # if the random number is less than corrupt percent corrupt the packet
        if(randomNum<=corruptpercent):
            corruptPacketsCount+=1
            Hpacket=coruptPacket(Hpacket)
        else:
            cleanPakcetsCount+=1

        #append the packet with the header to the list
        packet.append(Hpacket)

        #get the next packet
        currentIndex += 1024

    print("corrupt packets: " + str(corruptPacketsCount))
    print("clean packets: "+str(cleanPakcetsCount))

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

    packet = Make_Packets(file, packetSize,10)

    file.close()

#Transmit

    #set server name and port to expect server at
    serverName = 'localhost'
    serverPort = 11000

    #create UDP Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i in range (0,len(packet)):
        clientSocket.sendto(packet[i], (serverName, serverPort))
        #time.sleep(0.001)

    clientSocket.sendto(b'stop', (serverName, serverPort))


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