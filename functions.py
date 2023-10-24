import random

def make_pkt(seq,data):
    chksum=GetCheckSum(data)
    return data

def extract(rcvpkt):
    #get rid of the header, so just take off the first 17 bits
    data=rcvpkt[16:]
    return rcvpkt


def GetCheckSum(packet):
    chksum=0
    currentIndex = 0
    #create packet list
    while(currentIndex < len(packet)):
        byteslice=packet[currentIndex:currentIndex + 2]


        intslice=int.from_bytes(byteslice, "big")

        #add the integer
        chksum+=intslice

        #if th chksum is greater than 65536 than subtrack 65536
        if(chksum>65536):
            chksum-=65535
        currentIndex += 2
    # convert integer back to byte slice
    chksum = int.to_bytes(chksum, 2, "big")
    print("checksum: ",chksum)



    return 0











#you give it a packet and it corrupts it for you
#corrupt just tells you if it is corrupt or not
def coruptPacket(packet):
    corruptpacket =packet+b'corrupt'
    return corruptpacket



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











def randomize_bytes(byte_string, change_probability):
    """
    Randomly changes bytes in a byte string based on the given change_probability.

    :param byte_string: The input byte string.
    :param change_probability: The probability of changing each byte.
    :return: A byte string with randomly changed bytes.
    """
    # Convert the byte string to a bytearray for mutability
    byte_array = bytearray(byte_string)

    # Generate random indices to change bytes
    indices_to_change = [i for i in range(len(byte_array)) if random.random() < change_probability]

    # Change the selected bytes
    for index in indices_to_change:
        byte_array[index] = bytes([random.randint(0, 255)])

    # Convert the bytearray back to a bytes object
    changed_byte_string = bytes(byte_array)

    return changed_byte_string
