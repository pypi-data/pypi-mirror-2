.. -*- mode: rst -*-

==========================
oap-cli
==========================
---------------------------------------------------------------
An OAP (OpenVAS Administration Protocol) command line interface
---------------------------------------------------------------

:Author:  Hartmut Goebel <h.goebel@goebel-consult.de>
:Version: Version |VERSION|
:Copyright: GNU Public Licence v3 (GPLv3)
:Manual section: 1

.. raw:: manpage

   .\" disable justification (adjust text to left margin only)
   .ad l


SYNOPSIS
==========


``oap-cli --help``

``oap-cli [options]``

``oap-cli command --help``

``oap-cli command [ command_opts ] [ command_args ]``


DESCRIPTION
============

`oap-cli` is a command line interface for OAP (OpenVAS Administration
Protocol). `oap-cli` let's you e.g. create, modify and delete targets,
tasks, and scan configs, retrieve reports in various formats and so
on.

To get a complete list of implemented OAP commands, run
``oap-cli -help``. To get help on a specific OAP command, run 
``oap-cli COMMAND -help``, e.g. ``oap-cli get-report --help``.

Please see below for some `EXAMPLES`_.


OPTIONS
========

General Options
--------------------

--version             Show program's version number and exit
--help                Show help message, list available commands and exit
-v, --verbose         Be verbose.
-P, --prompt          Prompt to exit.

Options for connecting to the administrator
-------------------------------------------

-h HOST, --host HOST    Connect to administrator on host HOST (default:
                        127.0.0.1)
-p PORT, --port PORT    Use port number PORT (default: 9390)
-u USERNAME, --username USERNAME
                        OAP username (default: current user's name)
-w PASSWORD, --password PASSWORD
                        OAP password (default: same as username)


EXAMPLES
============

:oap-cli get-users --help:
       Print usage, options and positional arguments for fetching a
       inforamtion about users (OAP command <get_users>)

:oap-cli create-user --new-pass xxx john:
       Create a new user `john` with password `xxx` and the default
       role (which is 'User').

:oap-cli get-users john:
       Retreive information about user 'john'


SEE ALSO
=============

Project Homepage http://www.openvas.org/
