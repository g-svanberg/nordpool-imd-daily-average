# nordpool-imd-daily-average

Link to github repository [https://github.com/g-svanberg/nordpool-imd-daily-average]

Python package for querying nordpool for average daily prices.
Price returned is a string of SEK/kWh
Default geo area is SE3 and currency SEK.
Can be changed by setting the class variable's currency and areacode

| areacode          |
| ----------------- |
| `"SE3"`           | 
| `"SE2"`           | 

Usage:
`pip install nordpool-daily-averages`

Getting average price for 2024-08-30, for areacode SE3 and in Euro
`
from nordpool import Prices as p
#instantiate class
price = p()
#Set price to Euro
price.curreny = "EUR"
#Get the price
price.get_prices_for_one_date("2024-08-30")
`

Getting average price for 2024-08-29 for areacode SE3 in SEK
`
from nordpool import Prices as p
#instantiate class
price = p()
#Get the price
price.get_prices_for_one_date("2024-08-29")
`

Getting average price for 2024-08-28 for areacode SE2 in SEK
`
from nordpool import Prices as p
#instantiate class
price = p()
#Set the areacode to SE2
price.areacode = "SE2"
#Get the price
price.get_prices_for_one_date("2024-08-29")
`
