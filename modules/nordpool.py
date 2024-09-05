import httpx
from datetime import datetime
import random
import os
import sys
import logging

log_level = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    stream=sys.stdout, format="%(asctime)s:%(levelname)s:%(message)s", level=getattr(logging, log_level, logging.INFO)
)
logger = logging.getLogger()
logger.setLevel(getattr(logging, log_level, logging.INFO))


def do_error_handling_by_mail(msg: str) -> bool:
    return True


def get_header() -> dict:
    """Returns a header dictionary with a random existing user agent to be used

    Returns:
        dict: http header
    """
    header = {"Content-Type": "application/json; charset=utf-8", "Accept": "application/json, text/plain, */*"}
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15\
        (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    ]
    random_number = random.randint(0, 3)
    header["User-Agent"] = user_agents[random_number]
    logging.info("returning headers")
    return header


class Prices:
    def __init__(
        self,
        areacode: str,
        currency: str,
        increment: str = "0",
        proxy: dict = None,
        verify: bool = True,
    ):
        self.areacode = areacode
        self.currency = currency
        self.increment = float(increment)
        self.proxy = proxy
        self.verify = verify
        self.this_year = datetime.now().year
        """Get previous year is this runs in january. And you need to harvest december data"""
        self.previous_year = self.this_year - 1
        """Get this year of data from nordpool"""
        self.headers = get_header()
        try:
            url = f"https://dataportal-api.nordpoolgroup.com/api/AggregatePrices?year={str(self.this_year)}&market=DayAhead&deliveryArea={self.areacode}&currency={self.currency}"
            res = httpx.get(url, headers=self.headers, verify=self.verify, proxies=self.proxy)
            if res.status_code == 200:
                data = res.json()
                self.this_year_data = data["multiAreaDailyAggregates"]
            else:
                """Error handling"""
                msg = f"Call to Nord Pool for current year did not return a 200 status code, code returned was {res.status_code}"
                logging.error(msg)
                do_error_handling_by_mail(msg)
        except Exception as e:
            logging.error(e)
            do_error_handling_by_mail(e)

        """Get last year data from nordpool"""
        self.headers = get_header()
        try:
            url = f"https://dataportal-api.nordpoolgroup.com/api/AggregatePrices?year={str(self.previous_year)}&market=DayAhead&deliveryArea={self.areacode}&currency={self.currency}"
            res = httpx.get(url, headers=self.headers, verify=self.verify, proxies=self.proxy)
            if res.status_code == 200:
                data = res.json()
                self.last_year_data = data["multiAreaDailyAggregates"]
            else:
                msg = f"Call to Nord Pool for previous year did not return a 200 status code, code returned was {res.status_code}"
                """Error handling"""
                logging.error(msg)
                do_error_handling_by_mail(msg)
        except Exception as e:
            logging.error(e)
            do_error_handling_by_mail(e)

        """Merge the 2 years into one list"""
        self.averages = self.this_year_data + self.last_year_data
        """Strip keys we dont need just get date and price"""
        final_list = []
        for entry in self.averages:
            if entry["deliveryStart"] != entry["deliveryEnd"]:
                """Error handling Something wrong with the data"""
                msg = "Something is wrong with the data from nordpool start and end date's does not match"
                do_error_handling_by_mail(msg)
                logging.error(msg)

            """prices are in mWh need to convert to kwH and round to 3 decimals"""
            final_list.append(
                {
                    "date": entry["deliveryStart"],
                    "price": round(entry["averagePerArea"][self.areacode] / 1000 + self.increment, 3),
                }
            )
        self.averages = final_list

    def get_all_prices(self) -> dict:
        """Returns all prices and date's

        Returns:
            dict: Dictionary for all dates in the current and last year
        """
        return self.averages

    def get_prices_for_one_date(self, date: datetime) -> str:
        """Returns price for given date

        Args:
            date (datetime): Date to get price from

        Raises:
            IndexError: If year is not cuurent or past

        Returns:
            str: Average daily price
        """
        this_year = datetime.now().year
        last_year = this_year - 1
        year = int(date.split("-")[0])
        if year != this_year and year != last_year:
            logging.error(f"Year is out of bounds, has to be current or last, was {year}")
            raise IndexError("Index out of bounds")
        for day in self.averages:
            if day["date"] == date:
                return day["price"]
