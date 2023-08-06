Introduction
============

This egg sets up a fully configured and running Babble instant messaging
environment for Plone.

It's intended as a demo and aid to help integrators familiarise themselves with
how Babble works and what it has to offer.

Please don't include this egg in any existing buildouts! It has its own
buildout config file, *plone4.cfg*, with which you are required to create a new
Zeo/Plone instance. See the `documentation 
<http://opkode.net/babbledocs/babble.demo/index.html>`_ for more detailed instructions
for setting up babble.demo.


All the eggs (currently) related to Babble are installed. These are:

- `babble.server <http://plone.org/products/babble.server>`_: 
   - The Zope messaging service. This service should ideally be run in it's
     own dedicated server or Zeo client (as in this case).
- `babble.client <http://plone.org/products/babble.client>`_: 
   - The Plone client side program. This provides the main chat functionality 
     such as the *online contacts* portlet and the chat boxes.
- `actionbar.panel <http://plone.org/products/actionbar.panel>`_:
   - This add-on is not directly associated with Babble and is not a
     requirement of it. It provides an extendablee action panel that hovers at 
     the bottom of the screen.
- `actionbar.babble <http://plone.org/products/actionbar.babble>`_:
   - The Babble extention for actionbar.panel. It provides a special
     action-box that provides a list of currently online users. Additionally,
     chatboxes are docked on this panel.


Additional info:
----------------

For information on how to set up the demo, 
please read the documentation at 
http://opkode.net/babbledocs/babble.demo/index.html


