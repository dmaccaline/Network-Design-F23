from functions import *


#using this to track what sequnce number the rdt_send function attaches to its packet
sequenceNum=0
def rdt_send(clientSocket,serverName,serverPort,data):
        global sequenceNum
        flag=True

        #make the packet
        sendpkt = make_pkt(['0'],data)

        #basically we keep sending the same packet until we get the response wanted
        if(flag):
            print("     sending sequnce number : ", sequenceNum)
            #udt send packet
            udt_send(clientSocket,(serverName,serverPort),sendpkt)
            # wait to recieve a packet
            rcvpkt, addr = udt_rcv(clientSocket)

            #if the response is bad do the loop again bad=corrupt or wrong sequnce number
            if(corrupt(rcvpkt)):
               flag=False


        #if we get here that means we like the repsonse we got and we can iterate the
        #sequence number and then move on
        sequenceNum = (sequenceNum + 1) % 2




#send the packets corrupting some of them
def udt_send(sendingSocket,destination_addr,packet):

    corruptPercent=5
    randomNum = random.randint(1, 100)

    # if the random number is less than corrupt percent corrupt the packet
    if (randomNum <= corruptPercent):
        packet=coruptPacket(packet)

    #convert the packet back to a byte aray to fit it through the port

    sendingSocket.sendto(packet, destination_addr)

def udt_rcv(recievingSocket):
    while True:
        #recieve the data as a byte array
        data, addr = recievingSocket.recvfrom(2048) # buffer size is 1024 bytes

        return data, addr


expected_sequence_Num=0
sndpkt = make_pkt([0], b'generic response')
def rdt_rcv(recievingSocket):
    global expected_sequence_Num
    global sndpkt
    flag=True
    recievedsequencNUm=0

    while(flag):
        flag = False
        #get the data
        rcvPacket, addr=udt_rcv(recievingSocket)

        #for now just read as 'if bad packet' bad=corrupt or wrong sequnce number
        if(corrupt(rcvPacket)):
            #keep previous response do the loop again
            flag=True
        else:
            #make good response, exit loop
            sndpkt=make_pkt(['0'],b'genericresponse')

        # reply to the data with either "good" repsonse or the previous response
        print("     sending ACK:",expected_sequence_Num)
        udt_send(recievingSocket, addr, sndpkt)


    #if we get here it means the data is good
    #extract the data
    data=extract(rcvPacket)

    #iterate the epected sequence num
    expected_sequence_Num=(expected_sequence_Num+1)%2

    #deliver the data
    return  data, addr