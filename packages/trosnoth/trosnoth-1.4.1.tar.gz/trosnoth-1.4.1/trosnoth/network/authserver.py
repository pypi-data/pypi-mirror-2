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

import os
import pickle
import random

from trosnoth import data
from trosnoth.data import getPath, makeDirs
from trosnoth import rsa
from trosnoth.model.mapLayout import LayoutDatabase
from trosnoth.network import authcommands
from trosnoth.network.netman import NetworkManager
from trosnoth.network.server import ServerNetHandler
from trosnoth.network.networkDefines import serverVersion
from trosnoth.settings import AlertSettings, AuthServerSettings
from trosnoth.utils.utils import hasher, timeNow

from trosnoth.gamerecording.achievementlist import achievementDict, OnceEverPerPlayer
from trosnoth.utils.jsonImport import json

from twisted.protocols import amp
from twisted.internet import reactor, defer
from twisted.internet.protocol import Factory, ClientCreator, Protocol
from twisted.internet.error import CannotListenError, ConnectError
from twisted.manhole import telnet

MAX_GAMES = 1
GAME_NAME = 'Auth Server Game'
GAME_KIND = 'Trosnoth1'

NEW_USERS_ALLOWED = True
GAME_VERIFY_TIME = 60

class AuthenticationProtocol(amp.AMP):
    '''
    Trosnoth authentication server which is used when running a game server
    which keeps track of users.
    @param dataPath: path to the location for this authentication server to
        store its data. If not specified, $HOME/.trosnoth/authserver will be
        used. If the path does not exist, it will be created.
    '''

    def connectionMade(self):
        super(AuthenticationProtocol, self).connectionMade()
        self.user = None
        self.token = None
        print 'New connection.'

    def connectionLost(self, reason):
        print 'Connection lost.'

    @authcommands.GetPublicKey.responder
    def getPublicKey(self):
        return {
            'e': self.factory.pubKey['e'],
            'n': self.factory.pubKey['n'],
        }

    @authcommands.ListGames.responder
    def listGames(self):
        games = []
        for gameId in self.factory.servers.iterkeys():
            games.append({
                'id': gameId,
                'game': GAME_KIND,
                'version': serverVersion,
            })

        return {'games': games}

    @authcommands.ListOtherGames.responder
    def listOtherGames(self):
        d = self.factory.getRegisteredGames()
        @d.addCallback
        def gotGames(rGames):
            result = []
            for rGame in rGames:
                result.append({
                    'game': rGame.game,
                    'version': rGame.version,
                    'ip': rGame.host,
                    'port': rGame.port,
                })
            return {
                'games': result,
            }
        return d

    @authcommands.RegisterGame.responder
    def registerGame(self, game, version, port):
        host = self.transport.getPeer().host
        self.factory.registerGame(game, version, host, port)
        return {}

    @authcommands.CreateGame.responder
    def createGame(self, game):
        if game != GAME_KIND:
            raise authcommands.CannotCreateGame()
        if len(self.factory.servers) >= MAX_GAMES:
            raise authcommands.CannotCreateGame()
        return {
            'id': self.factory.createGame(),
            'version': serverVersion,
        }

    @authcommands.ConnectToGame.responder
    def connectToGame(self, id):
        if self.user is None:
            raise authcommands.NotAuthenticated()
        try:
            server = self.factory.servers[id]
        except KeyError:
            raise authcommands.GameDoesNotExist()

        tag = server.authTagManager.newTag(self.user)
        nick = self.user.getNick()

        return {
            'port': server.netman.getTCPPort(),
            'authTag': tag,
            'nick': nick,
        }

    @authcommands.GetAuthToken.responder
    def getAuthToken(self):
        self.token = ''.join(str(random.randrange(256)) for i in xrange(16))
        return {
            'token': self.token
        }

    @authcommands.PasswordAuthenticate.responder
    def passwordAuthenticate(self, username, password):
        username = username.lower()
        password = self._decodePassword(password)
        if password is None:
            return {'result': False}    # Bad auth token used.

        d = self.factory.authManager.authenticateUser(username, password)
        @d.addCallback
        def authSucceeded(user):
            self.user = user
            return {'result': True}
        @d.addErrback
        def authFailed(failure):
            return {'result': False}
        return d

    @authcommands.CreateUserWithPassword.responder
    def createUserWithPassword(self, username, password):
        if self.factory.settings.allowNewUsers:
            nick = username
            username = username.lower()
            password = self._decodePassword(password)
            if password is None:
                return {'result': 'Authentication token failure.'}

            authMan = self.factory.authManager
            if authMan.checkUsername(username):
                return {'result': 'That username is taken.'}
            self.user = authMan.createUser(username, password, nick)
        else:
            return {'result': self.factory.settings.privateMsg}
        return {'result': ''}

    def _decodePassword(self, password):
        if self.token is None:
            return None
        token, self.token = self.token, None
        passwordData = rsa.decrypt(password, self.factory.privKey)
        if passwordData[:len(token)] != token:
            return None
        return passwordData[len(token):]

