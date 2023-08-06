Introduction
============
Torii allows access to a running zope server over a unix-domain-socket. Torii makes it
also possible to run scripts from the command line on the server. In addition it provides 
a python-prompt. That means full access to the Zope and ZODB at runtime.


The simplest way to install torii is to use raptus.recipe.torii in the buildout for your project.
This will add the required information in the zope.conf and build a startup script. The recipe provides
two buildout-variables. The first is named ${torii:additonal-conf} and holds the additional information
for the zope.conf. The second variable ${torii:eggs} is a list of all required eggs to add to the
python-path. Like this torii can also be used for non-plone projects.

`more information at raptus.torii <http://pypi.python.org/pypi/raptus.torii>`_

Copyright and credits
=====================

raptus.torii is copyright 2010 by raptus_ , and is licensed under the GPL. 
See LICENSE.txt for details.

.. _raptus: http://www.raptus.com/ 


