`klimalogger <https://github.com/wuan/klimalogger>`_
====================================================

.. image:: https://badge.fury.io/py/klimalogger.svg
    :alt: PyPi-Package
    :target: https://badge.fury.io/py/klimalogger
.. image:: https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=ncloc
    :alt: Lines of code
    :target: https://sonarcloud.io/project/overview?id=wuan_klimalogger
.. image:: https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=coverage
    :alt: Coverage
    :target: https://sonarcloud.io/project/overview?id=wuan_klimalogger
.. image:: https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=duplicated_lines_density
    :alt: Duplicated lines
    :target: https://sonarcloud.io/project/overview?id=wuan_klimalogger
.. image:: https://api.scorecard.dev/projects/github.com/wuan/bo-android/badge
    :alt: OpenSSF Scorecard
    :target: https://scorecard.dev/viewer/?uri=github.com/wuan/bo-android

Simple python client for logging measured climate data to InfluxDb.

Additional dependencies
-----------------------

.. list-table:: Dependencies
   :widths: 20 90
   :header-rows: 1

   * - Sensor Type
     - Command
   * - BME680
     - ``pip3 install adafruit-circuitpython-bme680``
   * - BMP3xx
     - ``pip3 install adafruit-circuitpython-bmp3xx``
   * - SGP30
     - ``pip3 install adafruit-circuitpython-sgp30``
   * - SGP40
     - ``pip3 install adafruit-circuitpython-sgp40``
   * - SHT4x
     - ``pip3 install adafruit-circuitpython-sht4x``

Build and upload
----------------

.. code-block:: sh

   python3 -m build
   python3 -m pip install --upgrade twine
   python3 -m twine upload dist/klimalogger-0.6.8.tar.gz

Install on server
-----------------

Software
........

It is recommended to use a virtual environment.

.. code-block:: sh

   virtualenv /usr/local/share/klimalogger
   . /usr/local/share/klimalogger/bin/activate
   pip install klimalogger

Then install hardware specific drivers e. g.

.. code-block:: sh

   pip3 install adafruit-circuitpython-sht4x

Then setup the configuration file ``/etc/klimalogger.conf``.

The sensor readout can be validated through

.. code-block:: sh

   /usr/local/share/klimalogger/bin/klimalogger --check

The result should be JSON formatted measurement data.

In order to run the service for debugging use the following command line

.. code-block:: sh

   /usr/local/share/klimalogger/bin/klimalogger --service --debug

Setup Service
.............

Create a service configuration, for example ``/etc/systemd/system/klimalogger.service`` with the following content:

.. code-block::

   [Unit]
   Description=Klimalogger Service
   After=multi-user.target

   [Service]
   Type=simple
   Restart=always
   ExecStart=/usr/local/share/klimalogger/bin/klimalogger --service

   [Install]
   WantedBy=multi-user.target

and run

.. code-block:: sh

   systemctl daemon-reload
   systemctl enable klimalogger
   service klimalogger start

to run the service.

Pre-commit hooks
----------------

This repository includes a pre-commit configuration to automatically run formatting, linting and type checks on each commit.

Setup locally:

.. code-block:: sh

   pip install pre-commit
   pre-commit install

You can also run all hooks against the full repo:

.. code-block:: sh

   pre-commit run --all-files

The configured tools include:

- black and isort for formatting
- ruff for linting (auto-fixes enabled)
- mypy for type checking (configured in mypy.ini)
