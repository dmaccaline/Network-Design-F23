Phase 1 Req, send bmp file

Client:

EDIT:
  According to the TA in slack earlier, there should be "ack/nack" or acknoledge and not acknoledge.  (assuming I am interpreting this correctly) We DO NOT need to keep track of packet #, as we simply send the packets in order, and wait for acknoledge before the next package is sent.  Below text is still relevent in reference to indicating to the server when the final packet has arrived.  
Edit2:
  After reading the section in the book directed to in the instructions (3.4.1) it specifically mentions that no acknoleddgement is used, as it is assumed in the section that there is a perfectly reliable underlying data transfer.  This assumption is also made in the assignment, as such acknoledgement may not be needed.  May need to ask for clarification from the TA since he mentioned ack/nack as an example of something we need, though he may be referring to future phases.  

Make_Packet 0 splits into 1024B sizes, + Header (number containing order of packets (might not be needed))
  Packet # should be in binary,not sure how many bits to use, maybe 16? (give max numb packets as ~65.5k, max file size of 67,108,864 bits assuming packets of 1024 bits (57 mBit))
  Theoretically can increase packet size if file is larger than max size (this would be fairly trivial to add later)
    Header also needs way to inicate when final packet is sent/recieved to tell server to stop concatenating
      The indication for when at file end may not be needed, as the BMP file has a header with file size, which could be re-used for this purpose
        See https://en.wikipedia.org/wiki/BMP_file_format for details
Send UDP Packet one at a time in loop


Server:

Recieve packet
    Re-assemble in order
	May need to hold on to packet seperaty if arrived out of order, depends on how bmp files are layed out

Functions
 Client main - recieves file as either command line input or hard-coded input (command line preferred)
  Calls Make_Packet, then loops for each packet and sends each to server
 Sever main - Co ntinually recieve packets and assemble.  
  Either assemble as it goes, or store and assemble all at once
    Later would make it easier to handle packages out of order

  Make_Packet - Splits file into smaller parts of fixed size, and creates header for the packets

  Assemble_Packets - re-assembles packets into a file
    Must read header too determine packet order, then remove header and concatenate file together
    
