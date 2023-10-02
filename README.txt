Daniel Maccaline, Nathan Grady
Phase 2

Made in Windows using Python 3.11.5



Files submitted
	- README.txt (this file)
	- DesignDoc.md
		- Word file containing details about the program and its execution
	- server.py
		- File containing code for the UDP server, acts as reciever
	- client.py
		- File containing code for the DP client, acts as sender
	- contribution.txt
	    - File containing contributions by each member


File setup:
	- extract zip files with the client.py and server.py to a location on the pc

How to run:
	- Open the file location containing client.py and server.py using the command prompt (terminal)
	- Run the server file first, using the command:
		python server.py
	- Once the server is running, start the client in a seperate terminal window with the following command:
		python client.py
	- NOTE: the server will indicate when it is ready to recieve messages by printing the message "The server is ready to recieve" in the terminal window
		- The client should not be started before this message is printed
		- Note2: once the server is started, the client can be run multiple times without re-starting the server.

Expected output:

Note: <message> is the string passed to the client by the main method in client.py

	- From Server:
		Expect the following on startup:
			- "The server is ready to recieve"
		When client is run, the following is expected:
			- "from connected user: <message>"
			- "Client socket number: <Socket>
			Note the above output occurs each time client is run

	- From Client:
		- "Starting Client with message:  <message>"
		- "from Server:  <message>"
		- "Server socket number: <Socket>


References:
both the client and server use code provided in a class handout, citation provided below and in the corresponding source files headers

