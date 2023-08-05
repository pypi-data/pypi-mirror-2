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

'''prompt.py - contains the definition for a prompt that could be used for
any type of input.'''

import pygame
import trosnoth.src.gui.framework.framework as framework
from trosnoth.src.gui.common import defaultAnchor
from trosnoth.src.utils.event import Event
from trosnoth.src.gui import keyboard

def intValidator(char):
    return char >= '0' and char <= '9'

class InputBox(framework.Element):
    # TODO: define these in terms of font size rather than pixels
    pxFromLeft = 2
    pxFromRight = 5
    pxToSkipWhenCursorGoesToTheRight = 90
    cursorFlashTime = 0.6
    def __init__(self, app, area, initValue='', validator=None,
                 font=None, colour=(255,255,255), 
                 maxLength=None):
        super(InputBox, self).__init__(app)
        
        self.area = area
        self.onClick = Event()
        self.onEnter = Event()
        self.onTab = Event()
        self.onEsc = Event()
        self.onEdit = Event()
        
        if validator:
            self.validator = validator
        else:
            self.validator = lambda x: True

            
        if font:
            self.font = font
        else:
            self.font = self.app.screenManager.fonts.defaultTextBoxFont
            
        self.value = initValue
        self.maxLength = maxLength
        self.fontColour = (0,0,0)
        self.backColour = colour
        self.cursorColour = (255, 0, 0)
        self._cursorVisibleAtThisMoment = True
        self._timeToFlash = self.cursorFlashTime

        # Calculate the white part of the input area
        self.cursorIndex = len(self.value)
        self.offset = 0

    def setValue(self, value):
        self.value = value
        self.cursorIndex = len(self.value)

    def getValue(self):
        return self.value

    def _getSize(self):
        return self._getRect().size

    def _getCursorImage(self):
        s = pygame.Surface((2, min(int(self.font.getHeight(self.app)*0.6), \
                                   self._getSize()[1] * 0.8)))
        s.fill(self.cursorColour)
        return s
    
    def _getRect(self):
        return self.area.getRect(self.app)

    def _getPt(self):
        return self._getRect().topleft

    def setFontColour(self, fontColour):
        self.fontColour = fontColour

    def setBackColour(self, backColour):
        self.backColour = backColour

    def setCursorColour(self, cursorColour):
        self.cursorColour = cursorColour

    def gotFocus(self):
        self._cursorVisibleAtThisMoment = True
        self._timeToFlash = self.cursorFlashTime

    def draw(self, surface):
        rect = self._getRect()
        size = rect.size
        pos = rect.topleft
        # Fill the input area with the specified colour
        surface.fill(self.backColour, rect)
        
        # Put what's currently inputted into the input area
        inputText = self.font.render(self.app, self.value, True, self.fontColour, self.backColour)
        
        # Adjust offset
        if self._getCursorPos() < self.offset:
            self.offset = max(0, self.offset - self.pxToSkipWhenCursorGoesToTheRight)
        elif self._getCursorPos() > self.offset + size[0] - (self.pxFromRight+self.pxFromLeft):
            self.offset = self._getCursorPos() - size[0] + (self.pxFromRight+self.pxFromLeft)
            
        text_rect = inputText.get_rect()
        text_rect.centery = rect.centery
        diff = (text_rect.height - rect.height) / 2
        # Find the currently-displaying text (based on where the cursor is):
        area = pygame.Rect(self.offset, diff, size[0] - self.pxFromRight, \
                           rect.height)

        # Put the text on the screen
        surface.blit(inputText, (pos[0]+self.pxFromLeft, rect.top), area)

        # Add the cursor where it is.
        if self.hasFocus and self._cursorVisibleAtThisMoment:
            cs = self._getCursorImage()
            cursor_rect = cs.get_rect()
            cursor_rect.centery = rect.centery
            surface.blit(cs, (pos[0] + self._getCursorPos() - self.offset,
                                                    cursor_rect.top))

    def _getCursorPos(self):
        return self.font.size(self.app, self.value[:self.cursorIndex])[0]+1

    # Get the index of the position clicked
    def __getCursorIndex(self, clickOffset):
        totalOffset = clickOffset + self.offset + self.pxFromLeft
        i = 1
        fontOffset = 0
        last = 0
        while fontOffset < totalOffset and i <= len(self.value):
            last = fontOffset
            fontOffset = self.font.size(self.app, self.value[:i])[0]
            i += 1
        if (fontOffset - totalOffset) <= (totalOffset - last):
            return i - 1
        else:
            return i - 2
        return i

    def processEvent(self, event):
        '''Processes the key press. If we use the event, return nothing.
        If we do not use it,
        return the event so something else can use it.'''
        
        if self.hasFocus and event.type == pygame.locals.KEYDOWN:
            self._cursorVisibleAtThisMoment = True
            self._timeToFlash = self.cursorFlashTime
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.onEnter.execute(self)
                return None
            if event.key == pygame.K_ESCAPE:
                self.onEsc.execute(self)
                return None
            if event.key == pygame.K_TAB:
                self.onTab.execute(self)
                return None

            # Delete the letter behind the cursor
            if event.key == pygame.K_BACKSPACE:
                # Make sure there's something in the string behind the cursor
                # first, don't want to kill what's not there
                if self.cursorIndex > 0:
                    letterGone = self.value[self.cursorIndex - 1]
                    self.value = self.value[:self.cursorIndex - 1] + \
                                         self.value[self.cursorIndex:]
                    self.cursorIndex -= 1
                    self.onEdit.execute(self)

            elif event.key == pygame.K_DELETE:
                # Make sure there's something in the string in front of the
                # cursor first, don't want to kill what's not there
                if self.cursorIndex < len(self.value):
                    letterGone = self.value[self.cursorIndex]
                    self.value = self.value[:self.cursorIndex] + \
                                 self.value[self.cursorIndex + 1:]
                    self.onEdit.execute(self)


            # Move the cursor back one character
            elif event.key == pygame.K_LEFT:
                if self.cursorIndex > 0:
                    self.cursorIndex -= 1


            # Move the character forward one character
            elif event.key == pygame.K_RIGHT:
                if self.cursorIndex < len(self.value):
                    self.cursorIndex += 1


            # Move the cursor to the end of the input
            elif event.key == pygame.K_END:
                self.cursorIndex = len(self.value)


            # Move the cursor to the start of the input
            elif event.key == pygame.K_HOME:
                self.cursorIndex = 0
                self.offset = 0

            # Add the character to our string
            elif event.unicode == u'':
                return event
            else:
                # Validate the input.
                if not self.validator(event.unicode):
                    return event

                # Check the maxLength
                if self.maxLength is not None:
                    if len(self.value) >= self.maxLength:
                        return event
                
                # Add the typed letter to the string
                self.value = self.value[:self.cursorIndex] + \
                                     event.unicode + \
                                     self.value[self.cursorIndex:]
                self.cursorIndex += len(event.unicode)
                self.onEdit.execute(self)

        else:
            rect = self._getRect()
                
            if event.type == pygame.locals.MOUSEBUTTONDOWN and \
             rect.collidepoint(event.pos) and event.button == 1:
                self.onClick.execute(self)
                xOffset = event.pos[0] - rect.left
                self.cursorIndex = self.__getCursorIndex(xOffset)
                self._timeToFlash = self.cursorFlashTime
                self._cursorVisibleAtThisMoment = True
            else:
                # It's not a keydown event. Pass it on.
                return event

    def tick(self, deltaT):
        self._timeToFlash -= deltaT
        while self._timeToFlash < 0:
            self._timeToFlash += self.cursorFlashTime
            self._cursorVisibleAtThisMoment = not self._cursorVisibleAtThisMoment
        

