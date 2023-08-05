Introduction
============

Acquisition is evil.

If you have a Zope tree like that::

     |
     \-- Site1
     |
     \-- Site2

You will be able to traverse Site2 from Site1 just by traversing::

    http://yoursite/Site1/Site2

This package avoid this behavior by adding verification during traversal.

  * Documentation: http://docs.affinitic.be/collective.siteisolation
  * Code Repository: https://svn.plone.org/svn/collective/collective.siteisolation
  * Buildbot: http://buildbot.affinitic.be/builders/collective.siteisolation%20linux_debian/
  * Test Coverage: http://coverage.affinitic.be/collective.siteisolation/collective.siteisolation.html

Author
======

 * ICTS Team - KULeuven (https://admin.kuleuven.be/icts)
 * Jean-Francois Roche <jfroche at affinitic dot be>
