.. -*- mode: rst; coding: utf-8 -*-

================
mekk.rtmimport
================

``mekk.rtmimport`` handles importing data to RememberTheMilk. At the
moment it handles importing data exported from Nozbe_, I keep more
generic name in case I write other importers in the future.

From Nozbe to RememberTheMilk
=============================

Exporting the data from Nozbe
-----------------------------

Prepare `.json` export of Nozbe_ data. For details see `mekk.nozbe`_
but usually you just want to::

    nozbetool export --json=mynozbedata.json

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

Uploads are not copied (= lost). I neither now how to export them from
Nozbe, nor RTM is able to handle them.

Action name formatting is not available on RememberTheMilk, so if you
used constructs like `Visit "the website":http://google.com`, they will
show up as is.

Sharing information (= delegation to other users) is lost. I haven't used
this feature so I don't know how do underlying data look like.

Source, bugs, patches
=====================

Development `is tracked on BitBucket`_.

.. _is tracked on BitBucket: http://bitbucket.org/Mekk/rtmimport
.. _mekk.nozbe: http://pypi.python.org/pypi/mekk.nozbe/
.. _Nozbe: http://nozbe.com