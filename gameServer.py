import sys, cgi, os
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import Physics as p
import random
import json

def nudge():
    return random.uniform( -1.5, 1.5 )

class gameServer(HTTPServer):
    table = None
    prevTableBalls = None
    high = 0
    low = 0
    playerTurn = 1
    game = None

class serverHandler(BaseHTTPRequestHandler):

    # Silences HTTP server POST and GET messages in terminal
    #   Borrowed from: https://stackoverflow.com/questions/53422825/how-do-i-prevent-a-python-server-from-writing-to-the-terminal-window
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        url = urlparse(self.path)
        
        if url.path in ["/index.html"]:
            fp = open('.' + url.path)
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
            fp.close()

        elif url.path in ["/setupBoard"]:

            if self.server.table == None:

                self.server.table = p.Table()
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
                    self.server.table.add_object(b)

                pos = p.Coordinate(displace + 120 + 60, 2000)
                b = p.StillBall(0,pos)
                self.server.table.add_object(b)

            content ={
                "player1Name": self.server.game.player1Name,
                "player2Name": self.server.game.player2Name,
                "turn": self.server.playerTurn,
                "table": self.server.table.svg()
            }

            contentJSON = json.dumps(content)

            self.send_response(200)
            self.send_header("Content-type", "application/JSON")
            self.end_headers()
            self.wfile.write(contentJSON.encode("utf-8"))

        elif url.path in ["/anim"]:

            response = self.server.game.getFrames()

            if response[0] != None:
                self.server.table = self.server.game.db.readTable(response[0])
                
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
            
        elif url.path in ["/checkTable"]:

            ballList = []
            gameOver = 0

            for item in self.server.table:

                if isinstance(item, p.RollingBall):
                    ballList.append(item.obj.rolling_ball.number)
    
                elif isinstance(item, p.StillBall):
                    ballList.append(item.obj.still_ball.number)

            if 0 not in ballList:
                self.server.table.add_object(p.StillBall(0,p.Coordinate(p.TABLE_WIDTH/2,p.TABLE_LENGTH/2)))

            if self.server.high == 0:
                for i in range(1,8):
                    if i not in ballList:
                        if self.server.playerTurn == 1:
                            self.server.low = 1
                            self.server.high = 2
                        else:
                            self.server.low = 2
                            self.server.high = 1

                if self.server.high == 0:
                    for i in range(9,16):
                        if i not in ballList:
                            if self.server.playerTurn == 1:
                                self.server.high = 1
                                self.server.low = 2
                            else:
                                self.server.high = 2
                                self.server.low = 1

            if 8 not in ballList:
                highBallExist = False
                lowBallExist = False

                for i in range(len(ballList)):
                    if ballList[i] in range(1,8):
                        lowBallExist = True
                    elif ballList[i] in range(9,16):
                        highBallExist = True
                
                if highBallExist == False:
                    gameOver = self.server.high
                elif lowBallExist == False:
                    gameOver = self.server.low
                else:
                    if self.server.playerTurn == 1:
                        gameOver = 2
                    else:
                        gameOver = 1


            if self.server.prevTableBalls != None:
                sunkBalls =list(set(ballList).symmetric_difference(set(self.server.prevTableBalls)))
                highBallExist = False
                lowBallExist = False

                for i in range(len(sunkBalls)):
                    if sunkBalls[i] in range(1,8):
                        lowBallExist = True
                    elif sunkBalls[i] in range(9,16):
                        highBallExist = True
                
                if highBallExist == True and self.server.high == self.server.playerTurn:
                    if self.server.playerTurn == 1:
                        self.server.playerTurn = 2
                    else:
                        self.server.playerTurn = 1

                elif lowBallExist == True and self.server.low == self.server.playerTurn:
                    if self.server.playerTurn == 1:
                        self.server.playerTurn = 2
                    else:
                        self.server.playerTurn = 1



            if self.server.playerTurn == 1:
                self.server.playerTurn = 2
            else:
                self.server.playerTurn = 1

            content = {
                "ballList": ballList,
                "gameOver": gameOver,
                "turn": self.server.playerTurn,
                "high": self.server.high,
                "low": self.server.low,
                "table": self.server.table.svg()
            }

            self.server.prevTableBalls = ballList

            contentJSON = json.dumps(content)
            self.send_response(200)
            self.send_header("Content-type", "application/JSON")
            self.end_headers()
            self.wfile.write(contentJSON.encode("utf-8"))

        elif url.path in ["/reset"]:
            self.server.table = p.Table()
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
                self.server.table.add_object(b)

            pos = p.Coordinate(displace + 120 + 60, 2000)
            b = p.StillBall(0,pos)
            self.server.table.add_object(b)
            self.server.playerTurn = 1
            self.server.high = 0
            self.server.low = 0

            content ={
                "player1Name": self.server.game.player1Name,
                "player2Name": self.server.game.player2Name,
                "turn": self.server.playerTurn,
                "table": self.server.table.svg()
            }

            contentJSON = json.dumps(content)

            self.send_response(200)
            self.send_header("Content-type", "application/JSON")
            self.end_headers()
            self.wfile.write(contentJSON.encode("utf-8"))
                    
    def do_POST(self):
        url = urlparse(self.path)

        if url.path in ["/game.html"]:
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': self.headers['Content-Type'],})
            
            self.server.game = p.Game(None,"MyGame",form["player1Name"].value,form["player2Name"].value)

            fp = open('.' + url.path)
            content = fp.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
            fp.close()

        elif url.path in ["/shoot"]:

            data = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
            velx = float(data["velx"].value)
            vely = float(data["vely"].value)

            shotID = self.server.game.shoot(self.server.game.gameName,self.server.game.player1Name,self.server.table,velx,vely)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(str(shotID)))
            self.end_headers()
            self.wfile.write(bytes(str(shotID),"utf-8"))
            
        elif url.path in ["/frames"]:
            data = cgi.FieldStorage(fp=self.rfile, headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
            shotID = int(data["shotID"].value)

            frames = self.server.game.getNumFrames(shotID)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(str(frames)))
            self.end_headers()
            self.wfile.write(bytes(str(frames),"utf-8"))
            
if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("No Port Provided")
        exit()
    
    httpd = gameServer( ( 'localhost', int(sys.argv[1]) ), serverHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()
