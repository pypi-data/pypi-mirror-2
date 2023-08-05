buildout.threatlevel
====================

.. image:: http://www.dhs.gov/graphics/ready_hp167.jpg
   :align: right
   :height: 90px

..

 All ... should continue to be vigilant, take notice of their
 surroundings, and report suspicious items or activities to local authorities
 immediately.

 -- the U.S. Department of Homeland Security

``buildout.threatlevel`` is a buildout extension which will report on the
success of your buildout to the global `Buildout Threat Level`_ indicator.

.. _`Buildout Threat Level`: http://buildthreat.appspot.com

It will also report the current threat level, based on the percentage of
buildout runs that have succeeded for all users of buildout.threatlevel over
the past 4 hours.

Usage::

 [buildout]
 extensions = buildout.threatlevel
