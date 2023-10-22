import random

def byte_array_to_binary_array(byte_array):
    binary_array = []

    for byte in byte_array:
        binary_representation = bin(byte)[2:]  # Convert byte to binary and remove '0b' prefix
        binary_representation = '0' * (8 - len(binary_representation)) + binary_representation  # Pad with leading zeros
        binary_array.extend(list(binary_representation))  # Append each binary digit to the result list

    return binary_array

def binary_array_to_byte_array(binary_array):
    byte_array = bytearray()
    binary_string = ''.join(binary_array)  # Convert the binary array to a single string

    # Convert the binary string back to bytes (8 bits at a time)
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        byte_value = int(byte, 2)  # Convert the binary string to an integer
        byte_array.append(byte_value)  # Append the byte to the result bytearray

    return byte_array

def make_pkt(ACKorNAK,packet,sequenceNumber):
    #get checksum
    checkSum=GetCheckSum(packet)

    return packet


def GetCheckSum(packet):
    return 0


#you give it a packet and it corrupts it for you
#corrupt just tells you if it is corrupt or not
def coruptPacket(packet):
    return packet


#send the packets corrupting some of them
def udt_send(sendingSocket,destination_addr,packet):
    corruptPercent=0
    randomNum = random.randint(1, 100)

    # if the random number is less than corrupt percent corrupt the packet
    if (randomNum <= corruptPercent):
        packet=coruptPacket(packet)

    sendingSocket.sendto(packet, destination_addr)

def udt_rcv(recievingSocket):
    while True:
        data, addr = recievingSocket.recvfrom(1024) # buffer size is 1024 bytes
        return data, addr



#using this to track wich sequence number the rdt_rcv function is looking for
expected_sequence_Num=0
def rdt_rcv(recievingSocket):
    global expected_sequence_Num
    flag=True
    recievedsequencNUm=0

    #i think you have to start with sort of a generic "bad" response in case the first frame is bad
    sndpkt=make_pkt('Ack',b'0',0)

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
            sndpkt=make_pkt('ack',b'generic response',0)

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



#using this to track what sequnce number the rdt_send function attaches to its packet
sequenceNum=0
def rdt_send(clientSocket,serverName,serverPort,data):
        global sequenceNum
        flag=True



        #make the packet
        sendpkt = make_pkt(0,data, sequenceNum)

        #basically we keep sending the same packet until we get the response wanted
        if(flag):
            print("     sending sequnce number : ", sequenceNum)
            #udt send packet
            udt_send(clientSocket,(serverName,serverPort),sendpkt)
            # wait to recieve a packet
            rcvpkt, addr = udt_rcv(clientSocket)

            #if the response is bad do the loop again bad=corrupt or wrong sequnce number
            if(corrupt(rcvpkt) or (not isAck(rcvpkt,sequenceNum))):
               flag=False


        #if we get here that means we like the repsonse we got and we can iterate the
        #sequence number and then move on
        sequenceNum = (sequenceNum + 1) % 2





#tells you if a packet is corrupt or not
def corrupt(rcvPacket):
    return False


#tells you if a packet is acknoledged
def isAck(rcvPckt,sequenceNumber):
    return True

def extract(rcvpkt):
    data=rcvpkt
    return data