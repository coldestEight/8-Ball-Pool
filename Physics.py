import phylib;
import os
import sqlite3

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAMEINTERVAL = 0.01

# SVG constants
HEADER = """
<svg width="100%" height="100%" viewBox="-25 -25 1400 2750"
 xmlns="http://www.w3.org/2000/svg" 
 xmlns:xlink="http://www.w3.org/1999/xlink">
 <rect width="1350" height="2700" x="0" y="0" fill="#5ab54c" />"""

#C0D0C0

FOOTER = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    def svg(self):
        this = self.obj.still_ball
        if this.number == 0:
            return """ <circle onmousedown="clickBall()" id = "qball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (this.pos.x, this.pos.y, BALL_RADIUS, BALL_COLOURS[this.number])  
        else:  
            return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (this.pos.x, this.pos.y, BALL_RADIUS, BALL_COLOURS[this.number])

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, velocity, acceleration, position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    def svg(self):
        this = self.obj.rolling_ball
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (this.pos.x, this.pos.y, BALL_RADIUS, BALL_COLOURS[this.number])


################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y):
        """
        Constructor function. Requires y position
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;


    def svg(self):
        this = self.obj.hcushion
        if this.y == 0:
            return """ <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />\n"""
        else:
            return """ <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />\n"""
            



################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x):
        """
        Constructor function. Requires x position
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;


    def svg(self):
        this = self.obj.vcushion
        if this.x == 0:
            return """ <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />\n"""
        else:
            return """ <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />\n"""


################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos):
        """
        Constructor function. Requires y position
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0);
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;


    def svg(self):
        this = self.obj.hole
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (this.pos.x, this.pos.y, HOLE_RADIUS)      


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;


    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
        
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                    ball.obj.still_ball.pos.y ) );

                # add ball to table
                new += new_ball;
        
        # return table
        return new;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.9f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def cueball(self):

        cueball = None

        for i in self:
            if isinstance(i,StillBall):
                if i.obj.still_ball.number == 0:
                    cueball = i
        
        return cueball


    def svg(self):
        s = HEADER

        for obj in self:
            if(obj):
                s += obj.svg()

        s += FOOTER
        return s

################################################################################
    
