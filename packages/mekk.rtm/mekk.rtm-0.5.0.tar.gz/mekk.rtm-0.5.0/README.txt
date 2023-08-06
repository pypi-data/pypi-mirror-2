.. -*- mode: rst; coding: utf-8; compile-command: "rst2html README.txt /tmp/README.html" -*-

================
mekk.rtm
================

``mekk.rtm`` provides both RememberTheMilk_ client library (which you
can use to write client programs/libraries using relatively simple
API) and a few command-line utilities (which you can use to manage
your datea, for example import, export, massively tag, move between
lists etc).

.. contents::
   :local:
   :backlinks: none
   :depth: 2

Using mekk.rtm as client library
======================================

Contrary to two other python RememberTheMilk_ clients (RtmAPI_ and
pyrtm_), ``mekk.rtm`` tries to provide elaborate API with enumerated
explicit parameters and structured results. It is also tested with
some unittests.

For detailed documentation see inline docs of `mekk.rtm.RtmClient`_. Here is
simple example (see also longer `sample/sample_client.py`_ in package
sources, to get api key and shared secret visit 
`this page <http://www.rememberthemilk.com/services/api/keys.rtm>`_)::

    from mekk.rtm import RtmClient, create_and_authorize_connector_prompting_for_api_key

    APP_NAME = "mekk.rtm sample"

    connector = create_and_authorize_connector_prompting_for_api_key(APP_NAME)
    #
    # Function above interactively prompts for api key and shared secret and
    # preserves acquired data in keyring. This is useful for testing, but in
    # normal case you are more likely to do:
    #
    #    connector = create_and_authorize_connector(APP_NAME, API_KEY, SHARED_SECRET)

    client = RtmClient(connector)

    print "Normal lists: "
    for l in client.known_lists():
        if not l.archived:
            print u"%s (%s)" % (l.id, l.name)

    print "Smart lists: "
    for l in client.known_smart_lists():
        if not l.archived:
            print u"%s (%s, %s)" % (l.id, l.name, l.filter)

    test_list = client.find_or_create_list(u"The testing list")
    print "Test list: ", test_list

    another_list = client.find_or_create_list(u"The testing list")
    print "Another list: ", another_list

    task1 = client.create_task(
        u"Write some unit tests",
        list_id = test_list.id,
        tags = ["testy", "@dom"],
        priority = 3,
        due_date = "2010-11-30",
        estimate = "1 day 10 hours",
        repeat = "after 3 days",
        url = "http://en.wikipedia.org/wiki/Unit_testing",
        completed = False,
        notes = [ (u"Runner", u"Use nose to run them all\nIt is simplest"),
                  (u"Helper", u"And mock can help to wrap backend apis\nwithout calling them") ])
    print "Created task", task1

    task2 = client.create_task(
        u"Less serious one",
        list_id = test_list.id)
    print "Created task", task2

    task3 = client.create_task(
        u"Less serious one",
        list_id = another_list.id,
        tags = ["testy"])
    print "Created task", task3

    print "All incomplete tasks with notes on first list:"
    for t in client.find_tasks(list_id = test_list.id, filter = "status:incomplete and hasNotes:true"):
        print t

    task2 = client.update_task(
        task2.key,
        completed = True)
    print "Updated task", task2

    print "All incomplete tasks tagged 'testy':"
    for t in client.find_tasks(filter = "tag:testy and status:incomplete"):
        print t

.. _RtmAPI: http://pypi.python.org/pypi/RtmAPI/
.. _pyrtm: http://bitbucket.org/srid/pyrtm/
.. _sample/sample_client.py: http://bitbucket.org/Mekk/rtmimport/src/tip/sample/sample_client.py
.. _mekk.rtm.RtmClient: http://bitbucket.org/Mekk/rtmimport/src/tip/src/mekk/rtm/rtm_client.py

Using mekk.rtm as command-line tool
======================================

``mekk.rtm`` offers a few command-line helpers (mostly related to the
things original web interface fails to provide).

.. _RememberTheMilk: http://www.rememberthemilk.com