class AuthenticationFactory(Factory):
    protocol = AuthenticationProtocol

    def __init__(self, dataPath=None):
        if dataPath is None:
            dataPath = getPath(data.user, 'authserver')
        makeDirs(dataPath)
        self.dataPath = dataPath
        self.alertSettings = AlertSettings(dataPath)

        self.pubKey, self.privKey = self.loadKeys()
        self.servers = {}     # Game id -> game.
        self.nextId = 0
        self.theme = Theme()
        self.authManager = AuthManager(dataPath)
        self.registeredGames = []

        try:
            self.netman = NetworkManager(6789, 6789)
        except CannotListenError:
            self.netman = NetworkManager(0, None)
            print 'WARNING: Could not server on port 6789.'
        self.layoutDatabase = LayoutDatabase(self)

    @property
    def settings(self):
        return self.authManager.settings

    def loadKeys(self):
        '''
        Loads public and private keys from disk or creates them and saves them.
        '''
        keyPath = os.path.join(self.dataPath, 'keys')
        try:
            pub, priv = pickle.load(open(keyPath, 'rb'))
        except IOError:
            pub, priv = rsa.newkeys(self.settings.keyLength)
            pickle.dump((pub, priv), open(keyPath, 'wb'), 2)

        return pub, priv

    def createGame(self):
        '''
        Creates a new game and returns the game id.
        '''
        gameId = self.nextId
        self.nextId += 1
        authTagMan = self.authManager.newTagManager()
        halfWidth, height = self.settings.lobbySize
        server = ServerNetHandler(
                layoutDatabase=self.layoutDatabase, netman=self.netman,
                authTagManager=authTagMan, alertSettings=self.alertSettings,
                halfMapWidth=halfWidth, mapHeight=height,
                maxPlayers=self.settings.maxPlayers,
                voting=True, gameName=GAME_NAME)

        def onShutdown():
            self.netman.removeHandler(server)
            del self.servers[gameId]
        server.onShutdown.addListener(onShutdown)
        self.netman.addHandler(server)

        print 'Created game (id=%d)' % (gameId,)
        self.servers[gameId] = server
        return gameId

    @defer.deferredGenerator
    def registerGame(self, game, version, host, port):
        '''
        Registers a remote game with this server.
        '''
        rGame = RegisteredGame(game, version, host, port)
        result = defer.waitForDeferred(rGame.verify())
        yield result
        result = result.getResult()
        if result:
            print 'Registered game on %s:%s' % (host, port)
            self.registeredGames.append(rGame)
        else:
            print 'Failed to connect to game on %s:%s' % (host, port)
            raise authcommands.PortUnreachable()

    def getRegisteredGames(self):
        '''
        Returns a list of registered games which are running.
        '''
        if len(self.registeredGames) == 0:
            return defer.succeed([])

        result = []
        d = defer.Deferred()
        remaining = [len(self.registeredGames)]
        def gameVerified(success, rGame):
            if success:
                result.append(rGame)
            else:
                self.regisiteredGames.remove(rGame)

            remaining[0] -= 1
            if remaining[0] == 0:
                d.callback(result)

        for rGame in self.registeredGames:
            rGame.verify().addCallback(gameVerified, rGame)

        return d

