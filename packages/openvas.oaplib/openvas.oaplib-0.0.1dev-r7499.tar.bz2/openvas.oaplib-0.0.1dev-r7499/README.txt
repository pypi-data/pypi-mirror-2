.. -*- mode: rst -*-

==========================
`openvas.oaplib`
==========================

------------------------------------------------------------------
An OAP (OpenVAS Administration Protocol) client interface for Python.
------------------------------------------------------------------

:Author:  Hartmut Goebel <h.goebel@goebel-consult.de>
:Version: Version 0.0.1
:Copyright: GNU Public Licence v3 (GPLv3)
:Homepage: http://www.openvas.org/

`OpenVAS`__ (Open Vulnerability Assessment System) is a network
security scanner with associated tools. OpenVAS Version 3 introduces a
new core component: The OpenVAS-Administrator. It is intended to
simplify the configuration and administration of an OpenVAS server
both on a local installation as well as on a remote system.

__ http://www.openvas.org

OpenVAS Administration Protocol (OAP) is the protocol based on XML to
talk to the OpenVAS-Administrator. `openvas.oaplib` is a pure-Python
implementation of OAP which allows easy access to the
OpenVAS-Administrator.

Example::

    admin = openvas.oaplib.OAPClient(host=sensor)
    admin.open(username, password)
    admin.create_target(job_name, targets, comment)
    task_id = admin.create_task(job_name, comment, config=config_name,
                                  target=job_name)
    report_id = admin.start_task(task_id)
    # ... later ...
    report = admin.get_report(report_id)
    print etree.tostring(report)

`openvas.opmlib` also supports a low-level interface where you can send
OAP XML directly::

    help_text = admin.xml('<help/>')

.. 
  For more information please refer to the manpage or visit
  the `project homepage <http://pdfposter.origo.ethz.ch/>`_.


Requirements and Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`openvas.oaplib` requires

* `Python 2.5`__ or higher (Python 3.x is *not* supported)
* `setuptools`__ for installation (see below).
* `argparse`__ (already included in Python starting with Python 2.7)
* `pyOpenSSL`__ or `egenix-pyopenssl`__

__ http://www.python.org/download/
__ http://pypi.python.org/pypi/setuptools
__ http://pypi.python.org/pypi/argparse
__ http://pypi.python.org/pypi/pyOpenSSL
__ http://pypi.python.org/pypi/egenix-pyopenssl


:Hints for installing on Windows: Following the links above you will
   find .msi and .exe-installers. Simply install them and continue
   with `installing openvas.oaplib`_.

:Hints for installing on Linux: Most current Linux distributions
   provide packages for the requirements. Look for packages names like
   `python-setuptools`, `python-argparse` and `python-openssl`. Simply
   install them and continue with `installing openvas.oaplib`_.

:Hint for installing on other platforms: Many vendors provide Python.
   Please check your vendors software repository. Otherwise please
   download Python from http://www.python.org/download/ and follow the
   installation instructions there.

   After installing Python, install `setuptools`__. You may want to
   read `More Hints on Installing setuptools`_ first.

__ http://pypi.python.org/pypi/setuptools

   Using setuptools, compiling and installing the remaining
   requirements is a piece of cake::

     # if the system has network access
     easy_install argparse pyOpenSSL

     # without network access download pyOpenSSL 
     # from http://pypi.python.org/pypi/pyOpenSSL and run
     easy_install argparse-*.zip pyOpenSSL-*.tar.gz


Installing openvas.oaplib
---------------------------------

When you are reading this you most probably already downloaded and
unpacked `openvas.oaplib`. Thus installing is as easy as running::

   python ./setup.py install

Otherwise you may install directly using setuptools/easy_install. If
your system has network access installing `openvas.oaplib` is a
breeze::

     easy_install openvas.oaplib

Without network access download `openvas.oaplib` from
http://pypi.python.org/pypi/openvas.oaplib and run::

     easy_install openvas.oaplib-*.tar.gz


More Hints on Installing setuptools
------------------------------------

`openvas.oaplib` uses setuptools for installation. Thus you need
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

`openvas.oaplib` is just a single script (aka Python program). So you can
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
installing `openvas.oaplib`.

__ http://peak.telecommunity.com/DevCenter/EasyInstall#custom-installation-locations>
