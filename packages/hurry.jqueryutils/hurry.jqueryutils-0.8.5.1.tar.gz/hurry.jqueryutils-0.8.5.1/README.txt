hurry.jqueryutils
*****************

How to use?
===========

You can import hurry.jqueryutils from ``hurry.jqueryutils`` and ``.need`` it
where you want these resources to be included on a page::

  from hurry.jqueryutils import jqueryutils

  .. in your page or widget rendering code, somewhere ..

  jqueryutils.need()

This requires integration between your web framework and
``hurry.resource``, and making sure that the original resources
(shipped in the ``jqueryutils-build`` directory in ``hurry.jqueryutils``)
are published to some URL.

The package has already been integrated for Grok_ and the Zope
Toolkit. If you depend on the `hurry.zoperesource`_ package in your
``setup.py``, the above example should work out of the box. Make sure
to depend on the `hurry.zoperesource`_ package in your ``setup.py``.

.. _`hurry.zoperesource`: http://pypi.python.org/pypi/hurry.zoperesource

.. _Grok: http://grok.zope.org
