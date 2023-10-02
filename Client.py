"""
TCP Client
Authors: Daniel Maccaline and Nathan Grady
  Based on code from phase 1 (Daniel Maccaline)
"""
import time
#import socket library
import socket

#import file dialog stuff
import tkinter as tk
from tkinter import filedialog


def Make_Packets(file, packetSize):

    #Read file data
    data = file.read()

    #Setup variable to track progress
    currentIndex = packetSize

    #Get first packet
    packet = [data[0:packetSize]]

    #loop and create all other packets
    while(currentIndex < len(data)):
        packet.append(data[currentIndex:currentIndex + packetSize])
        currentIndex += packetSize

    #Return results
    return packet

#Client Functionality (called from main)
def TCPClient(fileName):

    #packet size in bytes
    packetSize = 1024

    #output message to indicate client startup/message contents
    print('Starting Client to send image: ', fileName)

    #read file in, output error if fails
    try:
        file = open(fileName,"rb")
    except:
        print("File could not be opened...")
        return

    #Create packets
    packet = Make_Packets(file, packetSize)

    #Close files
    file.close()

#Transmit

    #set server name and port to expect server at
    serverName = 'localhost'
    serverPort = 11000

    #create UDP Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    #Loop for each packet that needs to be sent
    for i in range (0,len(packet)):
        #Send packet
        clientSocket.sendto(packet[i], (serverName, serverPort))
        #Wait for server acknoledgement (will cause severe packet loss if client sends faster than server can recieve)
        modifiedSentence, server = clientSocket.recvfrom(2048)

    #Send code indicating end of file
    time.sleep(0.1)
    clientSocket.sendto(b'stop', (serverName, serverPort))

    #Output statement to command line and close socket
    print("Finished sending file")
    clientSocket.close()

#Main, used to start TCPClient and send name of passed file
if __name__ == "__main__":

    #Open file select menue
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    #check if file is selected
    if len(file_path) <= 1:
        #output error if no input file provided
        print("Error: No input file specified")
    else:
        #pass input file name to client
        TCPClient(file_path)
