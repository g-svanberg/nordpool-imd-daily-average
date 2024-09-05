# nordpool-imd-daily-average

[Link to github repository](https://github.com/g-svanberg/nordpool-imd-daily-average)

Python package for querying nordpool for average daily prices.
Prices can only be obtained for the current year and the previous year.

| Supported areacode's  | Suported currency's |
|-----------------------|---------------------|
| `"SE1"`               | `"SEK"`             |
| `"SE2"`               | `"EUR"`             |
| `"SE3"`               | 
| `"SE4"`               | 
| `"NO1"`               | 
| `"NO2"`               | 
| `"NO3"`               | 
| `"NO4"`               | 
| `"NO5"`               | 
| `"FI"`                | 
| `"DK1"`               | 
| `"DK2"`               | 


Usage:  
`pip install nordpool-daily-averages`  

~~~python
#Getting average price for 2024-08-30, for areacode SE3 and in Euro  
from nordpool import Prices as p
#instantiate class
price = p("SE3", "EUR")
#Get the price
price.get_prices_for_one_date("2024-08-30")
~~~

~~~python
#Getting average price for 2024-08-29 for areacode SE3 in SEK  
from nordpool import Prices as p
#instantiate class
price = p("SE3","SEK")
#Get the price
price.get_prices_for_one_date("2024-08-29")
~~~

~~~python
#Getting average price for 2024-08-28 for areacode SE2 in SEK  
from nordpool import Prices as p
#instantiate class
price = p("SE2","SEK")
#Get the price
price.get_prices_for_one_date("2024-08-28")
~~~
