.. warning::

  Work orders may not be used in the future. It is left here just in case.

.. _wo:

Work Orders
===========

The basic structure of a work order is as follows:

.. code-block:: python

    work_order = {
        "ID": "1",
        "WOType": "Observation",
        "Priority": None,
        "Datetime": "2019-03-05T14:34:54.234",
        "User": "Main Module",
        ...
    }

``WOType`` should be one of the following: ``Observation``.
``Priority`` is assigned by the ``scheduler`` module when receiving the WO.
It will be a float number in the range 0-10.

Telescope WO Format
-------------------

Work Orders sent to a telescope must contain
the ``WOType`` keyword set to the string ``Observation``
as well as other keywords relevant to an observation.

Below is an example.

.. code-block:: python

    {
        "ID": "1",
        "WOType": "Observation",
        "Priority": 1.3,
        "Datetime": "2019-03-05T14:34:54.234",
        "User": "Main Module",
        "Telescope Name": "CTMO",
        "RA": 23.1,
        "Dec": 13.2,
        "Filter": "I",
        "Exposure Time": 30.0,
        "Number of Exposures": 1,
        "Type of job": "Research",
        "Type of object": "Galaxy",
        "Calibration Frames": "Yes",
        "Output": "Analysis",
    }

Dome WO Format
--------------

.. code-block:: python

    {
        "ID": "1",
        "WOType": "Dome",
        "Priority": 2,
        "Datetime": "2019-03-05T14:34:54.234",
        "User": "John Doe",
        "Blink01": True,
    }
