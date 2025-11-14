# klimalogger

[![PyPI](https://badge.fury.io/py/klimalogger.svg)](https://badge.fury.io/py/klimalogger)
[![Lines of code](https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=ncloc)](https://sonarcloud.io/project/overview?id=wuan_klimalogger)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=coverage)](https://sonarcloud.io/project/overview?id=wuan_klimalogger)
[![Duplicated lines](https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=duplicated_lines_density)](https://sonarcloud.io/project/overview?id=wuan_klimalogger)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/wuan/klimalogger/badge)](https://scorecard.dev/viewer/?uri=github.com/wuan/klimalogger)

Simple python client for logging measured climate data to MQTT targets.

## Sensor support

As of now the following sensors are supported:

| Sensor Type                      | Measurement                                          |
| -------------------------------- | ---------------------------------------------------- |
| BME680                           | Barometric pressure, Temperature, Relative humidity, Air quality |
| BMP3xx                           | Temperature, Barometric Pressure                     |
| SGP30                            | Air quality                                          |
| SGP40                            | Air quality                                          |
| SHT4x                            | Temperature, Relative Humidity                       |
| SCD4x                            | CO2 concentration                                    |
| PM25                             | Particle concentration                               |
| BH1750, VEML7700, TSL2591        | Illumination                                         |
| MMC56x3                          | Magnetic Field                                       |

## Build and upload

```sh
python3 -m build
python3 -m pip install --upgrade twine
# Upload all artifacts from dist/ (wheel and sdist)
python3 -m twine upload dist/*
```

## Install on server

### Software

It is recommended to use a virtual environment.

```sh
virtualenv /usr/local/share/klimalogger
. /usr/local/share/klimalogger/bin/activate
pip install klimalogger
```

Then setup the configuration file `/etc/klimalogger.conf`.

The sensor readout can be validated through:

```sh
/usr/local/share/klimalogger/bin/klimalogger --check
```

The result should be JSON formatted measurement data.

In order to run the service for debugging use the following command line:

```sh
/usr/local/share/klimalogger/bin/klimalogger --service --debug
```

### Setup Service

Create a service configuration, for example `/etc/systemd/system/klimalogger.service` with the following content:

```
[Unit]
Description=Klimalogger Service
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/local/share/klimalogger/bin/klimalogger --service

[Install]
WantedBy=multi-user.target
```

and run

```sh
systemctl daemon-reload
systemctl enable klimalogger
service klimalogger start
```

to run the service.

## Run on Circuitpython targets

### Install

Connect a Circuitpython device so that `/Volumes/CIRCUITPY` is mounted.

### Update Circuitpython

Press and hold BOOT button and press reset to get into bootloader mode.

Run

```sh
esptool write-flash -e 0 ~/Downloads/adafruit-circuitpython-adafruit_qtpy_esp32s2-en_US-10.0.3.bin
```

### Update dependencies

```sh
circup install -r requirements_cpy.txt
```

### Install software

Run `./install.py` which will copy the sources

## Pre-commit hooks

This repository includes a pre-commit configuration to automatically run formatting, linting and type checks on each commit.

Setup locally:

```sh
pip install pre-commit
pre-commit install
```

You can also run all hooks against the full repo:

```sh
pre-commit run --all-files
```

The configured tools include:

- black and isort for formatting
- ruff for linting (auto-fixes enabled)
- mypy for type checking (configured in mypy.ini)
