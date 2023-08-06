Detailed Documentation
**********************

Introduction
============

The armory-API is a modified version of the armorypy @ http://code.google.com/p/armorypy/.

The additional info you can get from it:

- Primary & secondary spec with name and icon (to build a icon link with wowhead or wow-europe)
- Major and minor glyphs for the active spec with name, type and effect
- 2v2, 3v3 and 5v5 arenateams with name, rating and ranking
- Secondary professions (cooking, fishing etc.) with name and value
- Prefix titles, such as Private, Twilight Vanquisher etc.

Usage
=====

To use the API, just do an import like this

::

    >>> from armory_api import Armory

Mock Armory.getCharacter

Returns a dictionary similar to the dictionary we would get from the API,  so 
that this test can be used while offline

::

    >>> from test_armory import mocked_getCharacter

Mocking the function

::

    >>> Armory.getCharacter = mocked_getCharacter

First create an instance of the Armory object

::

    >>> armory = Armory()

To get the character info, use getCharacter(name, realm, zone, language)
currently only "de" and "en" are supported

::

    >>> raider = armory.getCharacter("Kutschurft","Azshara","EU", "en")

Now you can get the info with get(<key>)

::

    >>> name = raider.get("name")
    >>> name == "Kutschurft"
    True

    >>> server = raider.get("server")
    >>> server == "Azshara"
    True

    >>> zone = raider.get("zone")
    >>> zone == "EU"
    True
