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
import time
from functions import *

results = []

def Get_Packets_Raw(file, packetsize):

    currentIndex = 0

    data = file.read()

    #create packet list
    packet = [b'']

    while(currentIndex < len(data)):

        #extract just the data from the packet
        bytesdata=data[currentIndex:currentIndex + packetsize]

        packet.append(bytesdata)

        currentIndex += packetsize

    packet.append(b'stop')
    return packet

#Client Functionality (called from main)
def UDPClient(fileName):

    # packet size in bytes
    packetSize = 1024

    # read file in here
    try:
        file = open(fileName, "rb")
    except:
        print("File could not be opened...")
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
    clientSocket.bind(('', 9999))

    #send packets one at a time
    try:
        print("PIPELINED DATA TRANSFER WINDOW SIZE: ",window)
        print("sending ",len(data),"packets")
        print("corruption rate from the client to the server is: ",corruptPercent_client_to_server,"%")
        print("corruption rate from the server to the client is: ",corruptPercent_server_to_client,"%")
        print("loss percent both ways is: ",lossPercent,"%")
        print("timeout is : ",timeout," seconds")
        print()

        start_time = datetime.datetime.now()

        rdt_send(clientSocket, serverName, serverPort, data)

        #send stop bit

        end_time=datetime.datetime.now()
        print()
        print("finished sending")
        print("start: ",start_time," end:",end_time)
        time = end_time-start_time
        print("total time: ",(end_time-start_time))

    except:
        print("ther server is probably down")
        return 0, 0

    clientSocket.close()
    #Return time taken in microseconds and seconds
    return time.microseconds, time.seconds



#Main, used to start TCPClient and send name of passed file
if __name__ == "__main__":

    #Variables used for automatic tests, Iterations -> Number of tests, runMultipleTests bool used to control if tests are done
    iterations = 2
    runMultipleTests = False

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()


    #check if input argument provided
    if len(file_path) <= 1:
        #output error if no input file provided
        print("Error: No input file specified")
    else:
        #if not running multiple, just call UDP client and disregard returns
        if not runMultipleTests:
            #pass input file name to client
            UDPClient(file_path)
        else:
            #Store number of iterations for denominator of average calc
            avgDen = iterations
            #Stores time returned by function
            timeR = 0
            #iterate for (iterations) times
            while(iterations > 0):
                print("\n\n\nStarting run " + str(avgDen-iterations))
                iterations = iterations - 1
                #Function returns time spent in microseconds and seconds
                micros, sec = UDPClient(file_path)
                #add time to timeR, dividing micros to adjust
                timeR = timeR + micros/1000000 + sec
                #sleep before next call (avg time goes up without this sleep)
                time.sleep(1)
            #print average results
            print("Average results: ", str(timeR/avgDen))