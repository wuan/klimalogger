# klimalogger

[![PyPI](https://badge.fury.io/py/klimalogger.svg)](https://badge.fury.io/py/klimalogger)
[![Lines of code](https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=ncloc)](https://sonarcloud.io/project/overview?id=wuan_klimalogger)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=coverage)](https://sonarcloud.io/project/overview?id=wuan_klimalogger)
[![Duplicated lines](https://sonarcloud.io/api/project_badges/measure?project=wuan_klimalogger&metric=duplicated_lines_density)](https://sonarcloud.io/project/overview?id=wuan_klimalogger)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/wuan/klimalogger/badge)](https://scorecard.dev/viewer/?uri=github.com/wuan/klimalogger)

A Python client for logging environmental sensor data to MQTT brokers. Supports both server deployments (Linux/Unix with systemd) and embedded CircuitPython microcontrollers (ESP32, RP2040, etc.).

## Features

- **Automatic sensor detection** via I2C bus scanning
- **Multiple deployment targets**: Server (systemd) and CircuitPython microcontrollers
- **MQTT-based data transport** with configurable QoS
- **Flexible configuration**: File-based (server) or environment variable-based (CircuitPython)
- **Periodic measurements** with configurable intervals
- **Built-in calculations**: Sea-level pressure adjustment, temperature compensation

## Supported Sensors

All sensors use I2C communication and are automatically detected:

| Sensor Type                      | Measurement                                          | I2C Address (Hex) |
| -------------------------------- | ---------------------------------------------------- | ----------------- |
| BME680                           | Temperature, Humidity, Pressure, Air Quality (VOC)   | 0x77              |
| BMP3xx                           | Temperature, Pressure                                | Various           |
| DPS310                           | Temperature, Pressure                                | Various           |
| SHT4x                            | Temperature, Relative Humidity                       | 0x44              |
| SGP30                            | Air Quality (eCO2, TVOC)                             | Various           |
| SGP40                            | Air Quality (VOC raw)                                | 0x59              |
| SCD4x                            | CO2 Concentration                                    | 0x62              |
| PM25                             | Particulate Matter (PM1.0, PM2.5, PM10)              | 0x12              |
| BH1750                           | Light Intensity                                      | 0x23              |
| VEML7700                         | Ambient Light                                        | 0x10              |
| TSL2591                          | Light (Visible + IR)                                 | 0x29              |
| MMC56x3                          | Magnetic Field (3-axis)                              | 0x30              |

## Installation

### Server Deployment (Linux/Unix)

#### 1. Install via pip

It is recommended to use a virtual environment:

```sh
# Create virtual environment
virtualenv /usr/local/share/klimalogger

# Activate virtual environment
. /usr/local/share/klimalogger/bin/activate

# Install klimalogger
pip install klimalogger
```

#### 2. Configure

Create a configuration file at `/etc/klimalogger.conf`:

```ini
[queue]
host=mqtt.example.com
port=1883
queue_prefix=sensors
queue_qos=1
# Optional authentication
username=mqtt_user
password=mqtt_password

[client]
# Optional: Explicitly specify sensor I2C addresses (hex, comma-separated)
# If not specified, sensors are auto-detected
# sensors=0x44,0x62,0x77

# Optional: Override default device mapping
# device_map=0x44=SHT4x,0x62=SCD4x

# Optional: Elevation in meters for pressure calculations
elevation=100
```

Alternate config locations (checked in order):
- `./klimalogger.conf`
- `/etc/klimalogger/klimalogger.conf`
- `/etc/klimalogger.conf`

#### 3. Test

Validate sensor detection and readout:

```sh
/usr/local/share/klimalogger/bin/klimalogger --check
```

This outputs JSON-formatted measurement data.

For debugging with verbose output:

```sh
/usr/local/share/klimalogger/bin/klimalogger --service --debug
```

#### 4. Setup systemd Service

Create `/etc/systemd/system/klimalogger.service`:

```ini
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

Enable and start the service:

```sh
sudo systemctl daemon-reload
sudo systemctl enable klimalogger
sudo systemctl start klimalogger

# Check status
sudo systemctl status klimalogger

# View logs
sudo journalctl -u klimalogger -f
```

### CircuitPython Deployment (ESP32, RP2040, etc.)

#### 1. Hardware Setup

Connect your CircuitPython device via USB. The device should mount as `/Volumes/CIRCUITPY` (macOS) or similar on Linux/Windows.

Verified boards include:
- Adafruit QT Py ESP32-S2
- Adafruit QT Py ESP32-S3

Any CircuitPython-compatible board with I2C support should be supported with some minor modifications.

#### 2. Install CircuitPython (if needed)

To update to the latest CircuitPython firmware:

1. Enter bootloader mode (press BOOT + RESET, then release RESET)
2. Flash firmware using esptool:

```sh
esptool write-flash -e 0 ~/Downloads/adafruit-circuitpython-*.bin
```

Download firmware from [circuitpython.org/downloads](https://circuitpython.org/downloads)

#### 3. Install Dependencies

Install required CircuitPython libraries using `circup`:

```sh
# Install circup if needed
pip install circup

# Install dependencies
circup install -r requirements_cpy.txt
```

#### 4. Configure Environment

Create a `settings.toml` file in the root of your CircuitPython device:

```toml
# WiFi Configuration
WIFI_SSID = "your-wifi-ssid"
WIFI_PASSWORD = "your-wifi-password"

# MQTT Configuration
MQTT_HOST = "mqtt.example.com"
MQTT_PORT = "1883"
MQTT_PREFIX = "sensors"
MQTT_USERNAME = "mqtt_user"  # Optional
MQTT_PASSWORD = "mqtt_password"  # Optional

# Optional: Elevation in meters
ELEVATION = "100"

# Optional: Device mapping (address=SensorName)
DEVICE_MAP = "0x44=SHT4x,0x62=SCD4x"
```

#### 5. Deploy Software

Run the installation script to copy source files to your device:

```sh
./install.py
```

This copies the `klimalogger` package and `main_cpy.py` to your CircuitPython device.

#### 6. Run

The device will automatically run `main_cpy.py` on boot. To restart:

- Press CTRL+D in the REPL, or
- Reset the device

Monitor output via the serial console:

```sh
# macOS/Linux
screen /dev/tty.usbmodem* 115200

# Or use Mu Editor's serial console
```

## Development

### Requirements

- Python 3.10 or later
- Poetry for dependency management

### Setup Development Environment

```sh
# Clone the repository
git clone https://github.com/wuan/klimalogger.git
cd klimalogger

# Install dependencies with Poetry
poetry install

# Activate virtual environment
poetry shell
```

### Running Tests

```sh
# Run all tests
pytest

# Run with coverage report
pytest --cov=klimalogger

# Run specific test file
pytest tests/sensor/test_bme680.py
```

### Code Quality

This project uses pre-commit hooks for code quality:

```sh
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

Configured tools:
- **black** and **isort**: Code formatting
- **ruff**: Linting with auto-fixes
- **mypy**: Static type checking

### Building and Publishing

```sh
# Build distribution packages
python3 -m build

# Upload to PyPI
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```

## Project Structure

```
klimalogger/
├── klimalogger/           # Main package
│   ├── sensor/           # Individual sensor drivers
│   ├── calc/             # Calculation utilities (pressure, temperature)
│   ├── cpy/              # CircuitPython-specific code
│   ├── script/           # CLI entry points
│   ├── config.py         # Configuration management
│   ├── transport.py      # MQTT transport layer
│   ├── measurement.py    # Data structures
│   └── sensors.py        # Sensor management and auto-detection
├── tests/                # Test suite
├── main_cpy.py           # CircuitPython entry point
├── install.py            # CircuitPython deployment script
└── pyproject.toml        # Poetry configuration
```

## Usage Examples

### Check Sensor Data

```sh
klimalogger --check
```

Output:
```json
{
  "sensor": "SHT4x",
  "measurement": "temperature",
  "value": 23.5,
  "unit": "°C"
}
```

### Run as Service

```sh
# With default log level (warnings only)
klimalogger --service

# With verbose output
klimalogger --service --verbose

# With debug output
klimalogger --service --debug
```

### Check Version

```sh
klimalogger --version
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run pre-commit hooks
5. Submit a pull request

## License

Apache License 2.0 - See LICENSE file for details.

## Links

- **PyPI**: https://pypi.org/project/klimalogger/
- **GitHub**: https://github.com/wuan/klimalogger
- **Issues**: https://github.com/wuan/klimalogger/issues
