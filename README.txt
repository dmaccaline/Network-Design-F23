 Daniel Maccaline, Nathan Grady
Phase 2

Made in Windows using Python 3.11.5


Files submitted
	- README.txt (this file)
	- DesignDoc.docx
		- Word file containing details about the program and its execution
	- server.py
		- File containing code for the UDP server, acts as reciever
	- client.py
		- File containing code for the UDP client, acts as sender
	- send_recieve.py
		- File containing main sending and recieving functions, notable rdt_send and rdt_recieve.  Used by client and server
	- functions.py
		- File containing functions used for making packet headers, corrupting packets, and calculating checksums
		- File also contains variables to control corruption chances and debug output
	- contribution.txt
	    - File containing contributions by each member


File setup:
	- extract zip files with the client.py and server.py to a location on the pc

How to run:
	- Open the file location containing client.py and server.py using the command prompt (terminal)
	- Run the server file first, using the command:
		server.py
	-NOTE: Server must be restarted after each run

	- Once the server is running, start the client in a seperate terminal window with the following command:
		python client.py
	  Running the client will open a file select window.  From this window, select a bmp file.

	- NOTE: the server will indicate when it is ready to recieve messages by printing the message "The server is ready to recieve" in the terminal window
		- The client should not be started before this message is printed
		
Expected output:
Both of the below assume the printFlag variable in functions.py is false. See design doc for output when debug output is true
    -Server output:
        Initially the server will print "The server is ready to recieve"
        After the client is run, the server will output:
          Finished recieving file
          File opened in seperate window
        Once these are printed, a new windows with the image should have opened (by default, will use photos on windows

    -Client output:
        Will open a file select window when run.  From this, select a BMP file
        When complete, prints:
          Finished sending file
          start: [Time, y-m-d hr-min-s-ms]    end: [Time, y-m-d hr-min-s-ms]
          total time: [hr-min-s-ms]
	Note times are reported in 24 hr time

Additional note:
   The server file will create the file temp.bmp.  This is the file opened and used to display the file that is recieved from the client
   This file is overridden each time a new client is run.

