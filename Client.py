"""
TCP Client
Authors: Daniel Maccaline and Nathan Grady
  Based on code from phase 1 (Daniel Maccaline)
"""
import socket
import tkinter as tk
from tkinter import filedialog
from send_receive import *
import datetime

def Get_Packets_Raw(file, packetsize):

    currentIndex = 0

    data = file.read()

    #create packet list
    packet = []

    while(currentIndex < len(data)):

        #extract just the data from the packet
        bytesdata=data[currentIndex:currentIndex + packetsize]

        packet.append(bytesdata)

        currentIndex += packetsize

    return packet

#Client Functionality (called from main)
def TCPClient(fileName):

    # packet size in bytes
    packetSize = 1024

    # read file in here
    try:
        file = open(fileName, "rb")
    except:
        print("File coould not be opened...")
        return

    if file.closed:
        print("File could not be opened")

    #raw packets means just the packet with no header or anything yet
    data = Get_Packets_Raw(file, packetSize)

    file.close()
    # endregion

    # set server name and port to expect server at
    serverName = 'localhost'
    serverPort = 11000
    # create UDP Socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #send packets one at a time
    try:
        print("sending ",len(data),"packets at a corruption rate of ",corruptPercent,"%")
        start_time = datetime.datetime.now()

        for i in range (0,len(data)):
            rdt_send(clientSocket, serverName, serverPort, data[i])
            if(printflag):      print("sending packet number ",i)

        #send stop bit
        rdt_send(clientSocket, serverName, serverPort, b'stop')

        end_time=datetime.datetime.now()
        print()
        print("finished sending")
        print("start: ",start_time," end:",end_time)
        print("total time: ",(end_time-start_time))

    except:
        print("ther server is probably down")


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