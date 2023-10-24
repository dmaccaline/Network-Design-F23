import random

def make_pkt(seq,data):
    chksum=GetCheckSum(data)
    return data

def extract(rcvpkt):
    #get rid of the header, so just take off the first 17 bits
    pckt=rcvpkt
    seq=0
    chksum=0



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

        #if th chksum is greater than 65536 than subtrack 65535
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
#corrupt just tells you if it is corrupt or not
def coruptPacket(packet):
    corruptpacket =packet+b'corrupt'
    return corruptpacket



#tells you if a packet is corrupt or not
def corrupt(rcvPacket):
    return False