class Database:

    conn = None

    def __init__(self, reset=False):
        
        if reset is True:
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")
        
        self.conn = sqlite3.connect("phylib.db")
        self.createDB()


    def createDB(self):

        cur = self.conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Ball(
                        BALLID  INTEGER NOT NULL,
                        BALLNO  INTEGER NOT NULL,
                        XPOS    FLOAT NOT NULL,
                        YPOS    FLOAT NOT NULL,
                        XVEL    FLOAT,
                        YVEL    FLOAT,
                        PRIMARY KEY(BALLID AUTOINCREMENT))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS TTable(
                        TABLEID     INTEGER NOT NULL,
                        TIME        FLOAT NOT NULL,
                        PRIMARY KEY(TABLEID AUTOINCREMENT))""")

        cur.execute("""CREATE TABLE IF NOT EXISTS BallTable(
                        BALLID      INTEGER NOT NULL,
                        TABLEID     INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball,
                        FOREIGN KEY (TABLEID) REFERENCES TTable)""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Game(
                        GAMEID      INTEGER NOT NULL,
                        GAMENAME    VARCHAR(64),
                        PRIMARY KEY(GAMEID AUTOINCREMENT))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS TableShot(
                        TABLEID     INTEGER NOT NULL,
                        SHOTID      INTEGER NOT NULL,
                        FOREIGN KEY(TABLEID) REFERENCES TTable,
                        FOREIGN KEY(SHOTID) REFERENCES Shot
                        )""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Player(
                        PLAYERID    INTEGER NOT NULL,
                        GAMEID      INTEGER NOT NULL,
                        PLAYERNAME  VARCHAR(64) NOT NULL,
                        PRIMARY KEY(PLAYERID AUTOINCREMENT),
                        FOREIGN KEY(GAMEID) REFERENCES Game)""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Shot(
                        SHOTID      INTEGER NOT NULL,
                        PLAYERID    INTEGER NOT NULL,
                        GAMEID          INTEGER NOT NULL,
                        PRIMARY KEY (SHOTID AUTOINCREMENT),
                        FOREIGN KEY(PLAYERID) REFERENCES Player,
                        FOREIGN KEY(GAMEID) REFERENCES Game)""")
        
        cur.execute("""CREATE INDEX IF NOT EXISTS ballIndex ON Ball(BallID)""")
        cur.execute("""CREATE INDEX IF NOT EXISTS TableIndex ON TTable(TableID) """)
        cur.execute("""CREATE INDEX IF NOT EXISTS ballTableIndex ON BallTable(BallID,TableID) """)

        cur.close()
        self.conn.commit()



    def readTable(self, tableID):

        newTable = Table()

        cur = self.conn.cursor()

        tableData = None

        tableData = cur.execute("SELECT * from  BallTable, Ball, TTable WHERE(BallTable.TABLEID = %d AND Ball.BALLID = BallTable.BALLID AND TTable.TABLEID = %d)"%(tableID+1, tableID+1))

        dataEntry = tableData.fetchone()

        if dataEntry == None:
            return None

        newTable.time = dataEntry[8]

        while dataEntry != None:
            
            if dataEntry[6] == None or (dataEntry[6] == dataEntry[7] == 0):
                toAdd = StillBall(dataEntry[3], Coordinate(dataEntry[4],dataEntry[5]))
                newTable += toAdd
            else:
                vx = dataEntry[6]
                vy = dataEntry[7]

                acc = calcAcceleration(vx,vy)

                toAdd = RollingBall(dataEntry[3], Coordinate(dataEntry[4],dataEntry[5]),Coordinate(vx,vy),acc)
                newTable += toAdd

            dataEntry = tableData.fetchone()

        cur.close()
    
        return newTable


    def writeTable(self, table):
        
        cur = self.conn.cursor()

        cur.execute("INSERT INTO TTable VALUES(NULL, %f)"%(table.time))
        tableID = cur.lastrowid

        data = ""

        for item in table:
        
            if isinstance(item,RollingBall):
                cur.execute("""INSERT INTO Ball VALUES(NULL,%d,%f,%f,%f,%f)"""%(item.obj.rolling_ball.number, item.obj.rolling_ball.pos.x, item.obj.rolling_ball.pos.y, item.obj.rolling_ball.vel.x,item.obj.rolling_ball.vel.y))
                cur.execute("""INSERT INTO BallTable VALUES(%d,%d)"""%(cur.lastrowid,tableID))

            elif isinstance(item,StillBall):
                cur.execute("""INSERT INTO Ball VALUES(NULL,%d,%f,%f,NULL,NULL)"""%(item.obj.still_ball.number, item.obj.still_ball.pos.x, item.obj.still_ball.pos.y))
                cur.execute("""INSERT INTO BallTable VALUES(%d,%d)"""%(cur.lastrowid,tableID))


        cur.close()
        return tableID-1
    

    def getGame(self, gameID):
        
        cur = self.conn.cursor()
        
        data = cur.execute("SELECT * FROM Game, Player WHERE(Game.GAMEID = %d AND Player.GAMEID = Game.GAMEID)"%(gameID)).fetchall()

        cur.close()
        self.conn.commit()

        return data

    def setGame(self, gameName, player1Name, player2Name):

        cur = self.conn.cursor()

        cur.execute("""INSERT INTO Game VALUES(NULL,"%s")"""%(gameName))

        id = cur.lastrowid

        cur.execute("""INSERT INTO Player VALUES(NULL, %d, "%s")"""%(id,player1Name))
        cur.execute("""INSERT INTO Player VALUES(NULL, %d, "%s")"""%(id,player2Name))

        cur.close()
        self.conn.commit()

        return id


    def newShot(self, playerName, gameName):

        cur = self.conn.cursor()

        playerData = cur.execute("""SELECT PLAYERID FROM Player WHERE(Player.PLAYERNAME = "%s")"""%(playerName)).fetchone()
        gameData = cur.execute("""SELECT GAMEID FROM Game WHERE(Game.GAMENAME = "%s")"""%(gameName)).fetchone()
        
        if playerData == None:
            print("Player not Found")
            return
        
        if gameData == None:
            print("Game not Found")
            return

        playerID = playerData[0]
        gameID = gameData[0]

        cur.execute("""INSERT INTO Shot VALUES(NULL, %d,%d)"""%(playerID,gameID))

        shotID = cur.lastrowid

        cur.execute

        cur.close()
        self.conn.commit()

        return shotID-1
    
    def saveShotTable(self, tableID, shotID):

        cur = self.conn.cursor()

        cur.execute("INSERT INTO TableShot VALUES(%d,%d)"%(tableID+1,shotID+1))

        cur.close()
        


    def close(self):
        self.conn.commit()
        self.conn.close()

################################################################################
        
class Game:

    gameID = 0
    gameName = None
    player1Name = None
    player2Name = None
    db = None
    frameSet = []

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):

        self.db = Database()

        if gameID != None and gameName == player1Name == player2Name == None:
            
            data = self.db.getGame(gameID+1)
            print(data)
            if data != []:
                self.gameName = data[0][1]
                self.player1Name = data[0][4]
                self.player2Name = data[1][4]

        
        elif gameName != None and player1Name != None and player2Name != None and gameID == None:
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.gameName = gameName
            self.gameID = self.db.setGame(gameName,player1Name,player2Name)-1

        else:
            raise TypeError("Invalid Parameters")
        

    def __del__(self):
        self.db.close()
        
    
    def __str__(self):
        return """Game ID: %d\nGame Name %s
