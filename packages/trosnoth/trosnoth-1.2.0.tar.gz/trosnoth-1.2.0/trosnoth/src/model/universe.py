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

'''universe.py - defines anything that has to do with the running of the
universe. This includes players, shots, zones, and the level itself.'''

import pygame

from trosnoth.src.utils.utils import timeNow
import trosnoth.src.utils.logging as logging
from trosnoth.src.utils.checkpoint import checkpoint
import trosnoth.src.model.modes as modes
from trosnoth.src.model.universe_base import GameState
import trosnoth.src.model.transaction as transactionModule
from trosnoth.src.model.upgrades import upgradeOfType

# TODO: remove isinstances so we can remove some of these:
from trosnoth.src.model.map import MapLayout, MapState
from trosnoth.src.model.mapblocks import BodyMapBlock
from trosnoth.src.model.shot import Shot, GrenadeShot
from trosnoth.src.model.player import Player
from trosnoth.src.model.team import Team


# Component message passing
from trosnoth.src.utils.components import Component, handler, Plug
from trosnoth.src.messages.chat import Chat, OwnChat
from trosnoth.src.messages.game import (SetCaptain, StartingSoon, TeamIsReady,
        GameOver, SetGameMode, SetTeamName)
from trosnoth.src.messages.gameplay import (TaggedZone, PlayerKilled, KillShot,
        PlayerRespawn)
from trosnoth.src.messages.players import AddPlayer, RemovePlayer
from trosnoth.src.messages.shot import ShotFired, ShotGone
from trosnoth.src.messages.grenade import GrenadeNowExists, GrenadeGone
from trosnoth.src.messages.transactions import (TransactionChanged,
        StartedTransaction, TransactionComplete, AbandonTransaction,
        AddedStars, UseUpgrade, DeleteUpgrade)
from trosnoth.src.messages.validation import NotifyUDPStatus
from trosnoth.src.network.chat import ChatFromServerMsg
from trosnoth.src.network.shot import ShotFiredMsg
from trosnoth.src.network.gameplay import PlayerUpdateMsg
from trosnoth.src.network.game import GameStartMsg
from trosnoth.src.network.players import AddPlayerMsg
from trosnoth.src.network.transactions import StartedTransactionMsg


# FIXME: there's the potential for some things to require an interface
# before it is created (such as using a transaction)

# TODO: Get this GUI stuff out of model
def init():
    '''Initialises anything that's needed by this module. This function should
    only be called after pygame.init() and after the video mode has been set.'''
    pygame.font.init()
            
