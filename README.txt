Phase 1 Req, send bmp file

Client:

Make_Packet 0 splits into 1024B sizes, + Header (number containing order of packets (might not be needed))
    Header also needs way to inicate when final packet is sent/recieved to tell server to stop concatenating
Send UDP Packet one at a time


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