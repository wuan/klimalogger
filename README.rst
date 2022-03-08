`klimalogger <https://github.com/wuan/klimalogger>`_
============================================

.. image:: https://badge.fury.io/gh/wuan%2Fklimalogger.svg
    :alt: project on GitHub
    :target: http://badge.fury.io/gh/wuan%2Fklimalogger
.. image:: https://badge.fury.io/py/klimalogger.svg
    :alt: PyPi-Package
    :target: https://badge.fury.io/py/klimalogger
.. image:: https://travis-ci.org/wuan/klimalogger.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/wuan/klimalogger
.. image:: https://coveralls.io/repos/wuan/klimalogger/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/wuan/klimalogger?branch=master

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
   * - SHT1x
     - download and install https://bitbucket.org/lunobili/rpisht1x.git
   * - SHT40
     - ``pip3 install adafruit-circuitpython-sht4x``