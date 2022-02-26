import math


class TemperatureCalc:

    def dew_point(self, temperature: float, relative_humidity: float):
        """
        Dew point calculation using the Arden Buck equation based calculation, see https://en.wikipedia.org/wiki/Dew_point
        :param temperature: Temperature in degress Celsius
        :param relative_humidity: Relavite humidity in percent (range 0..1)
        :return: Calculated dew point in degrees Celsius
        """

        a = 6.1121  # hPa
        b = 18.678
        c = 257.14  # °C
        d = 234.5  # °C

        gamma = math.log(relative_humidity/100.0 *
                         math.exp((b - temperature / d) * (temperature / (c + temperature))))

        return c * gamma / (b - gamma)