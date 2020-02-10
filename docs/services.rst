System Services
===============

Starting the services
---------------------

Once the system is properly configured (see :ref:`conf`), you can start, stop or restart any of the services.

The operations to do so are different in Linux and MacOS.
Both require root or sudo privilege.

Linux
^^^^^

On Linux, to start the preprocessor service you would run::

    $ systemctl start preprocessor

and similarly for other modules.
Now the system is ready to receive work orders through the network.

For more information, visit `systemd wikipedia page <https://en.wikipedia.org/wiki/Systemd>`_
or `the official documentation <https://freedesktop.org/wiki/Software/systemd/>`_.

MacOS
^^^^^

On MacOs, to start the scheduler service you would run::

    $ launchctl load /Library/LaunchAgents/org.toros.preprocessor.plist

and similarly for other modules.
To stop, use the ``unload`` command.

For more information, see `launchd's page <https://www.launchd.info>`_ 
or `Apple's official documentation`_.

Services
--------

**Preprocessor**: Preprocess CCD exposures.

More will be added in the future.

XML-RPC Interface
-----------------

Each service will run as a daemon (background process)
and work on a specific port specified in the configuration file
using the `XML-RPC`_ protocol.

Each service responds to a single function called ``front_desk`` which accepts a "Work Order".

Work Orders (WO) are dictionaries with a specific structure described in :ref:`wo`.

.. _XML-RPC: http://xmlrpc.scripting.com
.. _Apple's official documentation: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
