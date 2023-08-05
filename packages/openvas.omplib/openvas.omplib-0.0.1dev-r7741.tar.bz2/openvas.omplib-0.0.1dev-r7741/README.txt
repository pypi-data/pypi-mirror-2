.. -*- mode: rst -*-

==========================
`openvas.omplib`
==========================

------------------------------------------------------------------
An OMP (OpenVAS Management Protocol) client interface for Python.
------------------------------------------------------------------

:Author:  Hartmut Goebel <h.goebel@goebel-consult.de>
:Version: Version 0.0.1
:Copyright: GNU Public Licence v3 (GPLv3)
:Homepage: http://www.openvas.org/

`OpenVAS`__ (Open Vulnerability Assessment System) is a network security
scanner with associated tools. OpenVAS Version 3 introduces a new core
component: The OpenVAS-Manager, a layer between OpenVAS-Scanner and
various client applications such as OpenVAS-Client or Greenbone
Security Assistant. Among other features, it adds server-side storage
of scan results and it makes it unnecessary for a scan client to keep
the connection open until the scan finishes.

__ http://www.openvas.org

OpenVAS Management Protocol (OMP) is the protocol based on XML to talk
to the OpenVAS-Manager. `openvas.omplib` is a pure-Python
implementation of OMP which allows easy access to the OpenVAS-Manager.

This package also includes a command line tool `omp-cli` which uses
sub-commands like svn or openssl does. See examples below.


Example::

    manager = openvas.omplib.OMPClient(host=sensor)
    manager.open(username, password)
    manager.create_target(job_name, targets, comment)
    task_id = manager.create_task(job_name, comment, config=config_name,
                                  target=job_name)
    report_id = manager.start_task(task_id)
    # ... later ...
    report = manager.get_report(report_id)
    print etree.tostring(report)

`openvas.opmlib` also supports a low-level interface where you can send
OMP XML directly::

    help_text = manager.xml('<help/>')


Examples for `omp-cli` usage::

    omp-cli --help             # get help
    omp-cli get-report --help  # get help on subcommand get-report
    omp-cli get-status         # list tasks with stati and report-ids

                               # Retreive a report in PDF format
    omp-cli get-report -fPDF 343435d6-91b0-11de-9478-ffd71f4c6f30 \
                       -o some-report.pdf

.. 
  For more information please refer to the manpage or visit
  the `project homepage <http://pdfposter.origo.ethz.ch/>`_.


Requirements and Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`openvas.omplib` requires

* `Python 2.5`__ or higher with SSL support (which should be the
   default on most platforms) (NB: Python 3.x is *not* supported)
* `setuptools`__ for installation (see below).
* `argparse`__ (already included in Python starting with Python 2.7)

__ http://www.python.org/download/
__ http://pypi.python.org/pypi/setuptools
__ http://pypi.python.org/pypi/argparse


:Hints for installing on Windows: Following the links above you will
   find .msi and .exe-installers. Simply install them and continue
   with `installing openvas.omplib`_.

:Hints for installing on Linux: Most current Linux distributions
   provide packages for the requirements. Look for packages names like
   `python-setuptools` and `python-argparse`. Simply install them and
   continue with `installing openvas.omplib`_.

:Hint for installing on other platforms: Many vendors provide Python.
   Please check your vendors software repository. Otherwise please
   download Python 2.6 (or any higer version from the 2.x series) from
   http://www.python.org/download/ and follow the installation
   instructions there.

   After installing Python, install `setuptools`__. You may want to
   read `More Hints on Installing setuptools`_ first.

__ http://pypi.python.org/pypi/setuptools

   Using setuptools, compiling and installing the remaining
   requirements is a piece of cake::

     # if the system has network access
     easy_install argparse

     # without network access download argparse
     # from http://pypi.python.org/pypi/argparse and run
     easy_install argparse-*.zip


Installing openvas.omplib
---------------------------------

When you are reading this you most probably already downloaded and
unpacked `openvas.omplib`. Thus installing is as easy as running::

   python ./setup.py install

Otherwise you may install directly using setuptools/easy_install. If
your system has network access installing `openvas.omplib` is a
breeze::

     easy_install openvas.omplib

Without network access download `openvas.omplib` from
http://pypi.python.org/pypi/openvas.omplib and run::

     easy_install openvas.omplib-*.tar.gz


More Hints on Installing setuptools
------------------------------------

`openvas.omplib` uses setuptools for installation. Thus you need
either

  * network access, so the install script will automatically download
    and install setuptools if they are not already installed

or

  * the correct version of setuptools preinstalled using the
    `EasyInstall installation instructions`__. Those instructions also
    have tips for dealing with firewalls as well as how to manually
    download and install setuptools.

__ http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions


Custom Installation Locations
------------------------------

`openvas.omplib` is just a single script (aka Python program). So you can
copy it where ever you want (maybe fixing the first line). But it's
easier to just use::

   # install to /usr/local/bin
   python ./setup.py install --prefix /usr/local

   # install to your Home directory (~/bin)
   python ./setup.py install --home ~


Please mind: This effects also the installation of pfPDf (and
setuptools) if they are not already installed.

For more information about Custom Installation Locations please refer
to the `Custom Installation Locations Instructions`__ before
installing `openvas.omplib`.

__ http://peak.telecommunity.com/DevCenter/EasyInstall#custom-installation-locations>
