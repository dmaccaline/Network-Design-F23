from functions import *
import threading
import time

#global vairables
timerExpired = False
runTimer=True
nextSeqNum=0
base=0
window=10
sndpkt=[]
GO = True


def Timer():
    print("Timer Expired")
    global timerExpired
    timerExpired=True


#the listners job is listen for packets check if they are good and to move the base
#variable that is being used in the sender function
def Listner(clientSocket):
    global nextSeqNum, base, window, runTimer, sndpkt

    while (True):
        # Attempt to read from socket.  NOTE: With setvlocking(0) set, will throw error if nothing is ready to recieve
        try:
            # wait for ACKS
            rcvpkt, addr = clientSocket.recvfrom(2048)
            data, recieved_sequence_num, chksum = extract(rcvpkt)
            print("got ACK: ",recieved_sequence_num)
            if(not corrupt(rcvpkt)):
                if(base==recieved_sequence_num):
                    base+=1
        except:
            pass



#the job of the sender is to transmit base up to the window size and then retransmit if the
#timer runs out
def Sender(clientSocket,serverName,serverPort,allData):
    global nextSeqNum, base, window, runTimer,sndpkt

    while(True):
        if(not timerExpired):

            if(nextSeqNum<base+window):
                    sndpkt.append(make_pkt(nextSeqNum,allData[nextSeqNum]))
                    print("sending packet",nextSeqNum)
                    udt_send(clientSocket,(serverName,serverPort),sndpkt[nextSeqNum],corruptPercent_client_to_server,loss_Percent_client)
                    if(base==nextSeqNum):
                        #Start timer
                        runTimer=True
                    nextSeqNum+=1


                #if the timer is expired resart timer then retransmit
        else:
            # resart timer
            runTimer = False
            time.sleep(0.1)
            runTimer = True
            time.sleep(0.1)

            # resend all of the packts saved in sndpkt
            for i in range(base, nextSeqNum):
                print("resending Packet: ", i)
                udt_send(clientSocket, (serverName, serverPort), sndpkt[i], corruptPercent_client_to_server,
                         loss_Percent_client)



#this thread will call the timer thread after the interval. However if runtimer is turned off
#before that it will just cancel the timer thread. If There is no timer thread and runTimer is
#turned on then it will make a timer thread. This way you can turn the timer on and off from anywhere
#else in the code just by changing the runTimer Variable
def timerControler(num):
    count=0
    global runTimer
    global timerExpired

    while(True):
        #if run timer is on and there are not currently any timer threads then make one
        if(runTimer and count<1):
            timerExpired=False
            S = threading.Timer(3, Timer)
            S.start()
            count+=1
        #if run timer is off and a timer thread is on then turn it off
        if(not runTimer and count>0):
            #if we turn off the timer stop the timer thread
            S.cancel()
            count-=1


def rdt_send(clientSocket,serverName,serverPort,allData):
    global runTimer

    #this function needs to be in differnt threads so it can listen and send at the same time
    lisnerThread = threading.Thread(target=Listner, args=(clientSocket,))
    SenderThread = threading.Thread(target=Sender, args=(clientSocket,serverName,serverPort,allData))
    TimerControl=threading.Thread(target=timerControler, args=(10,))

    lisnerThread.start()
    SenderThread.start()
    TimerControl.start()


    #wait for threads to finsih, none of them will yet
    lisnerThread.join()
    SenderThread.join()
    TimerControl.join()



#send the packets corrupting some of them
def udt_send(sendingSocket,destination_addr,packet,corruptPercent,loss_Percent):

    randomNumC = random.randint(1, 100) #for corrupting
    randomNumL = random.randint(0, 99) #for losing packets

    # if the random number is less than corrupt percent corrupt the packet
    if (randomNumC <= corruptPercent):
        packet=coruptPacket(packet)

    if(randomNumL<(100-loss_Percent)):
        sendingSocket.sendto(packet, destination_addr)


def udt_rcv(recievingSocket):
    while True:
        #recieve the data as a byte array
        data, addr = recievingSocket.recvfrom(2048) # buffer size is 1024 bytes

        return data, addr


expected_sequence_Num=0
returnPckt=make_pkt(3,b'ACK')
def rdt_rcv(recievingSocket):
    global  expected_sequence_Num

    while(True):
        #get the packet out of the socket
        rcvPacket, addr=udt_rcv(recievingSocket)

        #extract stuff out of the packet
        data,recieved_sequence_num,chksum = extract(rcvPacket)

        #if the packet is good update the response packet
        if(not corrupt(rcvPacket) and recieved_sequence_num==expected_sequence_Num):
            returnPckt=make_pkt(expected_sequence_Num,b'ACK')

        #send the response packet
        udt_send(recievingSocket, addr, returnPckt,corruptPercent_server_to_client,loss_Percent_server)
        #iterate the expect sequence number
        expected_sequence_Num+=1

        print("the esn is now : ",expected_sequence_Num)


    # #deliver the data
    return b'nada', 0