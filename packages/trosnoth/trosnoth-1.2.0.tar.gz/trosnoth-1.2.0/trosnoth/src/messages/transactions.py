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

from trosnoth.src.utils.components import Message

class AddingStars(Message):
    fields = 'teamd', 'player', 'numStars'

class StartedTransaction(Message):
    fields = 'transaction',

class AddedStars(Message):
    fields = 'team', 'player', 'numStars'

class TransactionComplete(Message):
    fields = 'team', 'player', 'upgradeType', 'transaction'

class DeleteUpgrade(Message):
    fields = 'player', 'upgrade'

class UseUpgrade(Message):
    fields = 'player',
    
class AbandonTransaction(Message):
    fields = 'transaction', 'reason'


class TransactionChanged(Message):
    fields = 'transaction',

class MinimapStarted(Message):
    fields = 'player',

class MinimapEnded(Message):
    fields = 'player'

class TurretStarted(Message):
    fields = 'player',

class TurretEnded(Message):
    fields = 'player',