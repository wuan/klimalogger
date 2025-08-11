import configparser
from unittest import mock

import pytest
from mock import patch

from klimalogger.measurement import Measurements
from klimalogger.sensor.bme680 import Sensor


@pytest.fixture
def sensor_module():
    # Patch the external dependency so tests don't require the hardware library
    with patch('klimalogger.sensor.bme680.adafruit_bme680', autospec=True) as mock_module:
        yield mock_module


@pytest.fixture
def config_parser():
    cp = configparser.ConfigParser()
    cp.add_section('bme680_sensor')
    cp.set('bme680_sensor', 'elevation', '123')
    return cp


@pytest.fixture
def uut(sensor_module, i2c_bus, config_parser, temp_calc, pressure_calc):
    return Sensor(i2c_bus=i2c_bus, config_parser=config_parser, temperature_calc=temp_calc, pressure_calc=pressure_calc)


def test_init_constructs_driver_and_sets_heater(uut, sensor_module, i2c_bus):
    # Driver constructed with given bus
    sensor_module.Adafruit_BME680_I2C.assert_called_once_with(i2c_bus)
    # Gas heater disabled
    sensor_module.Adafruit_BME680_I2C.return_value.set_gas_heater.assert_called_once_with(None, None)


def test_measure_adds_all_fields_and_updates_measurements(uut, sensor_module, data_builder, temp_calc, pressure_calc):
    # Given hardware readings
    measured_temperature = 21.2345
    measured_relative_humidity = 55.555
    measured_pressure = 1001.234
    measured_gas = 45678

    drv = sensor_module.Adafruit_BME680_I2C.return_value
    drv.temperature = measured_temperature
    drv.relative_humidity = measured_relative_humidity
    drv.pressure = measured_pressure
    drv.gas = measured_gas

    # And calculated values
    calc_dew_point = 10.5555
    calc_sea_level_pressure = 1015.678
    temp_calc.dew_point.return_value = calc_dew_point
    pressure_calc.sea_level_pressure.return_value = calc_sea_level_pressure

    meas = Measurements()

    # When
    uut.measure(data_builder, meas)

    # Then: measurements updated (note: bme680 sensor stores raw values without rounding)
    assert meas.temperature == measured_temperature
    assert meas.relative_humidity == measured_relative_humidity

    # And 6 records added with proper rounding
    assert len(data_builder.data) == 6
    types_units_values = [(e["tags"]["type"], e["tags"]["unit"], e["fields"]["value"]) for e in data_builder.data]

    assert ("temperature", "°C", round(measured_temperature, 2)) in types_units_values
    assert ("relative humidity", "%", round(measured_relative_humidity, 2)) in types_units_values
    assert ("dew point", "°C", round(calc_dew_point, 2)) in types_units_values
    assert ("pressure", "hPa", round(measured_pressure, 2)) in types_units_values
    assert ("sea level pressure", "hPa", round(calc_sea_level_pressure, 2)) in types_units_values
    assert ("voc gas", "Ohm", float(measured_gas)) in types_units_values

    # Check sensor tag and calculated flag on dew point
    dew_entries = [e for e in data_builder.data if e["tags"]["type"] == "dew point"]
    assert dew_entries and dew_entries[0]["tags"]["sensor"] == "BME680"
    assert dew_entries[0]["tags"]["calculated"] is True

    # Ensure calculators were called with expected values; elevation must be int from config (123)
    assert temp_calc.dew_point.call_args_list == [
        mock.call(measured_temperature, measured_relative_humidity)
    ]
    assert pressure_calc.sea_level_pressure.call_args_list == [
        mock.call(measured_pressure, measured_temperature, 123)
    ]
