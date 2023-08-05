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

# DEBUG: If this flag is set, profile information will be printed on exit.
profileMe = False

# DEBUG: If this flag is set, all game information will be saved to a log file.
logMe = False

import sys, pygame, os
from twisted.internet import reactor, task
from twisted.internet.error import CannotListenError
from twisted.python import log

from trosnoth.src.settings import DisplaySettings, SoundSettings
from trosnoth.src.trosnothgui import interface
from trosnoth.src.themes import Theme
from trosnoth.src.model import universe
from trosnoth.src.trosnothgui import defines
from trosnoth.src.utils import logging
from trosnoth.src.network.networkDefines import serverVersion

from trosnoth.src.gui import app

from trosnoth.src.network.netman import NetworkManager
from trosnoth.src.network.trosnothdiscoverer import TrosnothDiscoverer


class Main(app.MultiWindowApplication):
    '''Instantiating the Main class will set up the game. Calling the run()
    method will run the reactor. This class handles the three steps of joining
    a game: (1) get list of clients; (2) connect to a server; (3) join the
    game.'''

    def __init__(self):
        '''Initialise the game.'''

        self.initNetwork()

        self.displaySettings = DisplaySettings(self)
        self.soundSettings = SoundSettings(self)

        if self.displaySettings.fullScreen:
            options = pygame.locals.FULLSCREEN
        else:
            options = 0
        universe.init()
        
        super(Main, self).__init__(
            self.displaySettings.getSize(),
            options,
            defines.gameName,
            interface.Interface)
        
        # Set the master sound volume.
        self.soundSettings.apply()

        # Since we haven't connected to the server, there is no world.
        self.player = None

    def __str__(self):
        return 'Trosnoth Main Object'

    def initNetwork(self):
        self.server = None

        # Set up the network connection.
        try:
            self.netman = NetworkManager(6789, 6789)
        except CannotListenError:
            # Set up a network manager on an arbitrary port (i.e.
            # you probably cannot run an Internet server because you
            # won't have port forwarding for the correct port.)
            self.netman = NetworkManager(0, None)
            
            # TODO: Perhaps show a message on the interface warning that games
            # may not be visible on the Internet.

        # Set up the game discovery protocol.
        self.discoverer = TrosnothDiscoverer(self.netman)

    def stopping(self):
        # Shut down the server if one's running.
        if self.server is not None:
            self.server.shutdown()

        # Save the discoverer's peers.
        self.discoverer.kill()

        super(Main, self).stopping()

    def initialise(self):
        super(Main, self).initialise()

        # Loading the theme loads the fonts.
        self.theme = Theme(self)

    def getFontFilename(self, fontName):
        '''
        Tells the UI framework where to find the given font.
        '''
        return self.theme.getPath('fonts', fontName)

    def changeScreenSize(self, size, fullScreen):
        if fullScreen:
            options = pygame.locals.FULLSCREEN
        else:
            options = 0
        
        self.screenManager.setScreenProperties(size, options, defines.gameName)   

    def startServer(self, serverName, halfMapWidth=None, mapHeight=None,
                    maxPlayers=None, gameDuration=None, recordReplay=None,
                    invisibleGame=False):
        'Starts a server.'
        if self.server is not None:
            if self.server.running:
                return
        settings = {}
        
        if halfMapWidth != None:
            settings['halfMapWidth'] = halfMapWidth
        if mapHeight != None:
            settings['mapHeight'] = mapHeight
        if maxPlayers != None:
            settings['maxPlayers'] = maxPlayers
        if gameDuration != None:
            settings['gameDuration'] = gameDuration
        if recordReplay != None:
            settings['recordReplay'] = recordReplay
            
        from trosnoth.src.network.networkServer import ServerNetHandler

        try:
            self.server = ServerNetHandler(self.netman, serverName,
                    settings=settings)
        except:
            # Creating a local server failed
            logging.writeException()
        else:
            # Tell the discovery protocol about it.
            if not invisibleGame:
                info = {
                    'name': serverName,
                    'version': serverVersion,
                }
                self.discoverer.setGame(info)
                self.server.onShutdown.addListener(self._serverShutdown)

    def _serverShutdown(self):
        self.discoverer.delGame()
        self.server = None

def runGame():
    if logMe:
        logging.startLogging()
    
    mainObject = Main()
    
    try:
        mainObject.run_twisted()
    finally:
        if logMe:
            logging.endLogging()

        if 'checkpoint' in sys.argv:
            from trosnoth.src.utils.checkpoint import saveCheckpoints
            saveCheckpoints()

if __name__ == '__main__':
    if profileMe:
        import cProfile as profile
        profile.run('runGame()')
        raw_input('Press enter:')
    else:
        runGame()
