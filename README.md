# nordpool-imd-daily-average

[Link to github repository](https://github.com/g-svanberg/nordpool-imd-daily-average)

Python package for querying nordpool for average daily prices.
Prices can only be obtained for the current year and the previous year.
Incremet is how much you need to add to the price if you chargeback someone. It's optional and the default is zero

| Supported areacode's  | Suported currency's | Increment |
|-----------------------|---------------------|-----------|
| `"SE1"`               | `"SEK"`             | `"0.15"`  |
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


| Environment variables | Usage                    | Optional | Syntax                   | Comment                                         |
|-----------------------|--------------------------|----------|--------------------------|-------------------------------------------------|
| ERROR_EMAIL           | Where to send exceptions | Yes      | first.last@gmail.com     | If not used only local logging will occur       |
| LOGLEVEL              | stdout logging level     | Yes      | DEBUG                    | Defaults to INFO if not used                    |


Usage:  
`pip install nordpool-daily-averages`  

~~~python
#Getting average price for 2024-08-30, for areacode SE3 and in Euro and 15 cents is added to the prices  
from nordpool import Prices as p
#instantiate class
price = p("SE3", "EUR", "0.15")
#Get the price
price.get_prices_for_one_date("2024-08-30")
~~~

~~~python
#Getting average price for 2024-08-29 for areacode SE3 in SEK and 15 öre is added to the prices  
from nordpool import Prices as p
#instantiate class
price = p("SE3", "SEK", "0.15")
#Get the price
price.get_prices_for_one_date("2024-08-29")
~~~

~~~python
#Getting average price for 2024-08-28 for areacode SE2 in SEK and no increment is added to the prices  
from nordpool import Prices as p
#instantiate class
price = p("SE2", "SEK")
#Get the price
price.get_prices_for_one_date("2024-08-28")
~~~

~~~python
#Getting all price's for current year and last year for areacode SE2 in SEK and no increment is added to the prices  
from nordpool import Prices as p
#instantiate class
price = p("SE2", "SEK")
#Get all price's
price.get_all_prices()
~~~

