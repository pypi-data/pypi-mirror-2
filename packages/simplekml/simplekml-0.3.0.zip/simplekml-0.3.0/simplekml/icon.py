"""
simplekml
Copyright 2011 Kyle Lancaster

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact me at kyle.lan@gmail.com
"""

from base import Kmlable

class Icon(Kmlable):
    """Defines an image associated with an Icon style or overlay."""
    def __init__(self, href=" "):
        self.href = href


class ItemIcon(Kmlable):
    """Defines an image associated with an Icon style or overlay."""
    def __init__(self, state=None, href=None):
        self.href = href
        self.state = state