.. -*- mode: rst -*-

==========================
omp-cli
==========================
-------------------------------------------------------------
An OMP (OpenVAS Management Protocol) command line interface
-------------------------------------------------------------

:Author:  Hartmut Goebel <h.goebel@goebel-consult.de>
:Version: Version 0.0.1
:Copyright: GNU Public Licence v3 (GPLv3)
:Manual section: 1

.. raw:: manpage

   .\" disable justification (adjust text to left margin only)
   .ad l


SYNOPSIS
==========


``omp-cli --help``

``omp-cli [options]``

``omp-cli command --help``

``omp-cli command [ command_opts ] [ command_args ]``


DESCRIPTION
============

`omp-cli` is a command line interface for OMP (OpenVAS Management
Protocol). `omp-cli` let's you e.g. create, modify and delete
targets, tasks, and scan configs, retrieve reports in various formats
and so on.

To get a complete list of implemented OMP commands, run
``omp-cli -help``. To get help on a specific OMP command, run 
``omp-cli COMMAND -help``, e.g. ``omp-cli get-report --help``.

Please see below for some `EXAMPLES`_.


OPTIONS
========

General Options
--------------------

--version             Show program's version number and exit
--help                Show help message, list available commands and exit
-v, --verbose         Be verbose.
-P, --prompt          Prompt to exit.

Options for connecting to the manager
---------------------------------------

-h HOST, --host HOST  Connect to manager on host HOST (default: 127.0.0.1)
-p PORT, --port PORT  Use port number PORT (default: 9390)
-u USERNAME, --username USERNAME
                        OMP username (default: current user's name)
-w PASSWORD, --password PASSWORD
                        OMP password (default: same as username)


EXAMPLES
============

:omp-cli get-report --help:
       Print usage, options and positional arguments for fetching a
       report (OMP command <get_report>)

:omp-cli get-report -fPDF 343435d6-91b0-11de-9478-ffd71f4c6f30:
       Retreive a report in PDF format.

SEE ALSO
=============

Project Homepage http://www.openvas.org/
