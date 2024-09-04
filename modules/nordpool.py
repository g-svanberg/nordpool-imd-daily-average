import httpx
import datetime

"""Default areacode for class instantiation"""
areacode = "SE3"
currency = "SEK"


class Prices:
    # Constructor
    def __init__(self):
        pass

    def get_prices_for_one_date(self, date: datetime) -> str:
        pass
