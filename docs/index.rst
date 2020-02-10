TOROS Manager's Documentation
=============================

The TOROS Manager is a collection of installable daemons (services) to automize telescope 
operations.

The communication between modules is done using the `XML-RPC`_ protocol over sockets.
This allows the modules to be distributed on different machines, as well as a single computer.

Contents:
^^^^^^^^^
.. toctree::
   :maxdepth: 2

   installation
   configuration
   services
   workorders

.. _XML-RPC: http://xmlrpc.scripting.com
