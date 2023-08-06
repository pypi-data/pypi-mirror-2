hurry.datatables
****************

Introduction
============

This library packages the `DataTables`_ jquery extension for
`hurry.resource`_. It is aware of jQuery datatables' different modes
(normal, minified).

.. _`hurry.resource`: http://pypi.python.org/pypi/hurry.resource
.. _`DataTables`: http://www.datatables.net

How to use?
===========

You can import ``datatables`` from ``hurry.datatables`` and
``.need`` it where you want these resources to be included on a page::

  from hurry.datatables import datatables

  .. in your page or widget rendering code, somewhere ..

  datatables.need()

This requires integration between your web framework and
``hurry.resource``, and making sure that the original resources
(shipped in the ``datatables-build`` directory in
``hurry.datatables``) are published to some URL. The
``hurry.datatables.datatables_lib`` library, exposed as an entry point
to ``hurry.resource``, knows where the data is in its ``path``
argument.

The package has already been integrated for Grok_ and the Zope
Toolkit. If you depend on the `hurry.zoperesource`_ package in your
``setup.py``, the above example should work out of the box. Make sure
to depend on the `hurry.zoperesource`_ package in your ``setup.py``.

.. _`hurry.zoperesource`: http://pypi.python.org/pypi/hurry.zoperesource

.. _Grok: http://grok.zope.org
