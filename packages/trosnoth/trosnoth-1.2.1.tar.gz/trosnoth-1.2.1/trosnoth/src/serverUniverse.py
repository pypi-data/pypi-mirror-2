# Trosnoth (UberTweak Platform Game)
# Copyright (C) 2006-2009 Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

'''serverUniverse.py - defines anything that the server needs to know about
the running of the universe. The server should never require pygame to be
imported.'''

import struct
import random

from twisted.internet import reactor

from trosnoth.src.utils.utils import timeNow
from trosnoth.src.utils.checkpoint import checkpoint
from trosnoth.src.model import modes
from trosnoth.src.model.universe_base import GameState
from trosnoth.src.model.transaction import TransactionState

# TODO: Callbacks/callLaters should validate server-side before sending to
# everyone; make sure the player hasn't left since calling.

# TODO: Remove unused functions (probably carried over from universe.py)

class Team(object):
    '''Represents a team of the game'''

    opposingTeam = None

    def __init__(self, teamID):
        self.currentTransaction = None
        self.numOrbsOwned = 0
        self.teamStars = 0
        self.connIds = {}
        self.captain = None
        self.ready = False

        if (not isinstance(teamID, str)) or len(teamID) != 1:
            raise TypeError, 'teamID must be a single character'
        self.id = teamID

        if teamID == "A":
            self.teamName = "Blue"
        else:
            self.teamName = "Red"
        
    def __repr__(self):
        return '%s team' % self.teamName

    def teamReady(self, initiator = None):
        if initiator == self.captain and not self.ready:
            self.ready = True
            return True
        return False

    def makeCaptain(self, player):
        if not self.captain:
            self.captain = player
            return True
        return False

    def orbLost(self):
        '''Called when a orb belonging to this team has been lost'''
        self.numOrbsOwned -= 1

    def orbGained(self):
        '''Called when a orb has been attributed to this team'''
        self.numOrbsOwned += 1

    def checkWon(self):
        '''Returns whether the team has won the game (True = Won Game)'''
        return self.opposingTeam.numOrbsOwned == 0

    def removeStars(self, stars):
        if stars == 0:
            return
        self.teamStars -= stars
        transaction = self.currentTransaction
        if transaction and transaction.state == TransactionState.Open and \
           self.teamStars < transaction.requiredStars:
            transaction.abandon()

    def playerDie(self, player):
        '''Allows the team object to know whether the transaction is still
        valid. Must be called before the player has their stars set to 0'''
        self.removeStars(player.stars)
        transaction = self.currentTransaction
        if transaction:
            if transaction.purchasingPlayer == player:
                # This player started the transaction: kill it.
                transaction.abandon()
            transaction.removeStars(player)
    
    def addStar(self):
        self.teamStars += 1

    def addAddress(self, pId, connId):
        self.connIds[pId] = connId

    def isCaptain(self, player):
        return player == self.captain

    def leave(self, player):
        '''Cleans up after the leaving player.'''
        del self.connIds[player.id]
        self.playerDie(player)
        player.currentZone.removePlayer(player)
        if self.captain == player:
            self.captain = None
            self.ready = False

    def hasAddress(self, connId):
        return connId in self.connIds.values()

    @staticmethod
    def setOpposition(teamA, teamB):
        teamA.opposingTeam = teamB
        teamB.opposingTeam = teamA

    @staticmethod
    def determineWinner(teamA, teamB):
        if teamA.numOrbsOwned > teamB.numOrbsOwned:
            return teamA
        elif teamA.numOrbsOwned < teamB.numOrbsOwned:
            return teamB
        else:
            return None
    
