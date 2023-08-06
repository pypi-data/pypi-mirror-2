hurry.datalink
**************

Introduction
============

This library packages the jQuery `datalink plugin`_ for
`hurry.resource`_. 

.. _`hurry.resource`: http://pypi.python.org/pypi/hurry.resource
.. _`datalink plugin`: https://github.com/jquery/jquery-datalink

How to use?
===========

You can import ``datalink`` from ``hurry.datalink`` and ``.need`` it
where you want these resources to be included on a page::

  from hurry.datalink import datalink

  .. in your page or widget rendering code, somewhere ..
  
  datalink.need()

This requires integration between your web framework and
``hurry.resource``, and making sure that the original resources
(indicated by the setup.py entry point) are published to some URL.
