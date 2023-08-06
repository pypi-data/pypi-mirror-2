# Trosnoth (UberTweak Platform Game)
# Copyright (C) 2006-2010 Joshua D Bartlett
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

from trosnoth.game import makeLocalGame
from trosnoth.network.networkDefines import serverVersion
from trosnoth.network import netmsg
from trosnoth.model.universe_base import GameState
from trosnoth.utils.components import DynamicPlug, UnhandledMessage

from trosnoth.messages import (ChatMsg, InitClientMsg,
        QueryWorldParametersMsg, RequestMapBlockLayoutMsg, RequestPlayersMsg,
        RequestUDPStatusMsg, NotifyUDPStatusMsg, DeleteUpgradeMsg,
        BuyUpgradeMsg, ShootMsg, RespawnRequestMsg, JoinRequestMsg,
        UpdatePlayerStateMsg, AimPlayerAtMsg, SetCaptainMsg, TeamIsReadyMsg,
        RequestZonesMsg, tcpMessages, PlayerIsReadyMsg, SetPreferredDurationMsg,
        SetPreferredTeamMsg, SetPreferredSizeMsg, RemovePlayerMsg,
        ChangeNicknameMsg)
from trosnoth.utils.event import Event

# The set of messages that the server expects to receive.
serverMsgs = netmsg.MessageCollection(
    RequestUDPStatusMsg,
    QueryWorldParametersMsg,
    RequestMapBlockLayoutMsg,
    ShootMsg,
    DeleteUpgradeMsg,
    SetCaptainMsg,
    TeamIsReadyMsg,
    UpdatePlayerStateMsg,
    AimPlayerAtMsg,
    BuyUpgradeMsg,
    RespawnRequestMsg,
    JoinRequestMsg,
    RequestPlayersMsg,
    RequestZonesMsg,
    ChatMsg,
    PlayerIsReadyMsg,
    SetPreferredDurationMsg,
    SetPreferredTeamMsg,
    SetPreferredSizeMsg,
    RemovePlayerMsg,
    ChangeNicknameMsg,
)
class ServerNetHandler(object):
    '''
    A network message handler designed for use with trosnoth.network.netman.
    '''
    greeting = 'Trosnoth1'
    messages = serverMsgs

    def __init__(self, layoutDatabase, netman, halfMapWidth, mapHeight,
            duration=0, maxPlayers=8, authTagManager=None,
            voting=False, gameName=None, alertSettings=None):
        self.netman = netman
        self.authTagManager = authTagManager
        self.connectedClients = {}      # connId -> IP addr
        self.agents = {}                # connId -> agent
        self.agentPlugs = {}            # connId -> plug

        self.onShutdown = Event()       # ()

        self.game = makeLocalGame(gameName, layoutDatabase, halfMapWidth,
                mapHeight, duration, maxPlayers, authTagManager, voting=voting,
                alertSettings=alertSettings)

        self.running = True
        self._alreadyShutdown = False

    def connectionComplete(self, connId):
        'Should never be called'
    def connectionFailed(self, connId):
        'Should never be called'

    def receiveBadString(self, connId, line):
        print 'Server: Unrecognised network data: %r' % (line,)
        print '      : Did you invent a new network message and forget to'
        print '      : add it to trosnoth.network.server.serverMsgs?'

    def newConnection(self, connId, ipAddr, port):
        '''
        Called by the network manager when a new incoming connection is
        completed.
        '''
        # Remember that this connection's ready for transmission.
        self.connectedClients[connId] = ipAddr
        agent = self.game.addAgent(*self._makeRemoteAgent(connId))
        self.agents[connId] = agent

        # Send the setting information.
        self.netman.sendTCP(connId,
                InitClientMsg(self._getClientSettings()))

    def _makeRemoteAgent(self, connId):
        '''
        Returns (eventPlug, controller) for the remote agent.
        '''
        def sendMessage(msg):
            try:
                if msg.__class__ in tcpMessages:
                    self.netman.sendTCP(connId, msg)
                else:
                    self.netman.send(connId, msg)
            except ValueError:
                pass
        eventPlug = DynamicPlug(sendMessage)
        requestPlug = DynamicPlug(self._sendBackToRequestPlug)
        
        self.agentPlugs[connId] = requestPlug
        return eventPlug, requestPlug

    def _sendBackToRequestPlug(self, msg):
        raise UnhandledMessage('Server will not send %r backwards over '
                'request plug' % (msg,))

    def receiveMessage(self, connId, msg):
        if isinstance(msg, RequestUDPStatusMsg):
            # Client has requested info as to whether server is sending UDP.
            self.netman.sendTCP(connId, NotifyUDPStatusMsg(
                    self.netman.getUDPStatus(connId)))
            return

        try:
            plug = self.agentPlugs[connId]
        except KeyError:
            return
        plug.send(msg)

    def _getClientSettings(self):
        '''Returns a string representing the settings which must be sent to
        clients that connect to this server.'''

        result = {
            'serverVersion': serverVersion,
        }

        return repr(result)
            
    def connectionLost(self, connId):
        if connId in self.connectedClients:
            self.game.detachAgent(self.agents[connId])

        del self.connectedClients[connId]

        # Check for game over and no connections left.
        if (len(self.connectedClients) == 0 and self.game.world.gameState
                == GameState.Ended):
            # Don't shut down if local player is connected.
            if len(self.game.world.players) == 0:
                # Shut down the server.
                self.shutdown()

    def shutdown(self):
        if self._alreadyShutdown:
            return
        self._alreadyShutdown = True

        # Kill server
        self.running = False
        self.game.stop()
        self.game.world.stopClock()
        self.onShutdown.execute()
