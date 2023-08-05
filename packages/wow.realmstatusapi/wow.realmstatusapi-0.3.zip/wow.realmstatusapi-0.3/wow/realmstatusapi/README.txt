Detailed Documentation
**********************

Introduction
============

The realmstatus-API reads the realmstatus-xml from wow-europe.com to get the status of a specified realm ("Realm Up/Realm Down") and
the type of the realm (PvE,PvP etc.).

Usage
=====

To use the API, just do an import like this

::

    >>> from realmstatus_api import Realmstatus

Mock Realmstatus.get_realm_status and Realmstatus.get_realm_type
Returns output similar to what we would get from the API,  so
that this test can be used while offline

::

    from test_realmstatus.py import mocked_get_realm_status, mocked_get_realm_type

Mocking the functions

::

    >>> Realmstatus.get_realm_status = mocked_get_realm_status
    >>> Realmstatus.get_realm_type = mocked_get_realm_type

First create an instance of the Realmstatus object

::

    >>> realmstatus = Realmstatus()

To get the status of a realm, use get_realm_status(name)

::

    >>> status = realmstatus.get_realm_status("Azshara")
    >>> status == "Realm Up"
    True

To get the type of a realm, use get_realm_type(name)

::

    >>> type = realmstatus.get_realm_type("Azshara")
    >>> type == "PvP"
    True

Contributors
************

Marc Goetz, Author

Download
********
