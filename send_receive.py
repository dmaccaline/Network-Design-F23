import time

from functions import *
import threading



#this is the first response the server will send to the client

TimerExpired=False
fail=0


def rdt_send(clientSocket,serverName,serverPort,file):
    global  TimerExpired,window,fail

    failcount=0
    sends=0

    nextSeqNum = 1
    base = 1

    # make the buffer Note both the buffer and data have a dummy entry as the first thing in the list
    sndpkt = [b'']
    while (base<len(file)-1):

        if not (TimerExpired):
            # if the next sequence number is between the base and the window but not out of the end of the file
            if (nextSeqNum < base + window and nextSeqNum<len(file)):

                # make the packet and add it to the buffer
                if (printflag): print("sent: ", nextSeqNum, " base: ", base)

                sndpkt.append(make_pkt(nextSeqNum, file[nextSeqNum]))

                udt_send(clientSocket, (serverName, serverPort), sndpkt[nextSeqNum], corruptPercent_client_to_server)
                sends+=1

                if (base == nextSeqNum):
                    # start timer
                    starttimer()
                nextSeqNum += 1

        # recieve the data
        clientSocket.setblocking(0)
        try:
            rcvPacket, addr = clientSocket.recvfrom(2048)
            fail = 0

            if (not corrupt(rcvPacket)):

                data, recieved_sequence_num, chksum = extract(rcvPacket)

                if (printflag): print("recieved: ", recieved_sequence_num, " new base: ", recieved_sequence_num + 1)

                base = recieved_sequence_num + 1

                # if the whole window was recieved then pause the timer
                if (base == nextSeqNum):
                    stopTimer()

                # if we the recieved sequence number is equal to or above the base then reset the timer
                elif (recieved_sequence_num >= base):
                    starttimer()
        except:
            fail+=1
            if(fail==1):
                failcount+=1



        # if the timer is expired resart the timer then retransmit base up to nextseqnum-1
        if (TimerExpired):

            starttimer()
            for i in range(base, nextSeqNum):
                if (printflag): print("resending : ", i, " base: ", base)
                udt_send(clientSocket, (serverName, serverPort), sndpkt[i], corruptPercent_client_to_server)
                sends+=1
    print("done")
    print("failed ",failcount)
    print("sens: ",sends)






sndpkt = make_pkt(0, b'generic response')
expected_sequence_Num=1


def rdt_rcv(recievingSocket):
    global expected_sequence_Num,sndpkt
    # get the data
    flag=True

    while(flag):
        rcvPacket, addr = udt_rcv(recievingSocket)

        # extract the data
        data, recieved_sequence_num, chksum = extract(rcvPacket)
        if(printflag):print("recieved: ", recieved_sequence_num," expecting: ",expected_sequence_Num)

        #if the data is not corrupt and it has the correct sequence number update the response
        if( not corrupt(rcvPacket)and recieved_sequence_num==expected_sequence_Num):
            sndpkt = make_pkt(expected_sequence_Num, b'')
            expected_sequence_Num += 1
            flag=False
        if(corrupt(rcvPacket)):
            if(printflag):print("corrupt")

        #respond to the data
        if printflag: print("sent: ",expected_sequence_Num)
        udt_send(recievingSocket, addr, sndpkt, corruptPercent_server_to_client)

    return data, addr
















#send the packets corrupting some of them
def udt_send(sendingSocket,destination_addr,packet,corruptPercent):
    global lossPercent

    randomNumC = random.randint(1, 100) #for corrupting
    randomNumL = random.randint(0, 99) #for losing packets

    # if the random number is less than corrupt percent corrupt the packet
    if (randomNumC <= corruptPercent):
        packet=coruptPacket(packet)

    if(randomNumL<(100-lossPercent)):
        sendingSocket.sendto(packet, destination_addr)


def udt_rcv(recievingSocket):
    while True:
        #recieve the data as a byte array
        data, addr = recievingSocket.recvfrom(2048) # buffer size is 1024 bytes

        return data, addr









def Timer():
    if(printflag):print("Timer Expired")
    global TimerExpired,fail
    fail=0
    TimerExpired=True

timerThread= threading.Timer(timeout, Timer)


#if a timer thread is running stop it, start another
def starttimer():
    global timerThread,TimerExpired,timeout
    if(printflag):print("starting timer")
    TimerExpired=False
    timerThread.cancel()
    timerThread = threading.Timer(timeout, Timer)
    timerThread.start()


#if a timer thread is running stop it
def stopTimer():
    global  timerThread,timercount,TimerExpired
    if(printflag):print("stop timer")
    timerThread.cancel()
    TimerExpired=False
