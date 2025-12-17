=========================
bluetooth-mesh-messages
=========================

.. image:: https://img.shields.io/pypi/v/bluetooth-mesh-messages.svg
   :target: https://pypi.org/project/bluetooth-mesh-messages
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/bluetooth-mesh-messages.svg
   :target: https://pypi.org/project/bluetooth-mesh-messages
   :alt: Python versions

----

Bluetooth mesh messages library for Python provides parsing and building
of Bluetooth Mesh access layer messages as defined in Bluetooth SIG specifications.

What is this thing?
--------------------

This library implements message serialization and deserialization for Bluetooth Mesh
protocol, supporting both standard SIG models and Silvair vendor-specific extensions.

https://www.bluetooth.com/specifications/mesh-specifications

Supported models include:

- **Generic models**: OnOff, Level, Battery, Property
- **Lighting models**: Lightness, CTL
- **Scene model**
- **Sensor model**
- **Time model**
- **Health model**
- **Config model**
- **Silvair vendor models**: Debug, Emergency Lighting, Gateway Config,
  Light Extended Controller, Network Diagnostic, RRule Scheduler

Installation
------------

You can install "bluetooth-mesh-messages" via `pip`_ from `PyPI`_::

    $ pip install bluetooth-mesh-messages

Contributing
------------

Contributions are very welcome. Tests can be run with `pytest`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `GPL-2.0`_ license, "bluetooth-mesh-messages" is
free and open source software.

Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`GPL-2.0`: http://opensource.org/licenses/GPL-2.0
.. _`file an issue`: https://github.com/SilvairGit/python-bluetooth-mesh-messages/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