class RegisteredGame(object):
    '''
    Represents a remote game that has been registered with this server.
    '''
    def __init__(self, game, version, host, port):
        self.game = game
        self.version = version
        self.host = host
        self.port = port
        self.lastVerified = 0
        self.running = True

    @defer.deferredGenerator
    def verify(self):
        '''
        If more than GAME_VERIFY_TIME has passed since the last verification,
        connects to the game to check whether it is still running. Returns a
        deferred whose callback will be executed with True or False depending on
        whether the game is still running.
        '''
        t = timeNow()
        if t - self.lastVerified < GAME_VERIFY_TIME:
            yield self.running
            return
        self.lastVerified = t

        p = defer.waitForDeferred(ClientCreator(reactor,
                Protocol).connectTCP(self.host, self.port, timeout=5))
        yield p
        try:
            p = p.getResult()
        except ConnectError:
            self.running = False
            yield False
            return

        # TODO: Check that the game is not full.

        self.running = True
        yield True

class Theme(object):
    '''
    Dummy object which provides enough of the interface of app.Theme for the
    authentication server to get by.
    '''
    def getPath(self, *pathBits):
        return data.getPath(data, *pathBits)

SALT = 'Trosnoth'
class AuthManager(object):
    '''
    Manages user accounts on the system.
    '''
    def __init__(self, dataPath):
        self.dataPath = dataPath
        self.tags = {}      # auth tag -> user id
        self.settings = AuthServerSettings(dataPath)

    def checkUsername(self, username):
        '''
        Returns True or False, depending on whether the given username is
        already in use.
        '''
        return os.path.isdir(os.path.join(self.dataPath, 'accounts',
                username.lower()))

    def newTagManager(self):
        '''
        Returns an authentication tag manager for this set of users.
        '''
        return AuthTagManager(self)

    def authenticateUser(self, username, password):
        '''
        If a username exists with the given password, returns the user,
        otherwise returns None.
        '''
        hash1 = hasher(SALT + password).digest()
        try:
            hash2 = open(os.path.join(self.dataPath, 'accounts',
                    username.lower(), 'password'), 'rb').read()
        except IOError:
            return defer.fail()
        if hash1 == hash2:
            return defer.succeed(AuthenticatedUser(self, username))
        return defer.fail(ValueError('Incorrect password'))

    def getUserByName(self, username):
        return AuthenticatedUser(self, username)

    def createUser(self, username, password, nick=None):
        if self.checkUsername(username):
            raise ValueError('user %r already exists' % (username,))
        path = os.path.join(self.dataPath, 'accounts', username.lower())
        os.makedirs(path)
        user = AuthenticatedUser(self, username)
        user.setPassword(password)
        if nick is not None:
            user.setNick(nick)
        return user

    def getNick(self, username):
        path = os.path.join(self.dataPath, 'accounts', username.lower())
        try:
            return open(os.path.join(path, 'nick'), 'rb').read().decode()
        except IOError:
            return username

class AuthTagManager(object):
    '''
    Provides a gateway for the Validator to confirm that a player has
    authenticated and to check the player's userid.
    '''
    def __init__(self, authManager):
        self.authManager = authManager
        self.tags = {}      # auth tag -> user id

    def checkUsername(self, username):
        '''
        Returns True or False, depending on whether the given username is
        already in use.
        '''
        return self.authManager.checkUsername(username)

    def newTag(self, user):
        tag = random.randrange(1<<64)
        self.tags[tag] = user
        return tag

    def checkAuthTag(self, tag):
        '''
        Returns the authenticated user corresponding to the auth tag, or
        None if the tag is not recognised.
        Don't forget to call discardAuthTag() when the authentication tag is no
        longer valid.
        '''
        return self.tags.get(tag, None)

    def discardAuthTag(self, tag):
        try:
            del self.tags[tag]
        except KeyError:
            pass

