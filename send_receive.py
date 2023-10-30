from functions import *

#using this to track what sequnce number the rdt_send function attaches to its packet
sequenceNum=0
def rdt_send(clientSocket,serverName,serverPort,data):
        global sequenceNum
        flag=True

        #make the packet
        sendpkt = make_pkt(sequenceNum,data)
#
        #basically we keep sending the same packet until we get the response wanted
        while(flag):
            #udt send packet
            udt_send(clientSocket,(serverName,serverPort),sendpkt,corruptPercent_client_to_server)
            # wait to recieve a packet
            rcvpkt, addr = udt_rcv(clientSocket)

            #extract the data from the packet
            data, recieved_sequence_num, chksum = extract(rcvpkt)
            if(printflag):      print("     sent sequnce num: ", sequenceNum)
            if(printflag):      print("     recivied seq: ", recieved_sequence_num)

            flag=False
            #if the recieved packet is corrupt  or the wrong sequnce number do the loop again
            if(corrupt(rcvpkt)or (not (recieved_sequence_num==sequenceNum))):
                if(printflag):      print("corrupt")
                flag=True

#Test
        #if we get here that means we like the repsonse we got and we can iterate the
        #sequence number and then move on
        if(printflag): print()

        sequenceNum = (sequenceNum + 1) % 2



#send the packets corrupting some of them
def udt_send(sendingSocket,destination_addr,packet,corruptPercent):

    randomNum = random.randint(1, 100)

    # if the random number is less than corrupt percent corrupt the packet
    if (randomNum <= corruptPercent):
        packet=coruptPacket(packet)

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
        udt_send(recievingSocket, addr, sndpkt,corruptPercent_server_to_client)

    #if we get here it means the data is good

    #iterate the epected sequence num
    expected_sequence_Num=(expected_sequence_Num+1)%2

    #deliver the data
    return data, addr