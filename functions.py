import random

def make_pkt(seq,data):
    #packet format seq,chksum,data

    packet=seq+data
    chksum = GetCheckSum(packet)
    packet=chksum+packet

    return data

def extract(rcvpkt):
    chksum = rcvpkt[0:1] #chksum is 1st and 2nd bit
    seq = rcvpkt[0]  # sequence num should be 4th bit
    pckt=rcvpkt[3:] #packet starts at the 4th bit

    return pckt,seq,chksum


def GetCheckSum(packet):
    chksum=0
    currentIndex = 0
    #go though packet grouping bytes in groups of 2
    while(currentIndex < len(packet)):
        byteslice=packet[currentIndex:currentIndex + 2]


        #convert the byte slice to int
        intslice=int.from_bytes(byteslice, "big")

        #add the integer to the pre existing checksum
        chksum+=intslice

        #if the chksum is greater than 65536 than subtrack 65535
        if(chksum>=65536):
            chksum-=65535
        currentIndex += 2
    # convert integer back to byte slice
    chksum_byte = int.to_bytes(chksum, 2, "big")
    #print("checksum bytes: ",chksum_byte)
    #print("checksum int: ", chksum)
    #print("checksum binary: ", bin(chksum))

    return chksum_byte




#you give it a packet and it corrupts it for you
def coruptPacket(packet):
    corruptpacket =packet+b'corrupt'
    return corruptpacket



#tells you if a packet is corrupt or not
def corrupt(rcvPacket):
    recieved_chksum=rcvPacket[0:1] #checksum is the first two bits

    #take the checksum off of the front of the packt
    packet=rcvPacket[2:] #take the chksum off of the front of the packet

    calculated_chksum=GetCheckSum(packet)

    return (calculated_chksum==recieved_chksum)



