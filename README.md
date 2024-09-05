
Python package for querying nordpool for average daily prices.
Prices can only be obtained for the current year and the previous year.
Incremet is how much you need to add to the price if you chargeback someone per kWh. It's optional and the default is zero

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

EMAIL_RECEIVERS is a list like this ["person1@domain.com","person2@gmail.com","person3@hotmail.com"] or it can be just one user

| Environment variables | Usage                    | Required           | Syntax                   | Comment                                            |
|-----------------------|--------------------------|--------------------|--------------------------|----------------------------------------------------|
| LOGLEVEL              | stdout logging level     | No                 | DEBUG                    | Defaults to INFO if not used                       |
| EMAIL_HOST            | host for outgoing emails | No                 | "myhost@acme.com"        | If not existing no email error sending, port is 25 |
| EMAIL_SUBJECT         | Subject in email         | Yes if EMAIL_HOST  | "Something went wrong"   | What will in the subject for the email             |
| EMAIL_SENDER          | Who will be sender       | Yes if EMAIL_HOST  | "first.last@acme.com"    | Which email address will be sender                 |
| EMAIL_RECEIVERS       | Who will reseive the mail| Yes if EMAIL_HOST  | See above                | Who will receive the email(s)                      |


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

