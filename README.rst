`klimalogger <https://github.com/wuan/klimalogger>`_
====================================================

.. image:: https://badge.fury.io/gh/wuan%2Fklimalogger.svg
    :alt: project on GitHub
    :target: http://badge.fury.io/gh/wuan%2Fklimalogger
.. image:: https://badge.fury.io/py/klimalogger.svg
    :alt: PyPi-Package
    :target: https://badge.fury.io/py/klimalogger
.. image:: https://travis-ci.org/wuan/klimalogger.svg?branch=main
    :alt: Build Status
    :target: https://travis-ci.org/wuan/klimalogger
.. image:: https://app.codacy.com/project/badge/Grade/143e5b4f902b4680a2b9fd6464736f6b
    :target: https://www.codacy.com/gh/wuan/klimalogger/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wuan/klimalogger&amp;utm_campaign=Badge_Grade
.. image:: https://app.codacy.com/project/badge/Coverage/143e5b4f902b4680a2b9fd6464736f6b
    :target: https://www.codacy.com/gh/wuan/klimalogger/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wuan/klimalogger&amp;utm_campaign=Badge_Coverage

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