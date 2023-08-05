hurry.jquerylayout
******************

Introduction
============

This library packages the jQuery `UI.Layout plugin`_ for
`hurry.resource`_. It is aware of jQuery UI Layout's structure and
different modes (normal, minified).

.. _`hurry.resource`: http://pypi.python.org/pypi/hurry.resource
.. _`UI.Layout plugin`: http://layout.jquery-dev.net

How to use?
===========

You can import ``jquerylayout`` from ``hurry.jquerylayout`` and
``.need`` it where you want these resources to be included on a page::

  from hurry.jquerylayout import jquerylayout

  .. in your page or widget rendering code, somewhere ..

  jquerylayout.need()

This requires integration between your web framework and
``hurry.resource``, and making sure that the original resources
(shipped in the ``jquerylayout-build`` directory in ``hurry.jquerylayout``)
are published to some URL.

The package has already been integrated for Grok_ and the Zope
Toolkit. If you depend on the `hurry.zoperesource`_ package in your
``setup.py``, the above example should work out of the box. Make sure
to depend on the `hurry.zoperesource`_ package in your ``setup.py``.

.. _`hurry.zoperesource`: http://pypi.python.org/pypi/hurry.zoperesource

.. _Grok: http://grok.zope.org
