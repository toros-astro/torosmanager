.. _conf:

Configuring your system
=======================

Before you start the services you may have to configure your manager
to work with your system.


Configuration file
------------------

Open the configuration file located in ``/etc/toros/toros.conf.yaml``.
Inside you will find a `YAML`_ configuration file for the services.

Preprocessor Address
^^^^^^^^^^^^^^^^^^^^
**HTTP:** The full address and port to locate the ``preprocessor`` service on the net.

**IP:** The IP address of the server running the ``preprocessor`` service.

**Port:** The port for the address of the server running the ``preprocessor`` service.


Logging
^^^^^^^

**File:** File path to the log file that will be used to log.
Default is ``/etc/toros/logs/toros.log``.

**Log Level:** One of ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``. Default: ``INFO``.

Database
^^^^^^^^

Specify database connection parameters (TBD).

.. _YAML: https://yaml.org
