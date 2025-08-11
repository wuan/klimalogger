import configparser
from unittest import mock

import pytest
from mock import patch

from klimalogger.measurement import Measurements
from klimalogger.sensor.bmp3xx import Sensor


@pytest.fixture
def sensor_module():
    # Patch the external dependency so tests don't require the hardware library
    with patch('klimalogger.sensor.bmp3xx.adafruit_bmp3xx', autospec=True) as mock_module:
        yield mock_module


@pytest.fixture
def config_parser():
    cp = configparser.ConfigParser()
    cp.add_section('bmp3xx_sensor')
    cp.set('bmp3xx_sensor', 'elevation', '123')
    return cp


@pytest.fixture
def uut(sensor_module, i2c_bus, config_parser, pressure_calc):
    return Sensor(i2c_bus=i2c_bus, config_parser=config_parser, pressure_calc=pressure_calc)


def test_init_constructs_driver(uut, sensor_module, i2c_bus):
    # Driver constructed with given bus
    sensor_module.BMP3XX_I2C.assert_called_once_with(i2c_bus)


def test_measure_adds_pressure_and_sea_level_pressure(uut, sensor_module, data_builder, pressure_calc):
    # Given hardware readings
    measured_temperature = 21.2345
    measured_pressure = 1001.234

    drv = sensor_module.BMP3XX_I2C.return_value
    drv.temperature = measured_temperature
    drv.pressure = measured_pressure

    # And calculated value
    calc_sea_level_pressure = 1015.678
    pressure_calc.sea_level_pressure.return_value = calc_sea_level_pressure

    meas = Measurements()

    # When
    uut.measure(data_builder, meas)

    # Then: 2 records added with proper rounding
    assert len(data_builder.data) == 2
    types_units_values = [(e["tags"]["type"], e["tags"]["unit"], e["fields"]["value"]) for e in data_builder.data]

    assert ("pressure", "hPa", round(measured_pressure, 2)) in types_units_values
    assert ("sea level pressure", "hPa", round(calc_sea_level_pressure, 2)) in types_units_values

    # Check sensor tag and calculated flag on sea level pressure
    slp_entries = [e for e in data_builder.data if e["tags"]["type"] == "sea level pressure"]
    assert slp_entries and slp_entries[0]["tags"]["sensor"] == "BMP3xx"
    assert slp_entries[0]["tags"]["calculated"] is True

    # Ensure calculator was called with expected values; elevation must be int from config (123)
    assert pressure_calc.sea_level_pressure.call_args_list == [
        mock.call(measured_pressure, measured_temperature, 123)
    ]
