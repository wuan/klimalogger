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
   * - BMP085
     - ``pip3 install Adafruit_BMP``
   * - BMP3xx
     - ``pip3 install adafruit-circuitpython-bmp3xx``
   * - SGP30
     - ``pip3 install adafruit-circuitpython-sgp30``
   * - SGP40
     - ``pip3 install adafruit-circuitpython-sgp40``
   * - SHT1x (no I2C)
     - download and install https://bitbucket.org/lunobili/rpisht1x.git
   * - SHT4x
     - ``pip3 install adafruit-circuitpython-sht4x``

Build and upload
----------------

.. code-block:: sh

   python3 -m build
   python3 -m pip install --upgrade twine
   python3 -m twine upload dist/klimalogger-0.6.8.tar.gz