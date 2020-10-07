#! /usr/bin/env python3

import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

def write_file(file, byte, conn, addr):
    try:
        i = 0
        data = ''.encode()
        writer = open(file, 'w+b')

        while i < byte:

            data = conn.recv(1024)
            if not data:
                break
            i += len(data)

        bytearray(data)
        writer.write(data)

        writer.close()
        print("File %s received from %s" % (file, addr))

    except FileNotFoundError:

        print("File not found!")
        conn.sendall(str(0).encode()) # send fail
        sys.exit(1)

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", True), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

#progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
socket.bind(bindAddr)
socket.listen()

print("Waiting to be connected...")
sock, bind = socket.accept()
print('Connected by', bind)

os.chdir("./receivedFiles")

#from framedSock import framedSend, framedReceive

while True:
    conn, addr = socket.accept() 

    if not conn or not addr:
        sys.exit(1)

    if not os.fork():
        print("rec'd: ", addr)
        # receive file name first
        data = conn.recv(1024)
        file = data.decode()

        data_byte = conn.recv(1024).decode() # file byte size

        try:

            data_byte = int(data_byte)

        except ValueError:
            print("Byte size not received")
            conn.sendall(str(0).encode()) # fail status
            sys.exit(1)

        if file:
            write_file(file, data_byte, conn, addr)
            conn.sendall(str(1).encode()) # success status
            sys.exit(0)
        else:
            print("Error")
            conn.sendall(str(0).encode()) # fail status
            sys.exit(1)