class Universe(Component):
    '''Universe(halfMapWidth, mapHeight)
    Keeps track of where everything is in the level, including the locations
    and states of every alien, the terrain positions, and who owns the
    various territories and orbs.'''

    # The size of players and shots.
    halfPlayerSize = (10, 19)
    halfShotSize = (5, 5)

    # actionPlug is a sending plug
    # Things are sent to it after something happens
    # This may in turn be picked up by a network or a GUI
    actionPlug = Plug()

    # requestPlug is a sending plug
    # Things that this universe thinks should happen
    # should be sent to it
    requestPlug = Plug()

    # orderPlug is a receiving plug
    # When an object wants to order the universe to do something,
    # they should send a message to this plug
    orderPlug = Plug()

    def __init__(self, app, halfMapWidth, mapHeight):
        '''
        halfMapWidth:   is the number of columns of zones in each team's
                        territory at the start of the game. There will always
                        be a single column of neutral zones between the two
                        territories at the start of the game.
        mapHeight:      is the number of zones in every second column of
                        zones. Every other column will have mapHeight + 1
                        zones in it. This is subject to the constraints that
                        (a) the columns at the extreme ends of the map will
                        have mapHeight zones; (b) the central (initially
                        neutral) column of zones will never have fewer zones
                        in it than the two bordering it - this will sometimes
                        mean that the column has mapHeight + 2 zones in it.'''

        super(Universe, self).__init__()
        self.app = app

        # Initialise
        self.gameState = GameState.PreGame
        self.startTime = 0
        self.zonesToReset = []
        self.playerWithId = {}
        self.teamWithId = {'\x00' : None}

        # Create Teams:
        self.teams = (
            Team(self, 'A'),
            Team(self, 'B'),
        )
        Team.setOpposition(self.teams[0], self.teams[1])
        
        for t in self.teams:
            self.teamWithId[t.id] = t        
                
        # Set up zones
        self.zoneWithDef = {}
        self.map = MapState(self, halfMapWidth, mapHeight)
        self.zoneWithId = self.map.zoneWithId
        self.zones = self.map.zones
        self.zoneBlocks = self.map.zoneBlocks

        self.players = set()
        self.grenades = set()
        # TODO: could make shots iterate directly over the player objects rather than storing twice
        # (redundancy - potential inconsistencies)
        self.shots = set()
        self.gameOverTime = None
        self.gameModeController = modes.GameMode(Shot, Player, GrenadeShot)

    @handler(SetGameMode, orderPlug)
    def setGameMode(self, msg):
        mode = msg.gameMode
        try:
            getattr(self.gameModeController, mode)()
            print 'Client: GameMode is set to ' + mode
        except AttributeError:
            print 'No such gameMode'
        except TypeError:
            print 'No such gameMode'

    @handler(SetTeamName, orderPlug)
    def setTeamName(self, msg):
        msg.team.teamName = msg.name

    def setTimeLeft(self, time):
        # TODO: could do some validation here.
        pass

    def getTimeLeft(self):
        if self.gameState == GameState.PreGame:
            return None
        elif self.gameState == GameState.InProgress:
            return self.startTime + self.gameDuration - timeNow()
        elif self.gameState == GameState.Ended:
            return self.startTime + self.gameDuration - self.gameOverTime

    @handler(GameOver, orderPlug)
    def gameOver(self, msg):
        winningTeam, timeOver = msg.winningTeam, msg.timeOver
        self.gameOverTime = timeNow()
        self.gameState = GameState.Ended
        self.actionPlug.send(msg)

    @handler(GameStartMsg, orderPlug)
    def gameStart(self, msg):
        time = msg.timeLimit
        if self.gameState == GameState.PreGame:
            self.gameDuration = time
            self.startTime = timeNow()
            self.gameState = GameState.InProgress
            self.actionPlug.send(msg)

    @handler(AddPlayerMsg, orderPlug)
    def addPlayer(self, msg):
        team = self.teamWithId[msg.teamId]
        zone = self.zoneWithId[msg.zoneId]

        # Create the player.
        nick = msg.nick.decode()
        
        player = Player(self.app, self, nick, team, msg.playerId, zone,
                        msg.dead)

        #Add this player to this universe.
        self.players.add(player)
        self.playerWithId[msg.playerId] = player

        # Make sure player knows its zone
        i, j = MapLayout.getMapBlockIndices(*player.pos)
        try:
            player.currentMapBlock = self.zoneBlocks[i][j]
        except IndexError:
            logging.writeException()
            raise IndexError, 'player start position is off the map'
        
        self.actionPlug.send(AddPlayer(player))

    @handler(RemovePlayer, orderPlug)
    def delPlayer(self, msg):
        '''Removes the specified player from this universe.'''
        player = msg.player
        player.removeFromGame()
        self.players.remove(player)
        try:
            del self.playerWithId[player.id]
        except KeyError:
            logging.writeException()
            pass
        
        self.actionPlug.send(msg)
        
    def tick(self, deltaT):
        '''Advances all players and shots to their new positions.'''
        # Update the player and shot positions.
        update = lambda item: item.update(deltaT)
        map(update, list(self.shots))
        map(update, list(self.players))
        map(update, list(self.grenades))

        for zone in self.zonesToReset:
            zone.taggedThisTime = False
        self.zonesToReset = []
        
        self.checkForResult()
        
    def checkForResult(self):
        if self.gameState == GameState.InProgress and self.gameDuration > 0:
            # Check first for timeout
            if self.getTimeLeft() <= 0:
                if self.teams[0].numOrbsOwned > self.teams[1].numOrbsOwned:
                    self.requestPlug.send(GameOver(self.teams[0], True))
                    checkpoint('Universe: Out of time, blue wins')
                elif self.teams[1].numOrbsOwned > self.teams[0].numOrbsOwned:
                    self.requestPlug.send(GameOver(self.teams[1], True))
                    checkpoint('Universe: Out of time, red wins')
                else:
                    self.requestPlug.send(GameOver(None, False))
                    checkpoint('Universe: Out of time, game drawn')
                return
                    
            # Now check for an all zones win.
            team2Wins = self.teams[0].isLoser()
            team1Wins = self.teams[1].isLoser()
            if team1Wins and team2Wins:
                # The extraordinarily unlikely situation that all
                # zones have been neutralised in the same tick
                self.requestPlug.send(GameOver(None, False))
                checkpoint('Universe: Draw due to all zones neutralised')
            elif team1Wins:
                self.requestPlug.send(GameOver(self.teams[0], False))
                checkpoint('Universe: Zones captured, blue wins')
            elif team2Wins:
                self.requestPlug.send(GameOver(self.teams[1], False))
                checkpoint('Universe: Zones captured, red wins')

    def validateTurretVal(self, player, turretVal):
        return player.turret == turretVal

    @handler(ShotFiredMsg, orderPlug)
    def shotFired(self, msg):
        '''A player has fired a shot.'''
        player = self.playerWithId[msg.playerId]
        team = player.team
        pos = (msg.xpos, msg.ypos)
        turret = msg.type in ('T', 'G')
        ricochet = msg.type == 'R'
        #assert self.validateTurretVal(player, turret)
        shot = Shot(msg.shotId, team, pos, msg.angle, player, turret, ricochet)
        self.shots.add(shot)
        self.actionPlug.send(ShotFired(player, shot))

    def removeShot(self, shot):
        self.actionPlug.send(ShotGone(shot))
        try:
            self.shots.remove(shot)
        except KeyError:
            logging.writeException()

    def shotWithId(self, pId, sId):
        try:
            return self.playerWithId[pId].shots[sId]
        except:
            logging.writeException()
            return None


        
    def checkTag(self, tagger):
        '''Checks to see if the player has touched the orb of its currentZone
        If so, it fires the onTagged event'''

        # How zone tagging works (more or less)
        # 1. In its _move procedure, if a player is local, it will call checkTag
        # 2. If it is close enough to the orb, and it has the numeric
        #    advantage, and it onws at least one adjacent zone, it has tagged
        #    the zone
        # 3. The zone is checked again to see if the opposing team has also
        #    tagged it
        #    - If so, the zone is rendered neutral (if it's already neutral,
        #    nothing happens).
        #    - If not, the zone is considered to be tagged by the team.
        # 4. If any zone ownership change has been made, the server is informed
        #    however, no zone allocation is performed yet.
        # 5. The server should ensure that the zone hasn't already been tagged
        #    (such as in the situation of two players form the one team tag
        #    a zone simultaneously), as well as checking zone numbers,
        #    before telling all clients of the zone change.
        # 6. The individual clients recalculate zone ownership based on the
        #    zone change

        zone = tagger.currentZone
        if tagger.team == zone.orbOwner:
            return
        
        # If the tagging player has a phase shift, the zone will not be tagged.
        if tagger.phaseshift:
            return

        # Ensure that the zone has not already been checked in this tick:
        if zone is None or zone.taggedThisTime:
            return


        # Radius from orb (in pixels) that counts as a tag.
        tagDistance = 35
        xCoord1, yCoord1 = tagger.pos
        xCoord2, yCoord2 = zone.defn.pos

        distance = ((xCoord1 - xCoord2) ** 2 + (yCoord1 - yCoord2) ** 2) ** 0.5
        if distance < tagDistance:
            # Check to ensure the team owns an adjacent orb
            found = False
            for adjZoneDef in zone.defn.adjacentZones:
                adjZone = self.zoneWithDef[adjZoneDef]
                if adjZone.orbOwner == tagger.team:
                    found = True
                    break
            if not found:
                return

            # Check to see if the team has sufficient numbers to take the zone.
            numTaggers = 0
            numDefenders = 0
            for player in zone.players:
                if player.turret:
                    # Turreted players do not count as a player for the purpose
                    # of reckoning whether an enemy can capture the orb
                    continue
                if player.team == tagger.team:
                    numTaggers += 1
                else:
                    numDefenders += 1

            if numTaggers > numDefenders or numTaggers > 3:
                   
                if (numDefenders > 3 and 
                        zone.checkForOpposingTag(tagger.team)):
                    # The other team has also tagged it
                    if zone.orbOwner != None:
                        self.requestPlug.send(TaggedZone(zone, None))
                        checkpoint('Universe: two teams tag same zone')
                else:
                    # This team is the only to have tagged it
                    self.requestPlug.send(TaggedZone(zone, tagger))
                    checkpoint('Universe: zone tagged')

                zone.taggedThisTime = True
                self.zonesToReset.append(zone)
            else:
                checkpoint('Universe: failed attempt to tag zone')

    @handler(PlayerKilled, orderPlug)
    def killPlayer(self, msg):
        '''Turns a player into a ghost at the given location, crediting the
        killer with a star'''
        player, killer, shot = msg.target, msg.killer, msg.shot
        if shot:
            print killer.nick + ' killed ' + player.nick
        else:
            print killer.nick + ' killed turreted player ' + player.nick + \
                  ' by tagging the zone'

        # Credit the killer
        killer.incrementStars()

        # Remove player from its zone as a living player
        player.currentZone.removePlayer(player)
        # Turn them into a ghost
        player.die()
        # Add player back to the zone as a ghost
        player.currentZone.addPlayer(player)
        if shot:
            shot.kill()
            
        self.actionPlug.send(msg)

    @handler(TaggedZone, orderPlug)
    def tagged(self, msg):
        msg.zone.tag(msg.player)
        self.actionPlug.send(msg) 

    @handler(PlayerRespawn, orderPlug)
    def respawn(self, msg):
        '''Brings a player back into the land of the living'''
        # Remove player from its zone as a ghost
        ghost, zone = msg.player, msg.zone
        ghost.currentZone.removePlayer(ghost)
        ghost.currentZone = zone
        ghost.respawn()
        print ghost.nick + ' is back in the game'
        # Add player back to the zone as a living player
        ghost.currentZone.addPlayer(ghost)

        self.actionPlug.send(PlayerRespawn(ghost, zone))        

    # A hacky way of updating contributions if we lost information somewhere.
    def updateContributions(self, transaction, contributions):
        transaction.contributions = contributions
        self.actionPlug.send(TransactionChanged(transaction))


    @handler(StartedTransactionMsg, orderPlug)
    def startTransaction(self, msg):
        team = self.teamWithId[msg.teamId]
        player = self.playerWithId[msg.playerId]
        upgrade = upgradeOfType[msg.upgradeType]
        transaction = transactionModule.Transaction(team, player,
                                                       upgrade, msg.timeLeft)
        self.actionPlug.send(StartedTransaction(transaction))
        transaction.addStars(player, msg.numStars)

    def validateTransaction(self, team, update, numStars):
        if (not team.currentTransaction and update != 'a') or \
           (update == 's' and not team.currentTransaction.totalStars == numStars):
            print 'DEBUG: Invalid Transaction'
            print team.currentTransaction
            print update
            if team.currentTransaction:
                print team.currentTransaction.totalStars, numStars
            return False
        return True

    @handler(AddedStars, orderPlug)
    def addStarsToTransaction(self, msg):
        team = msg.team
        player = msg.player
        stars = msg.numStars
        team.currentTransaction.addStars(player, stars)
        self.actionPlug.send(msg)

    @handler(AbandonTransaction, orderPlug)
    def abandonTransaction(self, msg):
        # TODO: shouldn't need this check:
        
        # If the transaction doesn't exist, don't try and
        # abandon it (it was likely already abandoned)
        if msg.transaction is None:
            return
        msg.transaction.abandon(msg.reason)
        self.actionPlug.send(msg)

    
    def mapBlockWidth(self, blockClass):
        '''Returns the width in pixels of a map block of the given class.'''
        if issubclass(blockClass, BodyMapBlock):
            return MapLayout.zoneBodyWidth
        else:
            return MapLayout.zoneInterfaceWidth

    @handler(TransactionComplete, orderPlug)
    def completeTransaction(self, msg):
        '''Completes the team's transaction, allocating the player who purchased
        it the relevant upgrade'''
        if msg.team.currentTransaction == None:
            transaction = transactionModule.Transaction(msg.team, msg.player,
                                                       msg.upgradeType, 30)
            msg.team.currentTransaction = transaction
            transaction.addStars(msg.player, msg.upgradeType.requiredStars)
            msg.transaction = transaction
        
        msg.team.currentTransaction.complete()
        self.actionPlug.send(msg)
        print 'Transaction Completed'

    def addGrenade(self, grenade):
        self.grenades.add(grenade)
        self.actionPlug.send(GrenadeNowExists(grenade))

    def removeGrenade(self, grenade):
        self.grenades.remove(grenade)
        self.actionPlug.send(GrenadeGone(grenade))

    @handler(SetCaptain, orderPlug)
    def setCaptain(self, msg):
        captain = msg.captain
        captain.team.captain = captain
        self.actionPlug.send(msg)

    @handler(TeamIsReady, orderPlug)
    def teamReady(self, msg):
        player = msg.player
        player.team.ready = True
        self.actionPlug.send(TeamIsReady(player))

    @handler(KillShot, orderPlug)
    def shotDestroyed(self, msg):
        if msg.shot is not None:
            msg.shot.kill()

    @handler(UseUpgrade, orderPlug)
    def useUpgrade(self, msg):
        msg.player.upgrade.clientUse()
        self.actionPlug.send(msg)

    @handler(DeleteUpgrade, orderPlug)
    def destroyUpgrade(self, msg):
        msg.player.deleteUpgrade()
        self.actionPlug.send(msg)

    @handler(PlayerUpdateMsg, orderPlug)
    def gotPlayerUpdate(self, msg):
        # Receive a player update
        try:
            player = self.playerWithId[msg.playerId]
        except:
            # Mustn't have that info yet
            return
        player.gotPlayerUpdate(msg)

    # Passing some chat messages on to the UI
    @handler(OwnChat, orderPlug)
    def gotOwnChat(self, msg):
        self.actionPlug.send(msg)

    @handler(Chat, orderPlug)
    def gotChat(self, msg):
        self.actionPlug.send(msg)

    @handler(NotifyUDPStatus, orderPlug)
    def gotUDPNotification(self, msg):
        self.actionPlug.send(msg)

    @handler(ChatFromServerMsg, orderPlug)
    def gotServerChat(self, msg):
        self.actionPlug.send(msg)

    @handler(StartingSoon, orderPlug)
    def gotStartingSoon(self, msg):
        self.actionPlug.send(msg)
        
    def getTeamStars(self, team):
        total = 0
        for p in self.players:
            if p.team == team:
                total += p.stars
        return total
