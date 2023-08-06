Introduction
============

The package is meant to be used with the Plone3 theme collective.wowlichking,
but it is not required.

Best viewed with Mozilla Firefox.

It includes a custom contenttype (wowcharacter), a custom view (@@wowcharacter) and a custom portlet (realmstatus).

wowcharacter
------------

The contenttype represents a World of Warcraft character.
When creating one, you need to state the Name and Realm of the character,
also its faction (Horde/Alliance) and its zone (EU/US).

@@wowhcaracter
--------------

The view uses two APIs to communicate with the WoW-Armory to display additional
information about the character, like class, guild, talent specs, professions, equip, recent activities etc.
It also implements the wowhead-Tooltip for showing a WoW-ingame-like tooltip when hovering
over the equip-icons.

realmstatus
-----------

The portlet uses an API to fetch the realmstatus-xml from wow-europe.com to display the status of the realm
of the actual character.  It also displays the name and the type of the realm.
