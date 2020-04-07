[![Build Status](https://travis-ci.org/toros-astro/torosmanager.svg?branch=master)](https://travis-ci.org/toros-astro/torosmanager)

***

# TOROS Manager :telescope:

## Installation

To install, clone this repo and run the makefile.
Preferably use a virtual environment.

**NOTE:** Before installing, make sure that `DEBUG` in `config.py` is set to `False` while in production mode.

    $ git clone https://github.com/toros-astro/torosmanager.git
    $ cd torosmanager
    $ mkvirtualenv -p python3 torosmanager
    $ make
    $ sudo make install

Installation requires root privilege.

## Start any service with systemctl

Once the system is properly configured, you can start, stop or restart any of the services.

### In Linux OS:

    $ systemctl [action] [service]

Where `action` is one of: `start`, `stop` or `restart`
and service could be `preprocessor`.

### In MacOS:

    $ launchctl load /Library/LaunchAgents/org.toros.preprocessor

To stop use `unload` instead.

## To clean and uninstall:

    $ make clean
    $ sudo -H make uninstall

## Test

You can test the availability of the service on a web browser at `http://localhost:8000` (or the address of the preprocessor service in the configuration file).

Furthermore, you can test the service is receiving work orders with the script in `tests/send_work_order.py`:

    $ sudo /path/to/virtualenv/bin/python tests/send_work_order.py

You should see "Work order received." printed on the screen.

***

(c) 2020 - TOROS Dev Team
