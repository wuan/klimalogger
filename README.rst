***************************************************
`klimalogger <https://github.com/wuan/klimalogger>`
***************************************************

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
.. image:: https://api.scorecard.dev/projects/github.com/wuan/klimalogger/badge
    :alt: OpenSSF Scorecard
    :target: https://scorecard.dev/viewer/?uri=github.com/wuan/klimalogger

Simple python client for logging measured climate data to MQTT targets.

Sensor support
==============

As of now the following sensors are supported

.. list-table:: Supported Sensors
   :widths: 40 60
   :header-rows: 1

   * - Sensor Type
     - Measurement
   * - BME680
     - Barometric pressure, Temperature, Relative humidity, Air quality
   * - BMP3xx
     - Temperature, Barometric Pressure
   * - SGP30
     - Air quality
   * - SGP40
     - Air quality
   * - SHT4x
     - Temperature, Relative Humidity
   * - SCD4x
     - CO2 concentration
   * - PM25
     - particle concentration
   * - BH1750, VEML7700, TSL2591
     - Illumination
   * - MMC56x3
     - Magnetic Field

The following I2C addresses are matched by default:

.. csv-table:: I2C address mapping
   :widths: 50 50
   :header-rows: 1

   I2C address, Sensor name
   16, VEML7700
   35, BH1750
   48, MMC56x3
   68, SHT4x
   89, SGP40
   98, SCD4x
   119, BME680

Build and upload
================

.. code-block:: sh

   poetry publish --build

Install on server
=================

Software
--------

It is recommended to use a virtual environment.

.. code-block:: sh

   virtualenv /usr/local/share/klimalogger
   . /usr/local/share/klimalogger/bin/activate
   pip install klimalogger

Then setup the configuration file ``/etc/klimalogger.conf``.

The sensor readout can be validated through

.. code-block:: sh

   /usr/local/share/klimalogger/bin/klimalogger --check

The result should be JSON formatted measurement data.

In order to run the service for debugging use the following command line

.. code-block:: sh

   /usr/local/share/klimalogger/bin/klimalogger --service --debug

Setup Service
-------------

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

Run on Circuitpython targets
============================

This version should be compatible with Circuitpython 9.x and 10.x.

Example config
--------------

Set the following values in the `settings.toml` on the device.

.. code-block:: toml

   WIFI_SSID = "SSDF"
   WIFI_PASSWORD = "XZCXCZXC"
   MQTT_HOST = "mqtt"
   MQTT_PREFIX = "sensors/test"
   ELEVATION = "530"

Internal LED Color coding
-------------------------

.. csv-table:: LED color coding
   :widths: 50 50
   :header-rows: 1

   Step,Color
   WLAN connect, yellow
   NTP update, magenta
   MQTT connect / update, white
   Sensor detection, cyan
   Sensor readout, blue
   Operation, green -> red

Install
-------

Connect a Circuitpython device so that `/Volumes/CIRCUITPY` is mounted.

Update Circuitpython
^^^^^^^^^^^^^^^^^^^^

Press and hold BOOT button and press reset to get into bootloader mode.

Run

.. code-block:: sh

   esptool write-flash -e 0 ~/Downloads/adafruit-circuitpython-adafruit_qtpy_esp32s2-en_US-10.0.3.bin

Update dependencies
^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

   circup install -r requirements_cpy.txt

Install software
^^^^^^^^^^^^^^^^

Run `./install.py` which will copy the sources

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
