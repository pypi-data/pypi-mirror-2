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

# Component message passing
from trosnoth.src.utils.components import Component, handler, Plug
from trosnoth.src.messages.chat import *
from trosnoth.src.messages.connection import *
from trosnoth.src.messages.game import *
from trosnoth.src.messages.gameplay import *
from trosnoth.src.messages.players import *
from trosnoth.src.messages.shot import *
from trosnoth.src.messages.transactions import *
from trosnoth.src.messages.validation import NotifyUDPStatus

from trosnoth.src.network.setup import *
from trosnoth.src.network.players import *
from trosnoth.src.network.game import *
from trosnoth.src.network.shot import *
from trosnoth.src.network.chat import *
from trosnoth.src.network.validation import *
from trosnoth.src.network.gameplay import *
from trosnoth.src.network.map import *
from trosnoth.src.network.transactions import *

from trosnoth.src.model.upgrades import upgradeOfType

from trosnoth.src.utils import logging

# Network to Universe message Translator
class MessageTranslator_N2U(Component):

    receiverPlug = Plug()
    worldPlug = Plug()

    # TODO: This is similar to a function in networkClient.py - could generalise.
    def __createMessagePassOn(self):
        messagesToPassOn = (Chat, OwnChat, NotifyUDPStatus, AddPlayerMsg, GameStartMsg, ShotFiredMsg,
                            PlayerUpdateMsg, StartedTransactionMsg)
        
        for messageType in messagesToPassOn:
            string = 'handle_%s' % (messageType.__name__,)
            @handler(messageType, self.receiverPlug)
            def fn(self, msg):
                self.worldPlug.send(msg)
            setattr(self, string, fn)    
    
    # Need a reference to the world to
    # translate from ID to object
    def __init__(self, world):
        self.__createMessagePassOn()
        super(MessageTranslator_N2U, self).__init__()
        self.world = world
        self.worldPlug.connectPlug(world.orderPlug)

    # This is sort of like C++ overloading, but less safety.
    # With the convention that players are in there under
    # msg.playerId, zones as msg.zoneId and teams as msg.teamId
    def getPlayer(self, msg = None, id = -1):
        assert(msg != None or id != -1)
        if id == -1:
            return self.world.playerWithId[msg.playerId]
        return self.world.playerWithId[id]

    def getZone(self, msg = None, id = -1):
        assert(msg != None or id != -1)
        if id == -1:
            return self.world.zoneWithId[msg.zoneId]
        return self.world.zoneWithId[id]

    def getTeam(self, msg = None, id = -1):
        assert(msg != None or id != -1)
        if id == -1:
            return self.world.teamWithId[msg.teamId]
        return self.world.teamWithId[id]

    def getShot(self, player, msg):
        try:
            shot = player.shots[msg.shotId]
        except KeyError:
            logging.writeException()
            shot = None
        return shot

    # TODO: This is here temporarily, but should be deleted
    def positionUpdate(self, player, pos, yVel=None,
            angle=None, thrust=None):
        player._positionUpdate(pos, yVel, angle, thrust)

    @handler(KilledMsg, receiverPlug)
    def receiveKilledMsg(self, msg):
        player = self.getPlayer(id=msg.targetId)
        killer = self.getPlayer(id=msg.killerId)
        shot = self.getShot(player, msg)
        self.worldPlug.send(PlayerKilled(player, killer, shot))
        self.positionUpdate(player, (msg.xPos, msg.yPos))

    @handler(TaggedZoneMsg, receiverPlug)
    def receiveTaggedZoneMsg(self, msg):
        # Zone has been tagged.
        zone = self.getZone(msg)
        team = self.getTeam(msg)
        if team is None:
            self.worldPlug.send(TaggedZone(zone, None))
        else:
            player = self.getPlayer(msg)
            self.worldPlug.send(TaggedZone(zone, player))
            if msg.killedTurret:
                turret = self.getPlayer(msg.turretId)
                self.worldPlug.send(PlayerKilled(turret, player, None))

    @handler(RespawnMsg, receiverPlug)
    def receiveRespawnMsg(self, msg):
        player = self.getPlayer(msg)
        zone = self.getZone(msg)
        self.worldPlug.send(PlayerRespawn(player, zone))

    @handler(RemovePlayerMsg, receiverPlug)
    def receiveRemovePlayerMsg(self, msg):
        # Server says this player has left the game.
        try:
            player = self.getPlayer(msg)
        except KeyError:
            # TODO: Handle this sensibly.
            logging.writeException()
            return
        self.worldPlug.send(RemovePlayer(player))

    @handler(KillShotMsg, receiverPlug)
    def receiveKillShotMsg(self, msg):
        player = self.getPlayer(msg)
        shot = self.getShot(player, msg)
        self.worldPlug.send(KillShot(player, shot))

    @handler(SetCaptainMsg, receiverPlug)
    def receiveSetCaptainMsg(self, msg):
        player = self.getPlayer(msg)
        self.worldPlug.send(SetCaptain(player))

    @handler(TeamIsReadyMsg, receiverPlug)
    def receiveTeamIsReadyMsg(self, msg):
        player = self.getPlayer(msg)
        self.worldPlug.send(TeamIsReady(player))

    @handler(DeleteUpgradeMsg, receiverPlug)
    def receiveDeleteUpgradeMsg(self, msg):
        # A player's upgrade is deleted
        player = self.getPlayer(msg)
        self.worldPlug.send(DeleteUpgrade(player, player.upgrade))

    @handler(AddedStarsMsg, receiverPlug)
    def receiveAddedStarsMsg(self, msg):
        # A player has added star(s) to a transaction
        team = self.getTeam(msg)
        player = self.getPlayer(msg)
        self.worldPlug.send(AddedStars(team, player, msg.numStars))


    @handler(AbandonTransactionMsg, receiverPlug)
    def receiveAbandonTransactionMsg(self, msg):
        # A transaction has been abandoned
        team = self.getTeam(msg)
        transaction = team.currentTransaction
        reason = msg.reason.decode()
        self.worldPlug.send(AbandonTransaction(transaction, reason))


    @handler(UseUpgradeMsg, receiverPlug)
    def receiveUseUpgradeMsg(self, msg):
        # A player is using an upgrade
        player = self.getPlayer(msg)
        self.positionUpdate(player, (msg.xPos, msg.yPos))
        self.worldPlug.send(UseUpgrade(player))


    @handler(TransactionCompleteMsg, receiverPlug)
    def receiveTransactionCompleteMsg(self, msg):
        # A transaction has been completed
        team = self.getTeam(msg)
        player = self.getPlayer(msg)
        upgradeType = upgradeOfType[msg.upgradeType]
        self.worldPlug.send(TransactionComplete(team, player, upgradeType, team.currentTransaction))

    def receiveChat(self, text, sender, private):
        '''We have received a chat from someone in the game.'''
        self.worldPlug.send(Chat(sender, private, text))

    @handler(ChatMsg, receiverPlug)
    def receiveChatMsg(self, msg):
        # A chat is received
        sender = self.getPlayer(id=msg.senderId)
        if msg.kind == 't':     # Team
            team = self.getTeam(id=msg.targetId)
            self.receiveChat(msg.text.decode(), sender, team)
        elif msg.kind == 'p':   # Private
            print 'Received private chat for player %d' % (ord(msg.targetId))
            receiver = self.getPlayer(id=msg.targetId)
            # Find the address to send it to:
            self.receiveChat(msg.text.decode(), sender, receiver)
        elif msg.kind == 'o':   # Open
            self.receiveChat(msg.text.decode(), sender, None)
        else:
            print 'Client: received unknown chat kind: %r' % (msg.kind,)

    @handler(ChatFromServerMsg, receiverPlug)
    def receiveChatFromServerMsg(self, msg):
        self.worldPlug.send(ChatFromServer(msg.text.decode()))

    @handler(StartingSoonMsg, receiverPlug)
    def receiveStartingSoonMsg(self, msg):
        self.worldPlug.send(StartingSoon(msg.delay))

    @handler(GameOverMsg, receiverPlug)
    def receiveGameOverMsg(self, msg):
        winningTeam = self.getTeam(msg)
        self.worldPlug.send(GameOver(winningTeam, msg.timeOver))
        
    @handler(SetGameModeMsg, receiverPlug)
    def receiveSetGameModeMsg(self, msg):
        self.worldPlug.send(SetGameMode(msg.gameMode.decode()))

    @handler(SetTeamNameMsg, receiverPlug)
    def receiveSetTeamNameMsg(self, msg):
        team = self.getTeam(msg)
        self.worldPlug.send(SetTeamName(team, msg.name.decode()))