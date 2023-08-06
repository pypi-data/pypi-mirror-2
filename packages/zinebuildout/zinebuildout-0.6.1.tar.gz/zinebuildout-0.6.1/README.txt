Installation
============

This package allows you to install Zine and its dependencies in a sandbox with
buildout, then serve it with any WSGI server while using the Paste facilities
for WSGI stack configuration.

Install Zine:
-------------

Download and extract the zinebuildout archive from PyPI,
(or clone it with: hg clone https://cody.gorfou.fr/hg/zinebuildout ).
You don't need to easy_install it.
Then run: ::

  $ python bootstrap.py
  $ ./bin/buildout

Configure Zine:
---------------

Edit "deploy.ini" to adapt ``instance_folder``, ``host`` and ``port`` to
your needs. You don't need to change anything if you just want to try it on
your local host.

Start Zine:
-----------

In foreground: ::

  $ ./bin/paster serve deploy.ini

Or in background: ::

  $ ./bin/paster serve --daemon deploy.ini

Your admin interface will then be accessible through
http://localhost:8080/admin/

Then you can put this process behind a reverse proxy (with Apache ProxyPass or
RewriteRule) or any other. Example of an Apache VirtualHost::

  <virtualHost *>
  (...)
  RewriteEngine on
  RewriteRule ^/(.*) http://localhost:8080/$1 [proxy,last]
  </virtualHost>

Optional Twitter widget
-----------------------

This distribution offers a Twitter widget that displays the N latests tweets of
your timeline. To use it, just add the following line in the '_widgets.html'
file of your Zine theme::

    {{ widgets.tweets('ccomb', 5) }}

Replace 'ccomb' with your twitter account, and 5 with the number of tweets you
want to display.

Versions
========
0.6.1 (2010-12-28)
------------------
- upgraded minor versions
- added a missing tweets.html template 

0.6 (2010-11-01)
----------------
- upgraded to buildout 1.5
- upgraded all minor versions using z3c.checkversions

0.5 (2009-07-19)
----------------
- fixed some egg versions
- added a twitter widget to display the latest tweets

0.4 (2009-02-19)
----------------
- remove the zine section from Paste config. (thx Calvin)
  It will allow defining several zine instances in the same config file.

0.3  (2009-01-29)
-----------------
- fixed the bad 0.2 release

0.2  (2009-01-27)
-----------------
- move to zine 0.1.2
- no more need to configure the instance folder
- Added pygments and docutils (for the rst parser)

0.1  (2009-01-14)
-----------------

initial buildout for Zine 0.1.1
