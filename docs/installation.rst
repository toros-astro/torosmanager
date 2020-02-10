Installing TOROS Manager
========================

Requirements
------------

To install this software you need 

* Python >=3.6 installed, preferably in a virtual environment or a local installation.
* Linux or MacOS operating system.
* Root or sudo access.

Installation
------------

To install, clone the TOROS Manager repo and run the makefile.
Preferably use a virtual environment::

    $ git clone https://github.com/toros-astro/torosmanager.git
    $ cd torosmanager
    $ mkvirtualenv -p python3 toros
    (ctmo)$ make
    (ctmo)$ sudo make install

Installation requires root privilege.
Root is only used to install the systemd or launchd services.

Depending on your operating system,
this will install system services (currently only ``preprocessor``) under
``/etc/systemd/system`` (the default path to install services in Linux)
or ``/Library/LaunchAgents`` (the default path to install services in MacOS);
and a configuration file under ``/etc/toros``

Uninstall
---------

To clean (delete intermediate files) and uninstall::

    $ make clean
    $ sudo -H make uninstall
