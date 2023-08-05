>>> from realmstatus_api import Realmstatus

mock Realmstatus.get_realm_status
returns output similar to what we would get from the API
so that this test can be used while offline
>>> def mocked_get_realm_status(self, name):
...
...    if name == "Azshara":
...        return "Realm Up"
...    else:
...        return "Realm not found"

mock Realmstatus.get_realm_status
returns output similar to what we would get from the API
so that this test can be used while offline
>>> def mocked_get_realm_type(self, name):
...
...    if name == "Azshara":
...        return "PvP"
...    else:
...        return "Realm not found"

mocking the functions
>>> Realmstatus.get_realm_status = mocked_get_realm_status
>>> Realmstatus.get_realm_type = mocked_get_realm_type

>>> realmstatus = Realmstatus()

>>> status = realmstatus.get_realm_status("Azshara")
>>> status == "Realm Up"
True

>>> type = realmstatus.get_realm_type("Azshara")
>>> type == "PvP"
True
