import quandl
import matplotlib.pyplot as plt
from Basics.tickerchanger import quandl_to_yahoo

# Sans votre cle le nombre d'appel aux databases est limite

# your_key = 'Inscrivez votre cle pour API'
# quandl.ApiConfig.api_key = your_key

symbol = "TO_BBD_A"
print(quandl_to_yahoo(symbol))

data = quandl.get("YAHOO/" + symbol + ".6", start_date="2010-01-01", end_date="2016-10-31")
print(data)
plt.plot(data)
plt.show()


