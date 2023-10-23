import random

def make_pkt(seq,data):
    return data

def extract(rcvpkt):
    #get rid of the header, so just take off the first 17 bits
    data=rcvpkt[16:]
    return rcvpkt


def GetCheckSum(packet):
    #for now just retrun a 16 bit number
    return [0,'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']


#you give it a packet and it corrupts it for you
#corrupt just tells you if it is corrupt or not
def coruptPacket(packet):
    corruptPercent = 5

    for i in range (0,len(packet)):
        randomNum = random.randint(1, 100)
        # if the random number is less than corrupt percent corrupt the packet
        if (randomNum <= corruptPercent):
            packet[i]=not packet[i]
    return packet

#tells you if a packet is corrupt or not
def corrupt(rcvPacket):
    return False



#might need these if I have to work with the packets as bit arays rather than byte arrays
def byte_array_to_binary_array(byte_array):
    bool_array = []

    for byte in byte_array:
        for i in range(7, -1, -1):
            bit = (byte >> i) & 1  # Extract each bit from the byte
            bool_array.append(bool(bit))  # Convert the bit to a Boolean value

    return bool_array

def binary_array_to_byte_array(bool_array):
    byte_array = bytearray()

    # Convert the boolean values to bytes (8 bits at a time)
    for i in range(0, len(bool_array), 8):
        byte_bools = bool_array[i:i + 8]
        byte_value = 0
        for j, bit in enumerate(byte_bools):
            if bit:
                byte_value |= (1 << (7 - j))
        byte_array.append(byte_value)

    return byte_array