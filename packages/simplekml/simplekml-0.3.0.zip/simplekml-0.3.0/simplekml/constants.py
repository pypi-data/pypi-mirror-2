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

class AltitudeMode(object):
    """Constants for AltitudeMode constants."""
    clamptoground = "clampToGround"
    relativetoground = "relativeToGround"
    absolute = "absolute"


class ColorMode(object):
    """Constants for ColorMode constants."""
    normal = "normal"
    random = "random"

class DisplayMode(object):
    """Constants for DisplayMode constants."""
    default = "default"
    hide = "hide"


class ListItemType(object):
    """Constants for ListItemType constants."""
    check = "check"
    radiofolder = "radioFolder"
    checkoffonly = "checkOffOnly"
    checkhidechildren = "checkHideChildren  "