class Universe(object):
    '''Universe(netServer)
    Keeps track of whatever the server needs to know about what's going on.'''

    # The dimensions of zones. See diagram below.
    halfZoneHeight = 384        # a / 2
    zoneBodyWidth = 1024        # b
    zoneInterfaceWidth = 512    # c

    # This diagram explains the dimensions defined above.
    #     \___________/ _ _ _ _
    #     /           \       ^
    #    /             \      |
    # __/               \___  a
    #   \               /|    |
    #    \             / |    |
    #     \___________/ _|_ _ v
    #     /|         |\  | 
    #      |<-- b -->|<c>|

    # The size of players and shots.
    halfPlayerSize = (13, 19)
    halfShotSize = (5, 5)

    def __init__(self, netServer, timeLimit):
        '''Initialises the universe. the timeLimit parameter is the duration of
        the game in minutes'''
        self.gameState = GameState.PreGame
        self.winner = None
        self.gameTimeLimit = 60 * timeLimit
        # Initialise
        self.zonesToReset = []
        self.playerWithId = {}
        self.teamWithId = {}
        self.zoneWithId = {}

        self.teams = (Team('A'), Team('B'))
        Team.setOpposition(self.teams[0], self.teams[1])
        if netServer.settings['testMode']:
            self.teams[0].teamStars = 100
            self.teams[1].teamStars = 100
        
        for t in self.teams:
            self.teamWithId[t.id] = t
                
        # Set up zones
        halfMapWidth = netServer.settings['halfMapWidth']
        mapHeight = netServer.settings['mapHeight']
        
        totalWidth = halfMapWidth * 2 + 1
        middleHeight = ((halfMapWidth - 1) % 2) + 1 + mapHeight
        
        if middleHeight == mapHeight + 2:
            self.highExists = True
        else:
            self.highExists = False

        # List of all zones:
        self.zones = set()

        # Zones shall also be stored as a multidimensional array
        # in the following format of column/vertical position:
        #    0   1   2   3   4   5   6
        # 0 -/a  a  a\-  -  -/d  d  d\-
        # 1 -\a  a  a/c  c  c\d  d  d/-
        # 2 -/b  b  b\c  c  c/e  e  e\-
        # 3 -\b  b  b/-  -  -\e  e  e/-
        # so that the players' currentZone can more easily be calculated (in
        # the getMapBlockIndices procedure below)
        
        # This will be stored in the format of a list of lists of MapBlocks.
        # The most encompassing list will store the rows.
        # Each "row" will be a list of blocks.
        # Each "block" will be an instance of a subclass of MapBlock.

        self.zoneBlocks = []
        blockTypes = (BottomBodyMapBlock, ForwardInterfaceMapBlock, \
                      TopBodyMapBlock, BackwardInterfaceMapBlock)
        y = 0

        # Decide which type of block to start with.
        if halfMapWidth % 2 == 0:
            nextBlock = 1
        else:
            nextBlock = 3

        prevRow = None
        # Initialise self.zoneBlocks
        for i in range(middleHeight * 2):
            row = []
            x = 0
            bodyBlock = None
            for j in range(totalWidth):
                # Add an interface.
                blockType = blockTypes[nextBlock]
                ifaceBlock = blockType(self, x, y, None, None)
                row.append(ifaceBlock)
                # Link with previous block.
                if bodyBlock:
                    ifaceBlock.blockLeft = bodyBlock
                    bodyBlock.blockRight = ifaceBlock
                if prevRow:
                    ifaceBlock.blockAbove = prevRow[2*j]
                    prevRow[2*j].blockBelow = ifaceBlock
                
                x = x + self.zoneInterfaceWidth
                nextBlock = (nextBlock + 1) % 4
                
                # Add a body block.
                blockType = blockTypes[nextBlock]
                bodyBlock = blockType(self, x, y, None)
                row.append(bodyBlock)
                # Link with previous block.
                bodyBlock.blockLeft = ifaceBlock
                ifaceBlock.blockRight = bodyBlock
                if prevRow:
                    bodyBlock.blockAbove = prevRow[2*j+1]
                    prevRow[2*j+1].blockBelow = bodyBlock
                
                x = x + self.zoneBodyWidth
                nextBlock = nextBlock + 1

            # Add the last interface.
            blockType = blockTypes[nextBlock]
            ifaceBlock = blockType(self, x, y, None, None)
            row.append(ifaceBlock)
            # Link with previous block.
            ifaceBlock.blockLeft = bodyBlock
            bodyBlock.blockRight = ifaceBlock
            if prevRow:
                ifaceBlock.blockAbove = prevRow[2*totalWidth]
                prevRow[2*totalWidth].blockBelow = ifaceBlock
            
            self.zoneBlocks.append(row)
            y = y + self.halfZoneHeight

            prevRow = row

        # height: low means the column is of height mapHeight
        # mid means it is mapHeight + 1, high means mapHeight + 2 (middleHeight)

        # height starts (and ends) at low in every case.
        height = "low"

        # numSoFar keeps track of the number of zones created so far.
        numSoFar = 0

        ''' To calculate adjacent zones, the zones were conceptualised in the
         following pattern, counting downwards by column, then left to right:
         (assuming mapHeight = 3, halfMapWidth = 2)
              7
            3    12
         0    8     16
            4    13
         1    9     17
            5    14
         2    10    18
            6    15
              11

        '''

        '''In order to create each of the zones, we will iterate firstly through
        each of the columns, then through each of the zones in each column. This
        allows us to calculate adjacent zones based on column height.'''

        # Keep track of where the zones should be put.
        xCoord = self.zoneInterfaceWidth + int(self.zoneBodyWidth / 2)
        
        # Iterate through each column:
        for i in range(0, totalWidth):
            # Determine number of zones in the current column
            if height == "low":
                colHeight = mapHeight
            elif height == "mid":
                colHeight = mapHeight + 1
            elif height == "high":
                colHeight = mapHeight + 2

            # Calculate y-coordinate of the first zone in the column.
            if height == "low" and self.highExists:
                yCoord = self.halfZoneHeight
            elif (height == "mid" and self.highExists) or \
                 (height == "low" and not self.highExists):
                yCoord = 0
            elif height == "high" or \
                 (height == "mid" and not self.highExists):
                yCoord = -self.halfZoneHeight

            prevZone = None

            # Iterate through each zone in the column
            for j in range(0, colHeight):

                # Determine Team, and create a zone.
                if i < halfMapWidth:
                    team = self.teams[0]
                elif i > (halfMapWidth):
                    team = self.teams[1]
                else:
                    team = None

                newZone = Zone(self, team)

                # Tell the team object that it owns one more zone
                if team:
                    team.orbGained()
                
                # Determine co-ordinates of the zone's orb (middle of zone)
                yCoord = yCoord + 2 * self.halfZoneHeight
                
                newZone.yCoord = yCoord
                newZone.xCoord = xCoord

                # Link this zone to the zone above.
                if prevZone:
                    prevZone.adjacentZones.add(newZone)
                    newZone.adjacentZones.add(prevZone)
                    
                # Add zone to list of zones
                newZone.id = numSoFar
                newZone.universe = self
                self.zones.add(newZone)
                self.zoneWithId[numSoFar] = newZone


                
                # Add zone to zoneBlocks
                if self.highExists and height == "low":
                    startRow = 2 + j * 2
                elif (self.highExists and height == "mid") or \
                     (not self.highExists and height == "low"):
                    startRow = 1 + j * 2
                elif height == "high" or \
                     (not self.highExists and height == "mid"):
                    startRow = 0 + j * 2
                else:
                    raise Exception, "There's an error in zoneBlocks allocation"

                startCol = i * 2
                # Put new zone into zoneBlocks, and connect it to zones left.
                for y in range(startRow, startRow+2):
                    self.zoneBlocks[y][startCol+2].zone1 = newZone
                    self.zoneBlocks[y][startCol+1].zone = newZone
                    block = self.zoneBlocks[y][startCol]
                    block.zone2 = newZone
                    
                    if block.zone1:
                        # Connect this block to the block to the left.
                        block.zone1.adjacentZones.add(newZone)
                        newZone.adjacentZones.add(block.zone1)

                        # Make sure the block is not divided.
                        block.blocked = False

                # If block is at the top of a column, it must have a roof.
                if not prevZone:
                    self.zoneBlocks[startRow][startCol+1].blocked = True
                
                numSoFar = numSoFar + 1
                prevZone = newZone

            # Make sure that the bottom zone in each column has a floor.
            self.zoneBlocks[startRow+1][startCol+1].blocked = True

            # Advance x-coordinate.
            xCoord = xCoord + self.zoneBodyWidth + self.zoneInterfaceWidth

            # Determine how high the next column will be:
            if height == "low":
                if i == totalWidth - 1:
                    height = None
                else:
                    height = "mid"
            elif height == "mid":
                if i == halfMapWidth - 1:
                    height = "high"
                else:
                    height = "low"
            elif height == "high":
                height = "mid"
        
        for blockList in self.zoneBlocks:
            blockListLength = len(blockList)
            for i in range(blockListLength):
                mirror = blockList[blockListLength - i - 1]
                if mirror == blockList[i]:
                    mirror = None
                blockList[i].oppositeBlock = mirror


        # Zone initialisation and calculations end here.

        self.currentTime = None
        self.timeOutCaller = None
        self.gameOverTime = None
        self.netServer = netServer
        self.gameMode = "Normal"

    def setGameMode(self, mode):
        try:
            getattr(modes.GameMode(Shot, None, None), mode)()
        except AttributeError:
            print 'No such gameMode'
            return False

        self.gameMode = mode
        print 'Server: set game mode to ' + mode
        self.netServer.sendGameMode()
        return True

    def timeLeft(self):
        if self.gameState != GameState.InProgress or self.gameTimeLimit == 0:
            return None
        else:
            return self.currentTime + self.gameTimeLimit - timeNow()

    def gameStart(self):
        self.gameState = GameState.InProgress
        self.currentTime = timeNow()
        if self.gameTimeLimit > 0:
            self.timeOutCaller = reactor.callLater(self.gameTimeLimit, self.timeOut)
        self.netServer.gameStart()

    def timeOut(self):
        '''Called by the reactor when the game time limit has expired'''
        if self.gameState != GameState.InProgress:
            return

        winner = Team.determineWinner(self.teams[0], self.teams[1])
        self.netServer.gameOver(winner, True)
        checkpoint('ServerUniverse: time has run out')


        
    def shotWithId(self, pId, sId):
        try:
            return self.playerWithId[pId].shots[sId]
        except:
            return None

    def checkFinished(self):
        '''Checks to see if the game has been won'''
        if self.gameState == GameState.InProgress:
            for team in self.teams:
                if team.checkWon():
                    self.netServer.gameOver(team)
                    checkpoint('ServerUniverse: team has won')
                    if self.timeOutCaller is not None:
                        self.timeOutCaller.cancel()
                    return

    def getRandomZone(self, team):
        '''Returns a random zone of which the team owns the orb.
        Assume that the game is not over.'''
        while True:
            x = random.randrange(0, len(self.zoneWithId))
            zone = self.zoneWithId[x]
            if zone.orbOwner == team:
                return zone
    
    def newPlayer(self, player):
        '''Adds this player to this universe.'''
        # Remember this player.
        self.playerWithId[player.id] = player

    def checkStart(self):
        '''Checks to see if both teams are ready'''
        start = True
        for i in (0,1):
            start = start and self.teams[i].ready
        return start

