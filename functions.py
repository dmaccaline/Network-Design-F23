import random
printflag=False
#NOTE: Below values are in % (60 -> 60% chance of corruption or probablility of .6 to corrupt)
corruptPercent_client_to_server = 45
corruptPercent_server_to_client= 0
loss_Percent_server=0
loss_Percent_client=0

def make_pkt(seq,data):
    #packet format =  seq,chksum,data
    #Note: Sequence number 0 is encoded as 00000000 and Sequence number 1 is encoded as 11111111 (255)
    if(seq == 1):
        seq = int.to_bytes(255, 1, "big")
    else:
        seq = int.to_bytes(seq, 1, "big")

    #seq=int.to_bytes(seq, 1, "big")
    packet=seq+data
    chksum = GetCheckSum(packet)
    packet=chksum+packet

    return packet

def extract(rcvpkt):

    chksum = rcvpkt[0:2] #chksum is 1st and 2nd Byte

    seq = rcvpkt[2:3]  # sequence num should be 3rd Byte

    seqinteger = int.from_bytes(seq, "big")

    if(seqinteger == 255):
        seqinteger = 1

    pckt=rcvpkt[3:] #packet starts at the 4th Byte

    return pckt, seqinteger, chksum


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

        #if the chksum is greater than 65536 than subtrack 65535 (this is the decimal equivlent of
        #getting rid of the 17th 1 in binary and the adding 1 on the lsb
        if(chksum>=65536):
            chksum-=65535
        currentIndex += 2
    # convert integer back to byte slice
    chksum_byte = int.to_bytes(chksum, 2, "big")

    return chksum_byte


#you give it a packet and it corrupts it for you
def coruptPacket(packet):
    corruptpacket =packet+b'corrupt'
    return corruptpacket



#tells you if a packet is corrupt or not
def corrupt(rcvPacket):
    recieved_chksum=rcvPacket[0:2] #checksum is the first two bits

    packet=rcvPacket[2:] #take the chksum off of the front of the packet

    calculated_chksum=GetCheckSum(packet)#calculate the actual chksum of the packet so you can compare it
    #to the recieved one

    if(printflag):    print("     recieved chksum: ",recieved_chksum)
    if(printflag):    print("     calculated chksum: ", calculated_chksum)

    return (not(recieved_chksum==calculated_chksum))