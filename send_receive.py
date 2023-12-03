from functions import *
import threading
import time

timerExpired = False

def timerCall():
    if(printflag):  print("Timer expired")
    global timerExpired
    timerExpired = True
    

#using this to track what sequnce number the rdt_send function attaches to its packet
sequenceNum=0
def rdt_send(clientSocket,serverName,serverPort,allData):
        global sequenceNum
        global timerExpired

        #flag indicates wether we need to do the loop again



        for data in allData:
            flag = True

            #make the packet
            if(printflag):  print("Sending packet")
            sendpkt = make_pkt(sequenceNum,data)
    #
            #Loop until packet recieved (properly acked)
            while(flag):
                #udt send packet
                udt_send(clientSocket,(serverName,serverPort),sendpkt,corruptPercent_client_to_server,loss_Percent_client)


                #Start timer
                timerExpired = False
                #arguments (x, f), after x seconds, call function f
                timer = threading.Timer(.001, timerCall)
                timer.start()
                # Set client socket so recvfrom is not blocking
                clientSocket.setblocking(0)

                #Loop until timer expires
                while(not timerExpired):

                    # Attempt to read from socket.  NOTE: With setvlocking(0) set, will throw error if nothing is ready to recieve
                    try:
                        rcvpkt, addr = clientSocket.recvfrom(2048)

                        #Packet recieved, extract dadta and check if a good ack
                        data, recieved_sequence_num, chksum = extract(rcvpkt)
                        if(printflag):      print("     sent sequnce num: ", sequenceNum)
                        if(printflag):      print("     recivied seq: ", recieved_sequence_num)

                        #if not corrupt and correct sequence number, stop timer, and break from loop (packet successfully sent and acked)
                        if(not (corrupt(rcvpkt)or (not (recieved_sequence_num==sequenceNum)))):
                            if(printflag):   print("Good ack")
                            #Stop timer and change flags when good ack recieved
                            flag = False
                            timer.cancel()

                            #packet send, end function
                            if(printflag): print()
                            break;
                        else:
                            if(printflag):  print("corrupt")

                    except:
                        if(printflag and False):
                            print("Waiting for response")
                        #Nothing recieved, do nothing (loop repeats, to try waiting for data again or for timer expiration)


            #if we get here that means we like the repsonse we got and we can iterate the
            #sequence number and then move on
            if(printflag): print()

            sequenceNum = (sequenceNum + 1) % 2



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
sndpkt = make_pkt(1, b'generic response')
def rdt_rcv(recievingSocket):
    global expected_sequence_Num
    global sndpkt
    flag=True

    while(flag):

        flag = False

        #get the data
        rcvPacket, addr=udt_rcv(recievingSocket)

        # extract the data
        data,recieved_sequence_num,chksum = extract(rcvPacket)

        if(printflag):      print("     expecting sequnce num: ",expected_sequence_Num)
        if(printflag):      print("     recivied seq: ",recieved_sequence_num)

        #for now just read as 'if bad packet' bad=corrupt or wrong sequnce number
        if(corrupt(rcvPacket) or (not (recieved_sequence_num==expected_sequence_Num))):
            #keep previous response do the loop again
            if(printflag):  print("     corrupt")
            flag=True
        else:
            #make good response, exit loop
            sndpkt=make_pkt(expected_sequence_Num,b'')

        # reply to the data with either "good" repsonse or the previous response
        udt_send(recievingSocket, addr, sndpkt,corruptPercent_server_to_client,loss_Percent_server)

    #if we get here it means the data is good

    #iterate the epected sequence num
    expected_sequence_Num=(expected_sequence_Num+1)%2

    #deliver the data
    return data, addr