##        # Make sure player knows its zone
##        i, j = self.getMapBlockIndices(*player.pos)
##        try:
##            player.currentMapBlock = self.zoneBlocks[i][j]
##        except IndexError:
##            raise IndexError, 'player start position is off the map'
##
##        player.currentZone = player.currentMapBlock.getZoneAtPoint(*player.pos)
##        player.currentZone.addPlayer(player)

    def getMapBlockIndices(self, xCoord, yCoord):
        '''Returns the index in self.zoneBlocks of the map block which the
        given x and y-coordinates belong to.
        (0, 0) is the top-left corner.

        To find a zone, use MapBlock.getZoneAtPoint()'''
        
        blockY = int(yCoord // self.halfZoneHeight)

        blockX, remainder = divmod(xCoord, self.zoneBodyWidth + \
                                   self.zoneInterfaceWidth)
        if remainder >= self.zoneInterfaceWidth:
            blockX = int(2 * blockX + 1)
        else:
            blockX = int(2 * blockX)

        return blockY, blockX 

    
class MapBlock(object):
    '''Represents a grid square of the map which may contain a single zone,
    or the interface between two zones.'''

    def __init__(self, universe, x, y):
        self.universe = universe
        self.pos = [x, y]       # Pos is the top-left corner of this block.

        self.blocked = False    # There's a barrier somewhere depending on type.

        # We don't yet know which map blocks surround us.
        self.blockLeft = self.blockRight = self.blockAbove = \
                         self.blockBelow = None

        # Layout isn't selected yet.
        self.layout = None

    def __contains__(self, point):
        '''Checks whether a given point is within this zone.'''
        return self.rect.collidepoint(*point)

    def getZoneAtPoint(self, x, y):
        '''getZoneAtPoint(x, y)
        Returns what zone is at the specified point, ASSUMING that the point
        is in fact within this map block.'''
        raise NotImplementedError
                
    def fromEdge(self, player):
        '''Returns the distance from the edge of the zone that a player is'''
        return

    def removeShot(self, shot):
        '''Removes a given shot from this mapBlock'''
        self.shots.remove(shot)

    def addShot(self, shot):
        '''Adds a given shot to this mapBlock'''
        if not self.shots.has(shot):
            self.shots.add(shot)
        
class BodyMapBlock(MapBlock):
    '''Represents a map block which contains only a single zone.'''

    def __init__(self, universe, x, y, zone):
        super(BodyMapBlock, self).__init__(universe, x, y)
        self.zone = zone

    def __repr__(self):
        return '< %s >' % self.zone

    def getZoneAtPoint(self, x, y):
        return self.zone
    
    def Zones(self):
        if self.zone:
            return [self.zone]
        else:
            return []
    


class TopBodyMapBlock(BodyMapBlock):
    '''Represents a map block containing the top half of a zone.'''
    
    def orbPos(self):
        return self.drawRect.midbottom

    def fromEdge(self, player):
        '''Returns the distance from the edge of the zone that a player is'''

        return min(abs(player.pos[1] - self.rect.top), \
                   self.blockLeft.fromEdge(player),\
                   self.blockRight.fromEdge(player))

class BottomBodyMapBlock(BodyMapBlock):
    '''Represents a map block containing the bottom half of a zone.'''
    
    def orbPos(self):
        return self.drawRect.midtop    

    def fromEdge(self, player):
        '''Returns the distance from the edge of the zone that a player is'''
        
        return min(abs(self.rect.bottom - player.pos[1]), \
                   self.blockLeft.fromEdge(player),\
                   self.blockRight.fromEdge(player))

class InterfaceMapBlock(MapBlock):
    '''Base class for map blocks which contain the interface between two
    zones.'''

    def __init__(self, universe, x, y, zone1, zone2):
        super(InterfaceMapBlock, self).__init__(universe, x, y)

        self.zone1 = zone1
        self.zone2 = zone2
        self.blocked = True
        
    def Zones(self):
        tempZones = []
        if self.zone1:
            tempZones.append(self.zone1)
        if self.zone2:
            tempZones.append(self.zone2)
        return tempZones
    
class ForwardInterfaceMapBlock(InterfaceMapBlock):
    '''Represents a map block which contains the interface between two
    zones, split in the direction of a forward slash '/'.
    Note that exactly on the diagonal counts as being in the left-hand zone.
    '''

    def __repr__(self):
        return '< %s / %s >' % (self.zone1, self.zone2)

    def getZoneAtPoint(self, x, y):
        # Equation of interface line:
        #   (y - self.y) = -(halfZoneHeight / interfaceWidth)(x - self.x)
        #                        + halfZoneHeight
        deltaY = y - self.pos[1] - self.universe.halfZoneHeight
        deltaX = x - self.pos[0]

        if deltaY * self.universe.zoneInterfaceWidth > \
               -self.universe.halfZoneHeight * deltaX:
            return self.zone2
        return self.zone1


    def fromEdge(self, player):
        '''Returns the distance from the edge of the zone that a player is.
        Assumes that the player is actually in this map block.'''
        relPos = (self.rect.left - player.pos[0], self.rect.top - player.pos[1])
        # Note: this following formula relies upon the dimensions:
        # self.universe.halfZoneHeight = 384
        # self.universe.zoneInterfaceWidth = 512
        # Should they be changed, should change this to:
        # d = sin(theta) * abs(relPos[1] + relPos[0] * \
        # self.universe.halfZoneHeight / self.universe.zoneInterfaceWidth + 384)
        # (where theta is the angle formed by the diagonal line seperating the
        # zones, and a vertical line).
        d = 0.8 * abs(relPos[1] + relPos[0] * 0.75 + 384)
        return d

class BackwardInterfaceMapBlock(InterfaceMapBlock):
    '''Represents a map block which contains the interface between two
    zones, split in the direction of a backslash '\'.
    Note that a point exactly on the diagonal counts as being in the left-hand
    zone.
    '''

    def __repr__(self):
        return '< %s \ %s >' % (self.zone1, self.zone2)

    def getZoneAtPoint(self, x, y):
        # Equation of interface line:
        #   (y - self.y) = (halfZoneHeight / interfaceWidth)(x - self.x)
        deltaY = y - self.pos[1]
        deltaX = x - self.pos[0]

        if deltaY * self.universe.zoneInterfaceWidth > \
               self.universe.halfZoneHeight * deltaX:
            return self.zone1
        return self.zone2

    def fromEdge(self, player):
        '''Returns the distance from the edge of the zone that a player is.
        Assumes that the player is actually in this map block.'''
        relPos = (self.rect.left - player.pos[0], self.rect.top - player.pos[1])
        
        # Note: this following formula relies upon the dimensions:
        # self.universe.halfZoneHeight = 384
        # self.universe.zoneInterfaceWidth = 512
        # Should they be changed, should change this to:
        # d = sin(theta) * abs(relPos[1] - relPos[0] * \
        # self.universe.halfZoneHeight / self.universe.zoneInterfaceWidth)
        # where theta is the angle formed by the diagonal line seperating the
        # zones, and a vertical line.
        d = 0.8 * abs(relPos[1] - relPos[0] * 3 / 4)
        return d

class Zone(object):
    '''Represents information about a given zone and its state.'''

    def __init__(self, universe, initialOwner = None):
        self.universe = universe
        self.zoneOwner = initialOwner
        self.orbOwner = initialOwner
        self.adjacentZones = set()
        self.players = []
        self.nonPlayers = []

        self.turretedPlayer = None

    def __repr__(self):
        # Debug: uniquely identify this zone within the universe.
        if self.id == None:
            return 'Z---'
        return 'Z%3d' % self.id

    def canBeTaggedBy(self, tagger):
        team = tagger.team
        if self.orbOwner == team:
            return False

        numTaggers = 0
        numDefenders = 0
        # Create a temporary team reference to count
        # members on each team
        if team is not None:
            tempTeam = team
        else:
            tempTeam = self.universe.teams[0]

        # Count the players in this zone        
        for player in self.players:
            if player.turret:
                # Turreted players do not count as a player for the purpose
                # of reckoning whether an enemy can capture the orb
                continue
            if player.team == tempTeam: 
                numTaggers += 1
            else:
                numDefenders += 1
                    
        if team is not None:
            # Zone has been tagged for a team:
            
            # Verify that the player is in this zone.
            if tagger.currentZone != self:
                return False


            if not (numTaggers > numDefenders or numTaggers >= 4):
                return False
        else:
            # Zone to be Rendered neutral
            if not (numTaggers >= 4 and numDefenders >= 4):
                return False

        # If an adjacent zone is also owned, we are able to tag
        for zone in self.adjacentZones:
            if zone.orbOwner == team:
                return True
        # Otherwise, we are unable to tag
        return False     
        
    def tag(self, tagger):
        '''This method should be called by netClient when the orb in this
        zone is tagged. We assume that the tagging player is alive, that it
        is not a Turret, and that the team does not already own the orb.'''
        # Verify that the number of players within is in the team's favour
        assert self.canBeTaggedBy(tagger)
        team = tagger.team
        
        # Kill any turreted Player
        if self.turretedPlayer:
            self.turretedPlayer.killed(tagger)

        # Inform the team objects
        if self.orbOwner:
            self.orbOwner.orbLost()
        if team:
            team.orbGained()

            
        if team is None:
            self.orbOwner = None
            self.zoneOwner = None
            print 'Zone %s neutralised' % (self.id,)
        else:
            print '%s tagged Zone %s' % (tagger.nick, self.id)
            tagger.addStar()
            self.orbOwner = team
            allGood = True
            for zone in self.adjacentZones:
                if zone.orbOwner == team:
                    # Allow the adjacent zone to check if it is entirely
                    # surrounded by non-enemy zones
                    zone.checkAgain()
                elif zone.orbOwner == None:
                    pass
                else:
                    allGood = False
            if allGood:
                self.zoneOwner = team
            else:
                self.zoneOwner = None

        self.universe.checkFinished()
        return True

        
    def checkAgain(self):
        '''This method should be called by an adjacent friendly zone that has
        been tagged and gained. It will check to see if it now has all
        surrounding orbs owned by the same team, in which case it will
        change its zone ownership.'''

        # If the zone is already owned, ignore it
        if self.zoneOwner != self.orbOwner and self.orbOwner != None:
            for zone in self.adjacentZones:
                if zone.orbOwner == self.orbOwner \
                   or zone.orbOwner == None:
                    pass
                else:
                    # Found an enemy orb.
                    break
            else:
                # Change zone ownership to orb ownership.
                self.zoneOwner = self.orbOwner

    def removePlayer(self, player):
        '''Removes a player from this zone'''
        try:
            if player.dead:
                self.nonPlayers.remove(player)
            else:
                self.players.remove(player)
        except:
            print "MASSIVE WEIRD STUPID ERROR!!"
    def addPlayer(self, player):
        '''Adds a player to this zone'''
        if player.dead:
            self.nonPlayers.append(player)
        else:
            self.players.append(player)

    def playerDied(self, player):
        self.players.remove(player)
        self.nonPlayers.append(player)

    def playerRespawned(self, player):
        self.nonPlayers.remove(player)
        self.players.append(player)

class Player(object):
    '''serverUniverse's implementation of the player class'''

    maxStars = 10
    def __init__(self, universe, team, nick, id, zone, dead = True):
        '''Note that all players start off dead.'''

        self.reCall = None
        self.respawnCamp = False
        self.upgrade = None
        self.lastShotId = 41
        self.shots = {}
        self.dead = dead
        self.turret = False
        self.shielded = False
        self.phaseshift = False
        self.hasRicochet = False
        self.team = team
        self.universe = universe
        self.nick = nick
        self.id = id
        self.stars = 0
        universe.newPlayer(self)
        # TODO: Perhaps Implement this
        self.currentZone = zone
        zone.addPlayer(self)

        # In test mode, every player gets 20 stars.
        if universe.netServer.settings['testMode']:
            self.stars = 20
            self.team.teamStars = 100

    def killed(self, killer):
        if self.upgrade:
            self.upgrade.serverDelete()
        self.dead = True
        # In test mode, every player always has 20 stars.
        if not self.universe.netServer.settings['testMode']:
            self.stars = 0
            killer.addStar()
        self.currentZone.playerDied(self)
    
    def killable(self):
        return not (self.turret or self.shielded or self.dead or self.respawnCamp or self.phaseshift)

    def addStar(self):
        if self.universe.netServer.settings['testMode']:
            return
        if self.stars < self.maxStars and not self.dead and not self.turret:
            self.stars += 1
        self.team.addStar()

    def newShotId(self):
        '''Creates a new single-character player id.'''

        sId = struct.pack('B', self.lastShotId)
        self.lastShotId += 1
        self.lastShotId = self.lastShotId % 256
        return sId

    def destroyShot(self, sId):
        try:
            del self.shots[sId]
        except KeyError:
            # Shot must be already destroyed.
#            logging.writeException()
            pass

    def addShot(self, shot):
        self.shots[shot.id] = shot
    
    def respawnCampOff(self):
        self.respawnCamp = False

    def respawn(self):
        if self.dead:
            self.respawnCamp = True
            reactor.callLater(1.5, self.respawnCampOff)
            self.dead = False
            self.currentZone.playerRespawned(self)
        else:
            # Must have just been a validation
            pass

    def subtractStars(self, stars):
        if self.universe.netServer.settings['testMode']:
            return
        self.stars -= stars
        if self.stars < 0:
            print 'OH NOES! Self.stars < 0. %s %s' % (self.stars, stars)
            self.stars = 0
        print '%s now has %s stars' % (self.nick, self.stars)

    def changeZone(self, newZone):
        if newZone != self.currentZone:
            self.currentZone.removePlayer(self)
            newZone.addPlayer(self)
            self.currentZone = newZone
        

class Shot(object):
    # Speed that shots travel at.
    speed = 400       # pix/s
    lifetime = 1.2    # s

    def __init__(self, id, team, pos, angle, player, turret, ricochet):

        self.id = id
        self.team = team
        self.pos = list(pos)
        self.angle = angle
        self.originatingPlayer = player
        self.turretShot = turret
        self.ricochetShot = ricochet
        self.originatingPlayer.addShot(self)
        reactor.callLater(self.lifetime, self.shotDead)

    def shotDead(self):
        self.originatingPlayer.destroyShot(self.id)
