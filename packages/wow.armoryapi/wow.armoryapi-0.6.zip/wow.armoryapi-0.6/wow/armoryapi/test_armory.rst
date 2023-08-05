>>> from armory_api import Armory

mock Armory.getCharacter
returns a dictionary similar to the dictionary we would get from the API
so that this test can be used while offline
>>> def mocked_getCharacter(self, raiderName, raiderServer, raiderZone):
...
...    d = {}
...    d["name"] = raiderName
...    d["server"] = raiderServer
...    d["zone"] = raiderZone
...
...    return d

mocking the function
>>> Armory.getCharacter = mocked_getCharacter

>>> raider = Armory().getCharacter("Kutschurft","Azshara","EU")

>>> name = raider.get("name")
>>> name == "Kutschurft"
True

>>> server = raider.get("server")
>>> server == "Azshara"
True

>>> zone = raider.get("zone")
>>> zone == "EU"
True
