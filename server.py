#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    

    
    def handle(self):

        #Status reponse that needed
        NotAllowed405 = 'HTTP/1.1 405 Method Not Allowed\r\n'
        NotFound404 = 'HTTP/1.1 404 Not Found\r\n'
        Moved301 = 'HTTP/1.1 301 Moved Permanently\r\n'
        OK200 = 'HTTP/1.1 200 OK\r\n'
        
        #get GET header response
        self.data = self.request.recv(1024).strip().decode('utf-8')

        urlPath = self.getPath()

        if urlPath[-1] == '/':
            urlPath+='index.html'

        # content = self.readFile(path)

        #Status 405
        if self.isGet():
            
            if self.isHTML(urlPath):
                self.request.sendall(bytearray(OK200,'utf-8'))
                content = self.readFile(urlPath)
                self.request.sendall(b'Content-Type: text/html\r\n\r\n')
                self.request.sendall(content)
                            
            elif self.isCss(urlPath):
                self.request.sendall(bytearray(OK200,'utf-8'))
                content = self.readFile(urlPath)
                self.request.sendall(b'Content-Type: text/css\r\n\r\n')
                self.request.sendall(content)

        else:
            #Only deal with GET, if there are POST/PUT/DELETE, return Status Code 405
            self.request.sendall(bytearray(NotAllowed405),'utf-8')

    def isGet(self):
        """
        Return True if the header is GET, if the header is POST/PUT/DELETE, it returns False
        """
        return self.data.split()[0] == 'GET'

    def getPath(self):
        """
        get the path that need to view
        """
        path = self.data.split()[1]
        return path

    def readFile(self, path):
        """
        Return the content of the file as format of byte
        """
        with open('./www'+path,'r') as file:
            content = file.read()
        return bytearray(content,'utf-8')

    def isHTML(self,path):
        return path.endswith('.html')

    def isCss(self, path):
        return path.endswith('.css')

    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
