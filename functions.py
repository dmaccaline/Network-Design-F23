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

def addPacketHeader(packet):
    #get checksum
    checkSum=GetCheckSum(packet)

    return packet





def GetCheckSum(packet):
    return 0