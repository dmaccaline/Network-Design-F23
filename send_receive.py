from functions import *
import threading
import time

#global vairables
timerExpired = False
nextSeqNum=0
base=0
window=10
sndpkt=[]
GO = True


def timerCall():
    if(printflag):  print("Timer expired")
    global timerExpired
    timerExpired = True


def rdt_send(clientSocket,serverName,serverPort,allData):
    #Calls udt_send on data packets in list allData to send packets to server
    global base, window, timerExpired

    timerExpired = False
    # arguments (x, f), after x seconds, call function f
    timer = threading.Timer(.001, timerCall)

    sentPackets = 0
    recievedAcks = 0

    finishedSending = False

    # Start timer
    timer.start()
    while(not finishedSending):

        if(timerExpired):
            if (printflag):   print("Timer expired, re-send all packets in window")
            #reduce sendPackets
            timer.cancel()
            timer = threading.Timer(.001, timerCall)
            print("sentPackets%30 before: ", sentPackets%30, "sentPackets: ", sentPackets, "Base: ", base)
            sentPackets = recievedAcks
            print("   sentPackets: ", sentPackets)
            #reset and restart timer
            timerExpired = False
            timer.start()

        #if not all packets in window sent, send next packet and update sentPackets
        if(((sentPackets%30 < (base + window)%30) or (base+window >= 30 and sentPackets%30 >= base)) and sentPackets < len(allData)):
            if(printflag):  print("Sent packet: ", sentPackets, " (", sentPackets%30, ")")
            sendpkt = make_pkt(sentPackets%30, allData[sentPackets])
            udt_send(clientSocket,(serverName,serverPort),sendpkt,corruptPercent_client_to_server, loss_Percent_client)
            sentPackets = sentPackets + 1

        #check if an ack has arrived
        clientSocket.setblocking(0)

        try:
            rcvpkt, addr = clientSocket.recvfrom(2048)
            # Packet recieved, extract dadta and check if a good ack
            data, recieved_sequence_num, chksum = extract(rcvpkt)
            if (printflag):      print("     recivied seq: ", recieved_sequence_num)

            # if corrupt or sequence number not in window
            if ((corrupt(rcvpkt) or ((recieved_sequence_num < base) and (recieved_sequence_num > base - 4) and recieved_sequence_num < base + window))):
                if (printflag):   print("bad ack")
            else:
                if (printflag):  print("good ack, moving window to ", recieved_sequence_num)
                if(recieved_sequence_num < base):
                    recievedAcks = recievedAcks + ((recieved_sequence_num+30) - base + 1)
                else:
                    recievedAcks = recievedAcks + (recieved_sequence_num-base + 1)
                print("GoodAcks: ", recievedAcks)
                #restart timer
                timer.cancel()
                timer = threading.Timer(.001, timerCall)
                timerExpired = False
                base = recieved_sequence_num+1
                timer.start()
        except:
            pass

        if(recievedAcks == len(allData)):
            finishedSending = True





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
returnPckt=make_pkt(100,b'ACK')
def rdt_rcv(recievingSocket):
    global  expected_sequence_Num
    global returnPckt

    while(True):
        #get the packet out of the socket
        rcvPacket, addr=udt_rcv(recievingSocket)

        #extract stuff out of the packet
        data,recieved_sequence_num,chksum = extract(rcvPacket)

        #if the packet is good update the response packet
        print("recieved seq numb: ", recieved_sequence_num)
        if(not corrupt(rcvPacket) and recieved_sequence_num==expected_sequence_Num):
            returnPckt=make_pkt(expected_sequence_Num,b'ACK')
            expected_sequence_Num = (expected_sequence_Num + 1) % 30
            print("the esn is now : ", expected_sequence_Num)
            udt_send(recievingSocket, addr, returnPckt, corruptPercent_server_to_client, loss_Percent_server)
            return data, 0
        else:
            print("Packet error")