Detailed Documentation
**********************

Introduction
============

The activity-API reads the character-activity-sheet from the Armory to get the five last actions of the character.

Usage
=====

To use the API, just do an import like this

::

    >>> from activity_api import Activity

Mock Realmstatus.get_realm_status
Returns output similar to what we would get from the API,  so
that this test can be used while offline

::

    >>> from test_activity import mocked_get_activity

Mocking the functions

::

    >>> Activity.get_activity = mocked_get_activity

First create an instance of the Activity object

::

    >>> activity = Activity()

To get the recent activities, use get_activity(name, realm, zone)

::

    >>> activities = activity.get_activity("Kutschurft", "Azshara", "EU")
    >>> test_activities = [u'Earned the achievement [Neck-Deep in Vile (10 player)].',
    ...                    u'Has now completed [Victories over the Lich King (Icecrown 10 player)] 4 times.',
    ...                    u'Has now completed [Sindragosa kills (Heroic Icecrown 10 player)] 2 times.',
    ...                    u'Has now completed [Valithria Dreamwalker rescues (Heroic Icecrown 10 player)] 4 times.',
    ...                    u'Has now completed [Blood Queen Lanathel kills (Heroic Icecrown 10 player)] 6 times.']

    >>> activities == test_activities
    True

Contributors
************

Marc Goetz, Author

Download
********
