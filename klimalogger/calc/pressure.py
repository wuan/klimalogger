def sea_level_pressure(pressure: float, temperature: float, elevation: float) -> float:
    return pressure * pow(1 - (0.0065 * elevation / (temperature + 0.0065 * elevation + 273.15)), -5.255)
