Introduction
============
Torii allows access to a running zope server over a unix-domain-socket. Torii makes it
also possible to run scripts from the command line on the server. In addition it provides 
a python-prompt. That means full access to the Zope and ZODB at runtime.

This additional package offers the interface to plone. It provides some scripts,
a global variable 'plone' and sets the siteManager(access to persistence zope.components )
at startup time.


Use it with buildout::

    [torii]
    recipe = raptus.recipe.torii
    socket-path = ${buildout:directory}/var/torii.sock
    threaded = True
    extends =
        raptus.torii.plone


`more information at raptus.torii <http://pypi.python.org/pypi/raptus.torii>`_

Copyright and credits
=====================

raptus.torii is copyright 2010 by raptus_ , and is licensed under the GPL. 
See LICENSE.txt for details.

.. _raptus: http://www.raptus.com/ 


