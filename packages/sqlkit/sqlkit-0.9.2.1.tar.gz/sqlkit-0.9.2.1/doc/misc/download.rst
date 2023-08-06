=======================================
 Download, requirements & googlegroup
=======================================
  

Requirements
============

Sqlkit depends on:

       * Python
       * Pygtk
       * sqlalchemy (>=0.5.3). Rel 0.9.0 is the first sqlkit release
         that works with sqlalchemy 0.6+
       * glade2
       * python-dateutils 
       * setuptools
       * the correct driver for your database of choice among the backend
         `supported by sqlalchemy`_
       * babel (localization)

Changelog
===========

this is the Changelog_

.. _Changelog: http://sqlkit.argolinux.org/download/Changelog

Download
========
The code is available under an hg repository::

  hg clone http://hg.argolinux.org/py/sqlkit
  
You can download sqlkit package VER from here_ in tar or zip format. 

+--------------------------------------+-------------------------------------+
| Python package                       |* sqlkit-VER.tar.gz_                 |
|                                      |* sqlkit-VER.zip_                    |
+--------------------------------------+-------------------------------------+
| Debian/Ubuntu package (read below!   |python-sqlkit_DEBVER_all.deb_        |
| you are supposed to install          |                                     |
| sqlalchemy >= 0.5.3 and babel)       |                                     |
+--------------------------------------+-------------------------------------+
| Linux executable (pyinstaller)       |sqledit-binary-LNXVER.tar.gz_        |
+--------------------------------------+-------------------------------------+
| Windows executable (pyinstaller)     |sqledit-setup-WINVER.exe_            |
+--------------------------------------+-------------------------------------+


Sqlkit is used in a production environment and great care is put in fixing
any bug as soon as possible. The first stable version has been 0.8.6 in 2008. 

I really appreciate any bug report particularly if based on a repeatable
example, possibly starting from the demo.

Binary bundles
===============

Since sqlkit depends on several different packages we also provide a bundle
with an installer that you can use to run the demo and the command sqledit
for sqlite, mysql and postgresql databases. 

It does not have any dependencies.

You cannot use it to build other executables. If all you want to do is using
the command sqledit, that's a good choice (probably a little slower to open).

Debian/Ubuntu
=============

If you want a bleeding edge sqlkit version you'd better install from the
package distribution. On a Debian lenny or Ubuntu >= 9.04 you can prepare
dependencies::

  sudo apt-get install python-setuptools python-pybabel python-dateutil python-psycopg2 python-sqlalchemy python-mysqldb python-pip
  sudo pip install sqlkit

You can also add the source::

  deb http://apt.argolinux.org/ lenny sqlkit

by issuing the following command::

  wget http://apt.argolinux.org/sqlkit.list --output-document=/etc/apt/sources.list.d/sqlkit.list
  wget -O-  http://apt.argolinux.org/dists/lenny/public.key| sudo apt-key add -
  sudo apt-get update

and install it via::

  apt-get install python-sqlkit

Even if the source states ``lenny`` it can safely be used for Ubuntu.

.. note:: Sqlalchemy
    
    sqlkit depends on sqlalchemy >= 0.5 that is only packaged for Ubuntu >=
    9.10 so the .deb does not require it. You can install it

.. note:: Babel

   sqlkit depends on babel that is not packaged in Debian but is packaged in
   Ubuntu with two different names in hardy and jaunty and is missing in
   intrepid. So the package I have prepared does not depend on it. You are
   supposed to add the package. If using hardy install ``python-babel`` if
   using jaunty or following, use ``python-pybabel`` instead. If using
   intrepid... I'm almost sure there was a pybabel, but there is no
   more... install by hand!::

      easy_install babel

This way you'll also install backend drivers for postgresql, mysql and clearly sqlite.

Other platforms
===============

Sqlkit is now available via Pypi, so -if you have already installed
setuptools that provides the command easy_install- you can install it via
``easy_install`` or better ``pip``::

  easy_install pip
  pip install sqlkit

You can also install directly with easy_install that often will fail
understanding already installed packages. Should you have problems with pip
you can revert to::

  easy_install sqlkit


No one of these command will install the backend driver (psycopg2 for
postgresql, MySQLdb for mysql -MySQL-python,...) that you are supposed to
install by yourself. Sqlite is included in any 


Mailing list
============

You can join our mailing list_

Localization
============

We need the help from some translator to localize in different languages. It
takes some 20 minutes to provide a complete set of translations for each
language. Please visit the launchpad_ 's site or contact me directly.

Author
======

Sqlkit is developed by `Alessandro Dentella`_


.. _list: http://groups.google.com/group/sqlkit
.. _here: http://sqlkit.argolinux.org/download/
.. _Experimental: http://packages.debian.org/experimental/python-sqlalchemy
  
.. _sqlkit-VER.tar.gz: http://sqlkit.argolinux.org/download/sqlkit-VER.tar.gz
.. _sqlkit-VER.zip: http://sqlkit.argolinux.org/download/sqlkit-VER.zip
.. _python-sqlkit_DEBVER_all.deb: http://sqlkit.argolinux.org/download/python-sqlkit_DEBVER_all.deb
.. _sqledit-binary-LNXVER.tar.gz: http://sqlkit.argolinux.org/download/sqledit-binary-LNXVER.tar.gz
.. _sqledit-setup-WINVER.exe: http://sqlkit.argolinux.org/download/sqledit-setup-WINVER.exe
.. _sqlkit-doc_VER_all.deb: http://sqlkit.argolinux.org/download/sqlkiy-doc_VER_all.deb
.. _`Alessandro Dentella`: mailto:sandro@e-den.it
.. _launchpad: https://launchpad.net/sqlkit
.. _`supported by sqlalchemy`: http://www.sqlalchemy.org/trac/wiki/DatabaseNotes
