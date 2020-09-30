#! /usr/bin/env python3

import socket, sys, re

sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", True), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
socket.bind(bindAddr)
socket.listen()

print("Waiting to be connected...")
sock, addr = socket.accept()
print('Connected by', addr)

from framedSock import framedSend, framedReceive

while True:
    f_name, payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload or not f_name:
        break
    binary_format = bytearray(payload)
    with open('./server/'+f_name.decode(), 'w+b') as nf:
        nf.write(binary_format)
        nf.close()