Player1Name: %s\nPlayer2Name: %s\n"""%(self.gameID, self.gameName, self.player1Name,self.player2Name)
        

    def shoot(self, gameName, playerName, table, xvel, yvel):

        cueball = table.cueball()

        if cueball == None:
            return

        shotID = self.db.newShot(playerName, gameName)

        posx = cueball.obj.still_ball.pos.x
        posy = cueball.obj.still_ball.pos.y

        acc = calcAcceleration(xvel,yvel)

        cueball.type = phylib.PHYLIB_ROLLING_BALL
        cueball.obj.rolling_ball.pos = Coordinate(posx,posy)
        cueball.obj.rolling_ball.vel = Coordinate(xvel,yvel)
        cueball.obj.rolling_ball.acc = acc

        startTime = table.time
        newTable = table.segment()

        while newTable != None:
        
            elapsedTime = newTable.time - startTime - table.time
            numFrames = int(elapsedTime//FRAMEINTERVAL)

            for i in range(numFrames):
                #call roll on table (use frame*framinterval), save in new obj
                workingTable = table.roll(i*FRAMEINTERVAL)
                #set time of the result to start time + frame*frameinterval
                workingTable.time = round(table.time + (FRAMEINTERVAL*i),2)
                #save the result table with writetable
                tableID = self.db.writeTable(workingTable)
                #save the shot in shottable
                self.db.saveShotTable(tableID,shotID)
            
            

            table = newTable
            newTable = table.segment()

        self.db.conn.commit()
        return shotID
    
    def getFrames(self):

        svgList = []
        table = None

        for i in range(len(self.frameSet)):

            tableID = self.frameSet[i][0]
            temp = self.db.readTable(tableID)
            if(temp != None):
                table = temp
                svgList.append(table.svg())

        response = [table, svgList]

        return response

    def getNumFrames(self, shotID):
        cur = self.db.conn.cursor()

        data = cur.execute("SELECT TTable.TableID FROM TTable, TableShot WHERE (TableShot.ShotID = %d AND TTable.TableID = TableShot.TableID)"%(shotID+1)).fetchall()
        
        self.frameSet = data
        return len(data)




def calcAcceleration(x,y):

    vel = Coordinate(x,y)

    speed = phylib.phylib_length(vel)

    if speed != 0:
        xacc = -(x / speed) * DRAG
        yacc = -(y / speed) * DRAG

    if abs(x) < VEL_EPSILON:
        xacc = 0

    if abs(y) < VEL_EPSILON:
        yacc = 0

    acc = Coordinate(xacc,yacc)

    return acc