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

def addPacketHeader(packet,sequenceNumber):
    #get checksum
    checkSum=GetCheckSum(packet)

    return packet


def GetCheckSum(packet):
    return 0

def coruptPacket(packet):
    return packet


#send the packets corrupting some of them
def udt_send(clientSocket,serverName,serverPort,packet,corruptPercent):
    randomNum = random.randint(1, 100)

    # if the random number is less than corrupt percent corrupt the packet
    if (randomNum <= corruptPercent):
        packet=coruptPacket(packet)

    clientSocket.sendto(packet, (serverName, serverPort))




def rdt_send(clientSocket,serverName,serverPort,packet):

    #add a header to the packet
    Hpacket=addPacketHeader(packet,0)

    #udt send packet
    udt_send(clientSocket,serverName,serverPort,Hpacket,0)

    #wait to recieve a reply
    print('here')
    while True:
        #print("test")
        #data, addr = clientSocket.recvfrom(1024) # buffer size is 1024 bytes
        break







