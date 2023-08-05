Introduction
============

The package is meant to be used with the Plone3 theme collective.wowlichking,
but it is not required.

It includes a custom contenttype (wowcharacter) and a custom view (@@wowcharacter).

wowcharacter
------------

The contenttype represents a World of Warcraft character.
When creating one, you need to state the Name and Realm of the character,
also its fraction (Horde/Alliance) and its zone (EU/US).

@@wowhcaracter
--------------

The view uses an API to communicate with the WoW-Armory to display additional
information about the character, like class, guild, talent specs, professions, equip etc.
It also implements the wowhead-Tooltip for showing a WoW-ingame-like tooltip when hovering 
over the equip-icons.
