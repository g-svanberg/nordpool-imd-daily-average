import httpx
from datetime import datetime
import random
import os


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
        url = f"https://dataportal-api.nordpoolgroup.com/api/AggregatePrices?year={str(self.this_year)}&market=DayAhead&deliveryArea={self.areacode}&currency={self.currency}"
        res = httpx.get(url, headers=self.headers, verify=self.verify, proxies=self.proxy)
        if res.status_code == 200:
            data = res.json()
            self.this_year_data = data["multiAreaDailyAggregates"]
        else:
            """Error handling goes here"""
            do_error_handling_by_mail(
                f"Call to Nord Pool for current year did not return a 200 status code, code returned was {res.status_code}"
            )
        """Get last year data from nordpool"""
        self.headers = get_header()
        url = f"https://dataportal-api.nordpoolgroup.com/api/AggregatePrices?year={str(self.previous_year)}&market=DayAhead&deliveryArea={self.areacode}&currency={self.currency}"
        res = httpx.get(url, headers=self.headers, verify=self.verify, proxies=self.proxy)
        if res.status_code == 200:
            data = res.json()
            self.last_year_data = data["multiAreaDailyAggregates"]
        else:
            """Error handling goes here"""
            do_error_handling_by_mail(
                f"Call to Nord Pool for previous year did not return a 200 status code, code returned was {res.status_code}"
            )
        """Merge the 2 years into one list"""
        self.averages = self.this_year_data + self.last_year_data
        """Strip keys we dont need just get date and price"""
        final_list = []
        for entry in self.averages:
            if entry["deliveryStart"] != entry["deliveryEnd"]:
                """Error handling goes here. Something wrong with the data"""
                do_error_handling_by_mail(
                    "Something is wrong with the data from nordpool start and end date's does not match"
                )
            final_list.append(
                {
                    "date": entry["deliveryStart"],
                    "price": round(entry["averagePerArea"][self.areacode] / 1000 + self.increment, 3),
                }
            )
        self.averages = final_list

    def get_prices_both_years(self) -> dict:
        return self.averages

    def get_prices_for_one_date(self, date: datetime) -> str:

        pass


if __name__ == "__main__":
    if os.environ.get("WINDIR"):
        """If we run on windows for testing etc, load local .env file"""
        from dotenv import load_dotenv

        load_dotenv()
        AREACODE = os.environ.get("AREACODE")
        CURRENCY = os.environ.get("CURRENCY")
        INCREMENT = os.environ.get("INCREMENT")

    p = Prices(AREACODE, CURRENCY, INCREMENT)
    print(p.get_prices_both_years())
    # print(p.get_prices_last_year())
