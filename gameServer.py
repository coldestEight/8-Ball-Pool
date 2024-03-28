import sys, cgi, os
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import Physics as p
import random
import json

def nudge():
    return random.uniform( -1.5, 1.5 )

class serverHandler(BaseHTTPRequestHandler):

    table = p.Table()
    game = p.Game(None,"test","playerOne","playerTwo")

    # Silences HTTP server POST and GET messages in terminal
    #   Borrowed from: https://stackoverflow.com/questions/53422825/how-do-i-prevent-a-python-server-from-writing-to-the-terminal-window
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        url = urlparse(self.path)

        if url.path in ["/game.html"]:
            fp = open('.' + url.path)
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
            fp.close()
        
        elif url.path in ["/setupBoard"]:

            displace = 480

            for i in range(1,16):
                if i <= 5:
                    pos = p.Coordinate(displace + i*70 + nudge(), displace+nudge())
                
                elif i <= 9:
                    pos = p.Coordinate(displace + 30 + (i-5)*70 + nudge(), displace + 60 + nudge())
                
                elif i <= 12:
                    pos = p.Coordinate(displace + 60 + (i-9)*70 + nudge(), displace + 120 + nudge())

                elif i <= 14:
                    pos = p.Coordinate(displace + 90 + (i-12)*70 + nudge(), displace + 180 + nudge())

                elif i == 15:
                    pos = p.Coordinate(displace + 120 + (i-14)*70 + nudge(), displace + 240 + nudge())

                
                b = p.StillBall(i, pos)
                self.table.add_object(b)

            pos = p.Coordinate(displace + 120 + 60, 2000)
            b = p.StillBall(0,pos)
            self.table.add_object(b)

            content = self.table.svg()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content,"utf-8"))

    def do_POST(self):
        url = urlparse(self.path)

        if url.path in ["/shoot"]:

            data = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
            velx = float(data["velx"].value)
            vely = float(data["vely"].value)

            shotID = self.game.shoot(self.game.gameName,self.game.player1Name,self.table,velx,vely)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(str(shotID)))
            self.end_headers()
            self.wfile.write(bytes(str(shotID),"utf-8"))


        elif url.path in ["/anim"]:

            data = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD': 'POST'})

            response = self.game.getFrames()

            if response[0] != None:
                self.table = response[0]

            svg = response[1]

            content = {
                "frameCount" : len(svg),
                "frames": svg
            }

            contentJSON = json.dumps(content)

            self.send_response(200)
            self.send_header("Content-type", "application/JSON")
            self.end_headers()
            self.wfile.write(contentJSON.encode("utf-8"))

        elif url.path in ["/frames"]:
            data = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
            shotID = int(data["shotID"].value)

            frames = self.game.getNumFrames(shotID)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(str(frames)))
            self.end_headers()
            self.wfile.write(bytes(str(frames),"utf-8"))

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("No Port Provided")
        exit()
    
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), serverHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()