class KeycodeBox(framework.Element):
    # TODO: This class should probably also catch keyboard modifiers.
    pxFromLeft = 2
    pxFromRight = 5
    def __init__(self, app, area, initValue=None, font=None, colour=(255,255,255),
            focusColour=(192, 192, 255)):
        super(KeycodeBox, self).__init__(app)
        
        self.area = area
        self.onClick = Event()
        self.onChange = Event()
        
        if font:
            self.font = font
        else:
            self.font = self.app.screenManager.fonts.defaultTextBoxFont
            
        self.value = initValue
        self.fontColour = (0,0,0)
        self.realBackColour = self._backColour = colour
        self.focusColour = focusColour

    def _getBackColour(self):
        return self._backColour
    def _setBackColour(self, colour):
        if self.realBackColour == self._backColour:
            self.realBackColour = colour
        self._backColour = colour
    backColour = property(_getBackColour, _setBackColour)

    def draw(self, surface):
        rect = self._getRect()
        size = rect.size
        pos = rect.topleft

        # Fill the input area with the specified colour
        surface.fill(self.realBackColour, rect)
        
        # Put what's currently inputted into the input area
        if self.value is None:
            name = ''
        else:
            name = keyboard.shortcutName(self.value)

        inputText = self.font.render(self.app, name, True, self.fontColour,
                        self.realBackColour)
        
        text_rect = inputText.get_rect()
        
        area = pygame.Rect(0, 0, size[0] - self.pxFromRight, rect.height)

        # Put the text on the screen
        text_rect.centery = rect.centery
        surface.blit(inputText, (pos[0]+self.pxFromLeft, rect.top), area)

    def processEvent(self, event):
        '''Processes the key press. If we use the event, return nothing.
        If we do not use it,
        return the event so something else can use it.'''
        
        if self.hasFocus and event.type == pygame.locals.KEYDOWN:
            # Catch a single keystroke.
            self.value = event.key
            self.hasFocus = False
            self.lostFocus()
            self.onChange.execute(self)
        else:
            rect = self._getRect()
                
            if event.type == pygame.locals.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
                self.onClick.execute(self)
            else:
                # It's not a keydown event. Pass it on.
                return event

    def _getSize(self):
        return self._getRect().size

    def _getRect(self):
        return self.area.getRect(self.app)

    def _getPt(self):
        return self._getRect().topleft

    def gotFocus(self):
        self.realBackColour = self.focusColour
    
    def lostFocus(self):
        self.realBackColour = self._backColour
