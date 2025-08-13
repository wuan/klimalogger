import math


class TemperatureCalc:

    def dew_point(self, temperature: float, relative_humidity: float):
        """
        Dew point calculation using the calculation published by Mark G. Lawrence (https://journals.ametsoc.org/view/journals/bams/86/2/bams-86-2-225.xml)

        :param temperature: Temperature in degrees Celsius
        :param relative_humidity: Relavite humidity in percent (range 0..1)

        :return: Calculated dew point in degrees Celsius
        """

        # Parameters according to Alduchov and Eskridge (https://journals.ametsoc.org/view/journals/apme/35/4/1520-0450_1996_035_0601_imfaos_2_0_co_2.xml)
        a = 17.625
        b = 243.04  # °C

        # Formula according to Lawrence:
        # Ts = (b × alpha(T,RH)) / (a - alpha(T,RH))
        # with alpha(T,RH) = ln(RH/100) + aT/(b+T)

        alpha = math.log(relative_humidity / 100) + a * temperature / (b + temperature)

        return (b * alpha) / (a - alpha)
