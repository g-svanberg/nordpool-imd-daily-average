![Ruff](https://github.com/g-svanberg/nordpool-imd-daily-average/actions/workflows/ruff.yaml/badge.svg)
![Push](https://github.com/g-svanberg/nordpool-imd-daily-average/actions/workflows/push_to_repo.yaml/badge.svg)

Python package for querying nordpool for average daily and hourly prices per kWh.
Prices can only be obtained for the current year and the previous year.
Incremet is how much you need to add to the price if you chargeback someone per kWh. It's optional and the default is zero.
Default timezone is "Europe/Stockholm" 

| Supported areacode's | Suported currency's | Increment | Timezone             |
| -------------------- | ------------------- | --------- | -------------------- |
| `"SE1"`              | `"SEK"`             | `"0.15"`  | `"Europe/Stockholm"` |
| `"SE2"`              | `"EUR"`             |
| `"SE3"`              |
| `"SE4"`              |
| `"NO1"`              |
| `"NO2"`              |
| `"NO3"`              |
| `"NO4"`              |
| `"NO5"`              |
| `"FI"`               |
| `"DK1"`              |
| `"DK2"`              |

| Environment variables | Usage                | Required | Syntax | Comment                      |
| --------------------- | -------------------- | -------- | ------ | ---------------------------- |
| LOGLEVEL              | stdout logging level | No       | DEBUG  | Defaults to INFO if not used |

## Usage:

`pip install nordpool-daily-averages`

```python
#Getting average price for 2024-08-30, for areacode SE3 and in Euro and 15 cents is added to the prices
from nordpool import Daily as daily
#instantiate class
price = daily("SE3", "EUR", "0.15")
#Get the price
price.get_prices_for_one_date("2024-08-30")
```

```python
#Getting average price for 2024-08-29 for areacode SE3 in SEK and 15 öre is added to the prices
from nordpool import Daily as daily
#instantiate class
price = daily("SE3", "SEK", "0.15")
#Get the price
price.get_prices_for_one_date("2024-08-29")
```

```python
#Getting average price for 2024-08-28 for areacode SE2 in SEK and no increment is added to the prices
from nordpool import Daily as daily
#instantiate class
price = daily("SE2", "SEK")
#Get the price
price.get_prices_for_one_date("2024-08-28")
```

```python
#Getting all price's for current year and last year for areacode SE2 in SEK and no increment is added to the prices
from nordpool import Daily as daily
#instantiate class
price = daily("SE2", "SEK")
#Get all price's
price.get_all_prices()
```

```python
import asyncio
import httpx
from nordpool import Hourly as hour
#Getting hourly data prices for all the dates in a list concurrent. in SE3 and in SEK and add 8 öre as increment
#Dates can be max 2 months back in time
async def main():
    """Instantiate class"""
    spot = hourly("SE3", "SEK", "0.8")
    dates = ["2024-08-01", "2024-08-02", "2024-08-03"] #Usually all the dates in previous month
    """Get hour prices every date an append"""
    async with httpx.AsyncClient(timeout=10) as client:
        prices = [spot.get_hourly_prices(date, client) for date in dates]
        price = await asyncio.gather(*prices)
    print(price)

asyncio.run(main())
```
