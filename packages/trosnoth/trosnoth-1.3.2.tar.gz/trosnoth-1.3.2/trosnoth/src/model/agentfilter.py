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

from trosnoth.src.utils.components import Component, handler, Plug
from trosnoth.src.messages import (ChatMsg, TaggingZoneMsg, PlayerStarsSpentMsg,
        PlayerHasUpgradeMsg, DeleteUpgradeMsg, CannotBuyUpgradeMsg,
        BuyUpgradeMsg, GameStartMsg, GameOverMsg, StartingSoonMsg,
        SetTeamNameMsg, SetGameModeMsg, ShotFiredMsg, ShootMsg, KillShotMsg,
        RespawnRequestMsg, CannotRespawnMsg, RespawnMsg, PlayerKilledMsg,
        PlayerUpdateMsg, PlayerHitMsg, JoinRequestMsg, AddPlayerMsg,
        CannotJoinMsg, JoinSuccessfulMsg, UpdatePlayerStateMsg, AimPlayerAtMsg,
        RemovePlayerMsg, SetCaptainMsg, TeamIsReadyMsg, QueryWorldParametersMsg,
        SetWorldParametersMsg, RequestMapBlockLayoutMsg, MapBlockLayoutMsg,
        ConnectionLostMsg, NotifyUDPStatusMsg, ZoneStateMsg)
from twisted.internet import reactor

REQUEST_TIMEOUT = 2

def storeTag(tagsAttr):
    '''
    Returns a request message handler function which stores the message tag in
    the given tags attribute.
    '''
    def reqHandler(self, msg):
        tags = getattr(self, tagsAttr)
        tags.add(msg.tag)
        reactor.callLater(REQUEST_TIMEOUT, tags.discard, msg.tag)
        self.gameRequests.send(msg)
    return reqHandler

def checkTag(tagsAttr):
    '''
    Checks that the tag of the given message corresponds to a known tag.
    '''
    def evtHandler(self, msg):
        tags = getattr(self, tagsAttr)
        if msg.tag in tags:
            tags.remove(msg.tag)
            self.agentEvents.send(msg)
    return evtHandler

def checkPlayerId(fn):
    def reqHandler(self, msg):
        if msg.playerId in self.playerIds:
            fn(self, msg)
    return reqHandler

class AgentFilter(Component):
    '''
    This component is designed to sit between an agent (e.g. interface,
    server-side network connection, AI) and a game engine (local or network) and
    filter messages so that only messages relevant to this agent get through to
    it.
    '''

    # agentEvents <- AgentFilter <- gameEvents
    gameEvents = Plug()
    agentEvents = Plug()

    # agentRequests -> AgentFilter -> gameRequests
    agentRequests = Plug()
    gameRequests = Plug()

    def __init__(self):
        Component.__init__(self)
        self.buyUpgradeTags = set()
        self.joinGameTags = set()
        self.respawnTags = set()
        self.worldParamsTags = set()
        self.mapBlockLayoutTags = set()
        self.playerIds = set()

    def disconnect(self):
        '''
        Sends the appropriate messages to indicate that the agent that was
        connected through this AgentFilter is no longer connected.
        '''
        for playerId in list(self.playerIds):
            self.gameRequests.send(RemovePlayerMsg(playerId))

    # Events from game to agent which are always relevant.
    @handler(DeleteUpgradeMsg, gameEvents)
    @handler(GameStartMsg, gameEvents)
    @handler(TaggingZoneMsg, gameEvents)
    @handler(PlayerStarsSpentMsg, gameEvents)
    @handler(PlayerHasUpgradeMsg, gameEvents)
    @handler(KillShotMsg, gameEvents)
    @handler(ShotFiredMsg, gameEvents)
    @handler(AddPlayerMsg, gameEvents)
    @handler(RespawnMsg, gameEvents)
    @handler(UpdatePlayerStateMsg, gameEvents)
    @handler(AimPlayerAtMsg, gameEvents)
    @handler(PlayerKilledMsg, gameEvents)
    @handler(PlayerHitMsg, gameEvents)
    @handler(GameOverMsg, gameEvents)
    @handler(SetCaptainMsg, gameEvents)
    @handler(TeamIsReadyMsg, gameEvents)
    @handler(StartingSoonMsg, gameEvents)
    @handler(SetTeamNameMsg, gameEvents)
    @handler(SetGameModeMsg, gameEvents)
    @handler(PlayerUpdateMsg, gameEvents)
    @handler(ConnectionLostMsg, gameEvents)
    @handler(ChatMsg, gameEvents)
    @handler(NotifyUDPStatusMsg, gameEvents)
    @handler(ZoneStateMsg, gameEvents)
    def passToAgent(self, msg):
        self.agentEvents.send(msg)

    # Requests from agent to game which require no processing
    # except checking for correct player id.
    @handler(ShootMsg, agentRequests)
    @handler(DeleteUpgradeMsg, agentRequests)
    @handler(SetCaptainMsg, agentRequests)
    @handler(TeamIsReadyMsg, agentRequests)
    @handler(UpdatePlayerStateMsg, agentRequests)
    @handler(AimPlayerAtMsg, agentRequests)
    @handler(ChatMsg, agentRequests)
    @checkPlayerId
    def passToGame(self, msg):
        self.gameRequests.send(msg)

    # Buying upgrades may sometimes result in a response.
    reqBuyUpgrade = handler(BuyUpgradeMsg, agentRequests)(
        checkPlayerId(
            storeTag('buyUpgradeTags')))
    evtUpgradeResponse = (
        handler(CannotBuyUpgradeMsg, gameEvents)(
            checkTag('buyUpgradeTags')))

    # Respawn requests.
    reqRespawn = handler(RespawnRequestMsg, agentRequests)(
        checkPlayerId(
            storeTag('respawnTags')))
    evtRespawnResponse = handler(CannotRespawnMsg, gameEvents)(
            checkTag('respawnTags'))

    # World settings requests.
    reqWorldSettings = handler(QueryWorldParametersMsg, agentRequests)(
            storeTag('worldParamsTags'))
    evtWorldSettings = handler(SetWorldParametersMsg, gameEvents)(
            checkTag('worldParamsTags'))

    # Map block layout requests.
    reqMapBlockLayout = handler(RequestMapBlockLayoutMsg, agentRequests)(
            storeTag('mapBlockLayoutTags'))
    evtMapBlockLayout = handler(MapBlockLayoutMsg, gameEvents)(
            checkTag('mapBlockLayoutTags'))


    # Join requests.
    reqJoinGame = handler(JoinRequestMsg, agentRequests)(
            storeTag('joinGameTags'))
    evtJoinFailure = handler(CannotJoinMsg, gameEvents)(
            checkTag('joinGameTags'))

    @handler(JoinSuccessfulMsg, gameEvents)
    def evtJoinSucceeded(self, msg):
        tags = self.joinGameTags
        if msg.tag in tags:
            tags.remove(msg.tag)
            self.playerIds.add(msg.playerId)
            self.agentEvents.send(msg)

    @handler(RemovePlayerMsg, gameEvents)
    def evtRemovePlayer(self, msg):
        self.playerIds.discard(msg.playerId)
        self.agentEvents.send(msg)

