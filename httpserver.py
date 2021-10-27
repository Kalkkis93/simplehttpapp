import cgi
import time
import shutil
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir
from os.path import join as pjoin
import json


## NEW CODE ADDED 2021
import urllib.parse
## NEW CODE ADDED 2021


hostName = "localhost"
hostPort = 3100

class MyServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        d = self.getData()
        print(json.dumps(d))
        self.wfile.write(bytes("<html><body><h1>POST!</h1></body></html>", "utf-8"))

    def do_GET(self):
        print("=== do_GET/ ===")

        if self.path == "/" or self.path == "/favicon.ico":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            rootdir = 'simplePage.html'
            f = open(rootdir)
            self.wfile.write(bytes(f.read(), "utf-8"))
            f.close()

        elif self.path[:3] == "/go":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><h1>POST!</h1>", "utf-8"))
            self.wfile.write(bytes("<h2>" + self.path[6:] + "</h2>", "utf-8"))
            self.wfile.write(bytes("<span id='dataHere'></span>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

        elif self.path[:5] == "/data":
            d = self.getData()
            print("DATA:", d)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*") 
            self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin") 
            self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
            self.end_headers()
            self.wfile.write(bytes("<html><body><p>", "utf-8"))
            self.wfile.write(bytes(d, "utf-8"))
            #self.wfile.write(bytes("<span id='dataHere'></span>", "utf-8"))
            self.wfile.write(bytes("</p></body></html>", "utf-8"))

        print("Path: " + self.path)
        print("=== /do_GET ===")
        print()

    def do_POST(self):
        print("=== do_POST ===")
        print("Path: " + self.path)
        #print(self.request)
        #print(self.headers)
        #print(self.rfile.read)
        length = int(self.headers["content-length"])

        #vars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)

        ## NEW CODE ADDED 2021
        vars = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        ## NEW CODE ADDED 2021

        varsStr = str(vars)[3:(len(vars) - 10)]
        print(varsStr)
        print("=== do_POST ===")
        print()
        d = self.getData()
        return d

    def getData(p):
        return '{ "name": "test", "data": ["1", "2", "3"] }'


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))