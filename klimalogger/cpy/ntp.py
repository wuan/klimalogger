import os
from time import mktime

import adafruit_ntp
import rtc


class Ntp:

    def __init__(self, pool):
        ntp_server = os.getenv("NTP_SERVER")
        kwargs = {}
        if ntp_server:
            print(f"using NTP Server: {ntp_server}")
            kwargs = {"server": ntp_server}

        self.ntp = adafruit_ntp.NTP(pool, tz_offset=0, **kwargs)
        self.rtc = rtc.RTC()

    def update_time(self):
        try:
            ntp_datetime = self.ntp.datetime
        except Exception as e:
            print("  Ntp.update_time() failed:", e)
            raise e

        difference = mktime(ntp_datetime) - mktime(self.rtc.datetime)
        print(f"  updating time (with difference: {difference})")
        self.rtc.datetime = ntp_datetime

    @staticmethod
    def difference(struct1, struct2):
        return Ntp.to_datetime(struct1) - Ntp.to_datetime(struct2)

    @staticmethod
    def to_datetime(struct):
        return mktime(struct)