--------------------------------------------
Updating tags on many tasks (`rtmtag`)
--------------------------------------------

*Not yet implemented (but planned soon)*

---------------------------------------------
Moving many tasks to another list (`rtmmove`)
---------------------------------------------

*Not yet implemented (but planned soon)*

--------------------------------------------
Exporting RememberTheMilk data (`rtmexport`)
--------------------------------------------

*Not yet implemented (but planned soon)*

--------------------------------------------
Importing exported data back (`rtmimport`)
--------------------------------------------

*Not yet implemented (but planned soon)*

----------------------------------------------------------
Importing data from Nozbe to RememberTheMilk (`rtmimport`)
----------------------------------------------------------

*For obvious reasons (I already imported my data) I don't test
this module on every release. Make dry run before actually running
the import and report bugs if they happen.*

Exporting the data from Nozbe
-----------------------------

Prepare `.json` export of Nozbe_ data. For details see `mekk.nozbe`_
but usually you just want to::

    nozbetool export --user=MyNozbeName --json=mynozbedata.json

Importing data to RememberTheMilk
---------------------------------

First make a test run::

    rtmimport --nozbe-json=mynozbedata.json --verbose --dry-run

(it does not store anything, just prints what it is to do) and verify
whether everything seems correct. 

Then make actual import::

    rtmimport --nozbe-json=mynozbedata.json --verbose

(or omit `--verbose` if you don't want to track progress, but I
recommend you keep it)

Note: import can take some time. In case of my big list over
not-so-good network it has been running for almost an hour.

How the data is converted
-------------------------

Nozbe projects are saved as RememberTheMilk lists.

Nozbe contexts are converted to RememberTheMilk tags. `@` is prepended
to their names and non-alphanumeric characters are replaced with
dashes (so for example `My home/kitchen` becomes
`@My-home-kitchen`). 

Next actions are tagged as `Next`.

Actions are saved as tasks. Name, due date, recurrence, 
estimated cost and completion status are all saved.

In case of recurrence, RTM ``every`` mode is used (so the task marked
on Nozbe as recurring every week will be spawned 52 times a year by
RTM, whether user completes it, or not). If you prefer alternative way
(spawning new incarnation whenever previous is completed), edit tasks
after import, patch the code (and replace `every` with `after`), or
ask me for a commandline flag).

As notes are bound to projects on Nozbe, and to tasks on
RememberTheMilk, I save notes by creating artificial tasks named "Save
this note" (one per every list for which appropriate project had notes)
and binding notes to those tasks. This must be handled afterwards
using RTM interface, to make sure it happens I mark those tasks as due
immediately. Those task are also tagged as `Note`.

Limitations
-----------

Only main context is copied, additional contexts are lost. I don't know
how to grab them from Nozbe_ (in case somebody knows how to patch
`mekk.nozbe`_ to grab all contexts, I can extend this importer easily
to handle them all).

Uploads are not copied at all. I neither now how to export them from
Nozbe, nor how could I handle them afterwards (RTM has no uploads).

Action name formatting is not available on RememberTheMilk, so if you
used constructs like `Visit "the website":http://google.com`, they will
show up as is.

Sharing information (= information about delegations to other users)
is lost. I haven't used this feature so I don't know how do the
underlying data look like.

Some contexts could probably be converted to locations, not tags, but
I don't have an idea how to decide which way to go.

Problems and workarounds
------------------------

If import process is interrupted, re-running it would make duplicate
tasks (there is no duplicate checking, it would be costly). The best
way to resolve it is to open .json file in text editor (after making a
backup copy of it) and simply cut all actions which are already saved
(they are saved in order, so it is just a matter of locating the last
action saved before the process was interrupted and cutting all actions
up to this one).



Source, bugs, patches
=====================

Development `is tracked on BitBucket`_. Clone from there, report bugs
there, offer patches there.

.. _is tracked on BitBucket: http://bitbucket.org/Mekk/rtmimport
.. _mekk.nozbe: http://pypi.python.org/pypi/mekk.nozbe/
.. _Nozbe: http://nozbe.com