class AuthenticatedUser(object):
    '''
    Represents a user which has been authenticated on the system.
    '''
    def __init__(self, authManager, username):
        self.authManager = authManager
        self.username = username
        self._path = os.path.join(authManager.dataPath, 'accounts', username.lower())
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        self._loadAchievements()

    def __eq__(self, other):
        if (isinstance(other, AuthenticatedUser) and other.username ==
                self.username):
            return True
        return False

    def __hash__(self):
        return hash(self.username)

    def isElephantOwner(self):
        return self.username in self.authManager.settings.elephantOwners

    def getNick(self):
        try:
            return open(os.path.join(self._path, 'nick'), 'rb').read().decode()
        except IOError:
            return self.username

    def setNick(self, nick):
        open(os.path.join(self._path, 'nick'), 'wb').write(nick.encode())

    def setPassword(self, password):
        pwdHash = hasher(SALT + password).digest()
        open(os.path.join(self._path, 'password'), 'wb').write(pwdHash)

    def _loadAchievements(self):
        self.achievements = {}
        for achv in achievementDict.iterkeys():
            self.achievements[achv] = {'unlocked' : False}
        try:
            f = open(os.path.join(self._path, 'achievements'), 'r')
        except IOError:
            return
        
        jsonString = f.read()
        f.close()
        try:
            jsonParsed = json.loads(jsonString)
        except ValueError:
            pass
        else:
            self.achievements.update(jsonParsed)
        

    def _saveAchievements(self):
        f = open(os.path.join(self._path, 'achievements'), 'w')
        f.write(json.dumps(self.achievements, indent = 4))
        f.close()

    # Save the achievements which have made progress but are
    # not yet there.
    def saveProgressAchievements(self, playerAchievements):
        for achievement in playerAchievements:
            if isinstance(achievement, OnceEverPerPlayer):
                self.achievements[achievement.idstring] = achievement.JSONString()
        self._saveAchievements()

    def achievementUnlocked(self, msg):
        self.achievements[msg.achievementId] = {'unlocked' : True}
        self._saveAchievements()


def startServer(port=6787, dataPath=None, manholePort=6799, password=None):
    pf = AuthenticationFactory(dataPath)

    factory = telnet.ShellFactory()
    try:
        reactor.listenTCP(manholePort, factory)
    except CannotListenError:
        print 'Error starting manhole on port %d' % (manholePort,)
    else:
        if password is None:
            password = ''.join(random.choice('0123456789') for i in xrange(6))
        factory.namespace['authfactory'] = pf
        factory.username = 'trosnoth'
        factory.password = password
        print 'Manhole started on port %d with password %r' % (manholePort,
                password)

    try:
        reactor.listenTCP(port, pf)
    except CannotListenError:
        print 'Error listening on port %d.' % (port,)
    else:
        print 'Started Trosnoth authentication server on port %d.' % (port,)
        reactor.run()

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-p', '--port', action='store', dest='port', default=6787,
        help='which port to run the authentication server on')
    parser.add_option('-d', '--datapath', action='store', dest='dataPath',
        default=None, help='where to store the authentication server data')
    parser.add_option('-m', '--manhole', action='store', dest='manholePort',
        default=6799, help='which port to run the manhole on')
    parser.add_option('--password', action='store', dest='manholePassword',
        default=None, help='the password to use for the manhole')

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.error('no arguments expected')

    startServer(port=int(options.port), dataPath=options.dataPath,
            manholePort=int(options.manholePort),
            password=options.manholePassword)

if __name__ == '__main__':
    main()
