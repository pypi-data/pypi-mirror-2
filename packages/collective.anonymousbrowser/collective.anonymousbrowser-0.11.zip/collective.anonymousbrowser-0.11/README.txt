Introduction
=============
This Yet-Another-Mechanize implementation aims to give the developper those new
features:

 - It can be proxified
 - It does proxy balancing
 - It fakes user agent ``by default``
 - It does not handle robots ``by default``
 - There is a 'real" modification which uses an underlying moz repl server to
   control a distance firefox instance

It uses sys.prefix/etc/config.ini with a part [collective.anonymousbrowser] for its settings::

     [collective.anonymousbrowser]
     proxies=
     ; for a mozrepl server
     host = localhost
     port = 4242
     firefox = /path/To/Firefox
     ff-profile = /path/to/FFprofile

This file is generated at the first run without proxies. It s your own to feed it with some open proxies.

Of course, it can take another configuration file, please see the __init__ method.

Makina Corpus sponsorised software
======================================
|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com



TODO
=====
- lxml integration, maybe steal z3c.etestbrowser

