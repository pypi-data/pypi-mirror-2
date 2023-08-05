hurry.jqueryform
****************

Introduction
============

This library packages the jQuery `Form Plugin`_ for
`hurry.resource`_.

.. _`hurry.resource`: http://pypi.python.org/pypi/hurry.resource
.. _`Form plugin`: http://jquery.malsup.com/form/


How to use?
===========

You can import ``jqueryform`` from ``hurry.jqueryform`` and
``.need`` it where you want these resources to be included on a page::

  from hurry.jqueryform import jqueryform

  .. in your page or widget rendering code, somewhere ..

  jqueryform.need()

This requires integration between your web framework and
``hurry.resource``, and making sure that the original resources
(shipped in the ``jqueryform-build`` directory in
``hurry.jqueryform``) are published to some URL.

The package has already been integrated for Grok_ and the Zope
Toolkit. If you depend on the `hurry.zoperesource`_ package in your
``setup.py``, the above example should work out of the box. Make sure
to depend on the `hurry.zoperesource`_ package in your ``setup.py``.

.. _`hurry.zoperesource`: http://pypi.python.org/pypi/hurry.zoperesource

.. _Grok: http://grok.zope.org
