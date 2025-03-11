def sea_level_pressure(pressure: float, temperature_celsius: float, elevation: float) -> float:
    temperature = temperature_celsius + 273.15
    return pressure * pow(temperature / (temperature + 0.0065 * elevation), -5.255)
