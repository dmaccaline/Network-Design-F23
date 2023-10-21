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

def make_pkt(packet,sequenceNumber):
    #get checksum
    checkSum=GetCheckSum(packet)

    return packet


def GetCheckSum(packet):
    return 0

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

def rdt_rcv(recievingSocket):
    while True:
        #print("test")
            data, addr = recievingSocket.recvfrom(1024) # buffer size is 1024 bytes
            return data, addr





def rdt_send(clientSocket,serverName,serverPort,data):


    for i in range (0,len(data)):

        sequenceNum=i%2

        flag=True
        #print(data[i])
        sendpkt = make_pkt(data[i], sequenceNum)

        if(flag):
            #udt send packet
            udt_send(clientSocket,(serverName,serverPort),sendpkt)
            # wait to recieve a packet
            rcvpkt, addr = rdt_rcv(clientSocket)

            if(corrupt(rcvpkt) or (not isAck(rcvpkt,sequenceNum))):
               flag=False


    #send the stop bit
    udt_send(clientSocket, (serverName, serverPort), b'stop')





#tells you if a packet is corrupt or not
def corrupt(rcvPacket):
    return False


#tells you if a packet is acknoledged
def isAck(rcvPckt,sequenceNumber):
    return True