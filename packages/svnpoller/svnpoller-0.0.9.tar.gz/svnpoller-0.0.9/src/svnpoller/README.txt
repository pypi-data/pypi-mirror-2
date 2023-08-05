`svnpoller` watches target SVN repositories regularly and transmits a
commit-mail to the designated notify party about each commit when there
are new commits.

Setting sample
--------------

svnpoller.ini::

   [mail]
   smtpserver = localhost
   fromaddr = admin@example.com

   [sample-section]
   url = http://svn.example.org/path/to/repos/with/sub/path
   address = test1@example.com, test2@example.com


Notify mail sample
-------------------

Notified mail sample::

   From: admin@example.com
   To: test1@example.com, test2@example.com
   Subject: [sample-section: 1230]

   * Revision: 1230
   * Author: foo
   * Date: 2009-11-22T17:40:47.287888Z
   * Message:
   The commit log message for this revision here.

   * Paths:
   M /with/sub/path/somefile1.py
   A /with/sub/path/somefile2.py

   * Diff:
   Index: somefile1.py
   ===================================================================
   --- somefile1.py     (revision 1230)
   +++ somefile1.py     (revision 1229)


Requirements
------------

* Python 2.4 or later (not support 3.x)


Dependencies
------------

* `setuptools <http://pypi.python.org/pypi/setuptools>`_ or
  `distribute <http://pypi.python.org/pypi/distribute>`_

* svn external command (1.4 or later)

* `lxml` (optional)


Features
--------

* polling specified svn repository

* send commit message and diff by email


Setup
-----

Make environment (by easy_install)::

   $ easy_install svnpoller


Make environment (by buildout)::

   $ hg clone http://bitbucket.org/shimizukawa/svnpoller
   $ cd svnpoller
   $ python bootstrap.py
   $ bin/buildout


Copy and modify ini file. example::

   $ cp <svnpoller installed path>/svnpoller/svnpoller.ini .
   $ vi svnpoller.ini

Please refer to `Setting sample`_ section for the format of the
`svnpoller.ini` configuration file.

Usage
-----

Execute svnpoller command::

   $ svnpoller svnpoller.ini

or setup cron job::

   $ crontab -e
   0 0 * * * /path/to/svnpoller /path/to/svnpoller.ini


History
-------

0.0.9 (2010-6-23)
~~~~~~~~~~~~~~~~~~
* Fix: commit message include multi-byte charactor cause exception.
* Remove: `lxml` dependency, become optional
  (thanks to 'Federico' for the patch!).
* Fix: Exception caused by error status return from svn command
  when repository was not updated since last check
  (thanks to 'Federico' for the patch!).
* Add: copy-only or delete-only or move-only diff are not attached
  (thanks to 'Federico' for the patch!).

0.0.8 (2010-6-20)
~~~~~~~~~~~~~~~~~~
* Fix: Notify mail send only first address when multiple address
  (comma separated) was specified on ini file.

0.0.7 (2010-6-18)
~~~~~~~~~~~~~~~~~~
* Fix: datetime.strptime replaced with time.strptime (for Python-2.4)
* Remove: `lxml` dependency. (if python-2.5 or later)
* Change: supported svn external command version: 1.4 or later

0.0.6 (2010-6-18)
~~~~~~~~~~~~~~~~~~
* Fix: latest revision's change ware notified every time.
* Add: some tests.

0.0.5 (2010-5-20)
~~~~~~~~~~~~~~~~~~
* Add changed `path-list` to mail-message.

0.0.4 (2010-5-20)
~~~~~~~~~~~~~~~~~~
* first release

