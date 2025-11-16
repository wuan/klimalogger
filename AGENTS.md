# klimalogger - Agent Context

This document provides context for AI coding assistants working with the klimalogger codebase.

## Project Overview

klimalogger is a Python-based climate data logging client that reads sensor data and publishes it to MQTT brokers. The project supports both standard Python environments (Linux/Unix servers) and CircuitPython microcontrollers.

**Key Features:**
- Multiple sensor support (temperature, humidity, pressure, air quality, CO2, light, magnetic field, particulate matter)
- MQTT-based data transport
- Dual deployment: Server mode (systemd service) and embedded mode (CircuitPython)
- Configurable via file (`/etc/klimalogger.conf`) or environment variables

## Architecture

### Core Components

1. **Sensors** (`klimalogger/sensor/`)
   - Individual sensor drivers for each supported device
   - Each sensor module provides a consistent interface for reading measurements
   - Supported sensors: BME680, BMP3xx, SGP30, SGP40, SHT4x, SCD4x, PM25, BH1750, VEML7700, TSL2591, MMC56x3, DPS310

2. **Configuration** (`klimalogger/config.py`)
   - Handles two configuration modes:
     - File-based: Reads from `/etc/klimalogger.conf` for server deployments
     - Environment-based: Uses env vars for CircuitPython deployments
   - Key settings: MQTT connection, device mapping, elevation, sensor addresses

3. **Transport** (`klimalogger/transport.py`)
   - Handles MQTT communication
   - Publishes measurement data to configured topics

4. **Measurement** (`klimalogger/measurement.py`)
   - Data structures for sensor readings
   - Handles data formatting and JSON serialization

5. **Data Builder** (`klimalogger/data_builder.py`)
   - Assembles sensor readings into publishable data structures

6. **Main Script** (`klimalogger/script/klimalogger.py`)
   - Entry point for the application
   - Supports three modes:
     - `--check`: Single measurement output
     - `--service`: Continuous periodic measurements
     - `--version`: Version information

7. **CircuitPython Support** (`klimalogger/cpy/`)
   - Platform-specific code for embedded deployments
   - Includes I2C, MQTT, NTP, and pixel (LED) support

### Calculation Modules

- `klimalogger/calc/temperature.py`: Temperature conversions and calculations
- `klimalogger/calc/pressure.py`: Pressure calculations (e.g., sea level adjustments)

## Project Structure

```
klimalogger/
├── klimalogger/           # Main package
│   ├── sensor/           # Individual sensor drivers
│   ├── calc/             # Calculation utilities
│   ├── cpy/              # CircuitPython-specific code
│   ├── script/           # Command-line scripts
│   ├── config.py         # Configuration management
│   ├── transport.py      # MQTT transport
│   ├── measurement.py    # Data structures
│   ├── data_builder.py   # Data assembly
│   ├── logger.py         # Logging setup
│   └── sensors.py        # Sensor management
├── tests/                # Test suite
├── install.py            # CircuitPython installer
├── main_cpy.py           # CircuitPython entry point
└── pyproject.toml        # Poetry configuration
```

## Development Workflow

### Dependencies
- Managed via Poetry (`pyproject.toml`)
- Uses Adafruit CircuitPython libraries for sensor support
- MQTT via `paho-mqtt`
- Python 3.10+

### Testing
- pytest-based test suite in `tests/`
- Test coverage tracked via pytest-cov
- Tests organized by component (sensor/, calc/, etc.)

### Code Quality
Pre-commit hooks enforce:
- **black** and **isort**: Code formatting
- **ruff**: Linting with auto-fixes
- **mypy**: Static type checking (config in `mypy.ini`)

Run locally:
```bash
pre-commit run --all-files
```

### Build & Release
```bash
python3 -m build
python3 -m twine upload dist/*
```

## Common Tasks

### Adding a New Sensor

1. Create sensor driver in `klimalogger/sensor/<sensor_name>.py`
2. Implement consistent interface (measurement methods, data structures)
3. Update `klimalogger/sensors.py` to register the sensor
4. Add tests in `tests/sensor/test_<sensor_name>.py`
5. Update README.md sensor table
6. If CircuitPython support needed, add to `requirements_cpy.txt`

### Modifying Configuration

Configuration is loaded in `klimalogger/config.py`:
- File-based config uses ConfigParser format
- Environment-based config for CircuitPython
- Update `Config` class when adding new settings

### Testing Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=klimalogger

# Run specific test
pytest tests/sensor/test_bme680.py
```

### CircuitPython Deployment

```bash
# Install dependencies
circup install -r requirements_cpy.txt

# Deploy code
./install.py
```

## Important Conventions

1. **Type Hints**: Use type hints throughout (enforced by mypy)
2. **Logging**: Use the logger from `klimalogger.logger`
3. **Error Handling**: Graceful degradation for missing sensors
4. **Platform Detection**: Use `config.is_circuitpython()` for platform-specific code
5. **I2C Addresses**: Sensors can be specified by address for multi-sensor setups

## Testing Philosophy

- Mock I2C communication in tests (see `tests/sensor/conftest.py`)
- Test sensor data parsing and calculations independently
- Verify configuration loading from different sources
- Test both happy paths and error conditions

## Deployment Targets

1. **Server Mode**: Linux/Unix systems with systemd
   - Virtual environment recommended
   - Service runs continuously
   - File-based configuration

2. **CircuitPython Mode**: ESP32, RP2040, etc.
   - Resource-constrained environment
   - Environment variable configuration
   - Direct flash memory deployment

## Key Files for Common Changes

- **Adding MQTT features**: `klimalogger/transport.py`
- **Changing measurement format**: `klimalogger/measurement.py`, `klimalogger/data_builder.py`
- **Modifying CLI**: `klimalogger/script/klimalogger.py`
- **Sensor auto-detection**: `klimalogger/sensors.py`
- **Configuration options**: `klimalogger/config.py`

## Notes for AI Assistants

- The codebase supports two very different runtime environments (CPython and CircuitPython)
- Sensor libraries are abstracted through Adafruit's unified CircuitPython API
- Configuration is intentionally duplicated (file vs. env) to support both deployment modes
- Type safety is important - maintain mypy compliance
- Tests should not require actual I2C hardware
