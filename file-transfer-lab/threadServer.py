#! /usr/bin/env python3

import sys
sys.path.append("../lib")
import re, socket, params, os
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False),
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("Listening on:", bindAddr)

from threading import Thread, Lock
from encapFramedSock import EncapFramedSock
global flock

used_files = []

flock = Lock()
print(used_files)

def lock_start(filename):
    global flock
    flock.acquire()
    if filename in used_files:
        print("File is currently being used...")
        flock.release()
        sys.exit(1)
    else:
        used_files.append(filename)
        flock.release()

def lock_end(filename):
    used_files.remove(filename)

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("New thread handling connection from", self.addr)
        while True:
            try:
                filename = self.fsock.receive(debug)
                print("Checking server for : ", filename.decode())
                sentfile = filename.decode()
                sentfile = "Received "+ sentfile
                print(sentfile)
                if exists(sentfile):
                    self.fsock.send(b"True",debug)

                else:
                    self.fsock.send(b"False", debug)
                    payload = self.fsock.receive(debug)
                    lock_start(filename)
                    outfile = open(sentfile,"wb")
                    outfile.write(filename)
                    outfile.write(payload)
                    self.fsock.send(b"wrote new file",debug)
                    lock_end(filename)
                    outfile.close()
            except:
                print("Connection lost")
                sys.exit(0)

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()