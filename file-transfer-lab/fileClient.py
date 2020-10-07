#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params
#sys.path.append("../framed-echo")
#from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('Could not open socket')
    sys.exit(1)

s.connect(addrPort)

while True:

    filename = input(str("Enter the file name: "))
    # fileName = "testfile.txt"
    filename.strip()

    if filename == "exit":
        sys.exit(0)
    #break
    else:
        if not filename:
            continue

        elif os.path.exists("sentFiles/" + filename):

            s.sendall(filename.encode()) # send file name
            file = open("sentFiles/" + filename, "rb")

            s.sendall(str(os.stat("sentFiles/" + filename).st_size).encode()) # send size

            while True:

                data = file.read(1024)
                s.sendall(data)
                if not data:
                    break
            file.close()

            status = int(s.recv(1024).decode())
            #print(status)

            if status:
                print("File %s received by the server" % filename)
                sys.exit(0)

            else:
                print("File %s was not received by the server" % filename)
                sys.exit(1)
        else:
            print("File %s not found" % filename)

# fileContents = file.read() save contents in file

# framedSend(s, fileContents.encode(), debug)