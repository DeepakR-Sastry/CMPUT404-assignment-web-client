#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        x = data.split("\r\n")[0].split()[1]
        return int(x)


    def get_headers(self,data):
        # i dont use this function
        return None

    def get_body(self, data):
        x = data.split("\r\n\r\n")[1]
        return x

    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')


    def parse(self, url):
        # parse the url and set class variables

        # this returns a 6-tuple containing port/hostname/scheme etc
        o = urllib.parse.urlparse(url)

        self.hostName = o.hostname
        self.scheme = o.scheme
        self.path = o.path
        self.port = o.port

        # if path is undefined
        if self.path == "":
            self.path = "/"

        # if port is undefined
        if self.port is None:
            if self.scheme == "https":
                self.port = 443
            if self.scheme == "http":
                self.port = 80


    def GET(self, url, args=None):
        code = 500
        body = ""

        self.parse(url)
        self.connect(self.hostName, self.port)

        header = "GET " + str(self.path) + " HTTP/1.1\r\n" + "Host: "  + str(self.hostName) + "\r\n" + "Accept: */*\r\n" + "Connection: close\r\n\r\n"

        self.sendall(header)
        response = self.recvall(self.socket)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        if args is None:
            args = urllib.parse.urlencode("")
        else:
            args = urllib.parse.urlencode(args)

        self.parse(url)
        self.connect(self.hostName, self.port)

        header = "POST " + str(self.path) + " HTTP/1.1\r\n" + "Host: " + str(self.hostName) + "\r\n" + "Content-Type: application/x-www-form-urlencoded\r\n" + "Content-Length: " + str(len(args)) + "\r\n" + "Connection: close\r\n\r\n" + str(args)

        self.sendall(header)
        response = self.recvall(self.socket)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
