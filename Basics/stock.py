import requests
from datetime import date, timedelta

__author__ = "Alexis Paquette"
__date__ = 2016 - 1 - 29


def get_stock(ticker):

    query = 'select * from yahoo.finance.quotes where symbol in ("' + ticker + '")'
    parameters = {'q': query, 'format': 'json', 'diagnostics': 'false',
                  'env': 'store://datatables.org/alltableswithkeys', 'callback': ''}

    response = requests.get('https://query.yahooapis.com/v1/public/yql', parameters).json()
    resultsdict = {ticker: response['query']['results']['quote']}

    if resultsdict[ticker]["Name"] is None:
        raise ValueError("Invalid Ticker")

    # Removing items where no data is avaible)
    # for key, value in list(resultsdict[ticker].items()):
    #     if value is None:
    #         del resultsdict[ticker][key]

    previousclose = resultsdict[ticker]["PreviousClose"]
    price = resultsdict[ticker]["LastTradePriceOnly"]
    change = str("%.2f" % (float(price) - float(previousclose)))
    change_percent = str('%.2f' % (float(change) / float(previousclose) * 100))+"%"
    name = resultsdict[ticker]['Name'].split(",")[0]
    # self.dailychange = resultsdict[self.ticker]['Change_PercentChange']
    y_range = resultsdict[ticker]['YearRange']

    return [name, ticker, change+"/"+change_percent, price, y_range]


def us_to_can(start_date, end_date=None):
    """Data from  2002-6-25 to today"""
    if end_date is None:
        end_date = start_date

    for arg in start_date, end_date:
        if isinstance(arg, date) is False:
            raise TypeError('Unexpected argument type: ' + str(type(arg)) + ', arguments must be datetime.date class.')

    # No more than 364 data point can be called from yahoo per call
    resultslist = []
    temp_start = start_date
    while True:
        temp_end = temp_start + timedelta(500)  # 364 weekdays is a bit more than a 500 days interval

        if temp_end > end_date:
            temp_end = end_date

        results = []
        query = 'select * from yahoo.finance.historicaldata where symbol = "CAD=X" and startDate = "' +\
                temp_start.isoformat() + '" and endDate = "' + temp_end.isoformat() + '"'

        parameters = {'q': query, 'format': 'json', 'diagnostics': 'false',
                      'env': 'store://datatables.org/alltableswithkeys','callback': ''}

        response = requests.get('https://query.yahooapis.com/v1/public/yql', parameters).json()

        results.extend(response['query']["results"]["quote"])

        for item in results:
            del item["Symbol"]
            del item["Open"]
            del item["High"]
            del item["Volume"]
            del item["Low"]
            del item["Close"]

        resultslist.extend(results)

        temp_start = temp_end + timedelta(1)

        if temp_start > end_date:
            break

    return resultslist


class Stock(object):

    def __init__(self, ticker):
        self.ticker = ticker
        self.previous_close = None
        self.price = None
        self.change = None
        self.change_percent = None
        self.name = None
        self.daily_change = None
        self.y_range = None
        self.currency = None

    def get_data(self):
        """ Funtion that get data from YQL
        :param self

        self.ticker        string or list, ex : ['YHOO\n', 'HD\n']

        OUTPUTS :
            resultsdict = Dictionary where key are the tickers from the input and values are dictionaries that contains the
            following keys :
                        'HoldingsGainPercent'
                        'Bid'
                        'HoldingsValue'
                        'BookValue'
                        'AfterHoursChangeRealtime'
                        'TradeDate'
                        'PreviousClose'
                        'BidRealtime'
                        'SharesOwned'
                        'OneyrTargetPrice'
                        'Ask'
                        'AskRealtime'
                        'FiftydayMovingAverage'
                        'DividendShare'
                        'HoldingsGainPercentRealtime'
                        'ChangeFromYearHigh'
                        'DaysRangeRealtime'
                        'EBITDA'
                        'TwoHundreddayMovingAverage'
                        'MoreInfo'
                        'EarningsShare'
                        'OrderBookRealtime'
                        'MarketCapRealtime'
                        'LastTradeWithTime' ===============> format : 4:00pm - <b>28.75</b>
                        'YearLow'
                        'EPSEstimateNextQuarter'
                        'DaysValueChange'
                        'Currency'
                        'YearRange'
                        'EPSEstimateNextYear'
                        'ChangeFromYearLow'
                        'PricePaid'
                        'HoldingsGain'
                        'PEGRatio'
                        'PriceEPSEstimateNextYear'
                        'ErrorIndicationreturnedforsymbolchangedinvalid'
                        'LowLimit'
                        'ChangeFromTwoHundreddayMovingAverage'
                        'PercentChangeFromYearLow'
                        'DaysLow'
                        'StockExchange'
                        'PercentChangeFromTwoHundreddayMovingAverage'
                        'Symbol'
                        'LastTradePriceOnly'
                        'LastTradeRealtimeWithTime'
                        'PercentChangeFromFiftydayMovingAverage'
                        'PriceEPSEstimateCurrentYear'
                        'Change_PercentChange'
                        'Commission'
                        'ChangeinPercent'
                        'AnnualizedGain'
                        'ExDividendDate'
                        'EPSEstimateCurrentYear'
                        'Notes'
                        'DaysValueChangeRealtime'
                        'AverageDailyVolume'
                        'MarketCapitalization'
                        'LastTradeTime'
                        'PriceBook'
                        'Name'
                        'DaysRange'
                        'LastTradeDate'
                        'PriceSales'
                        'ChangeRealtime'
                        'HighLimit'
                        'PERatio'
                        'PercentChange'
                        'ChangeFromFiftydayMovingAverage'
                        'HoldingsGainRealtime'
                        'symbol'
                        'HoldingsValueRealtime'
                        'ShortRatio'
                        'Change'
                        'PERatioRealtime'
                        'DividendPayDate'
                        'ChangePercentRealtime'
                        'TickerTrend'
                        'DaysHigh'
                        'Volume'
                        'PercebtChangeFromYearHigh'
                        'Open'
                        'YearHigh'
                        'DividendYield'
        """

        query = 'select * from yahoo.finance.quotes where symbol in ("' + self.ticker + '")'
        parameters = {'q': query, 'format': 'json', 'diagnostics': 'false',
                      'env': 'store://datatables.org/alltableswithkeys', 'callback': ''}

        response = requests.get('https://query.yahooapis.com/v1/public/yql', parameters).json()
        resultsdict = {self.ticker: response['query']['results']['quote']}

        if resultsdict[self.ticker]["Name"] is None:
            raise ValueError("Invalid Ticker")

        self.previous_close = resultsdict[self.ticker]["PreviousClose"]
        self.price = resultsdict[self.ticker]["LastTradePriceOnly"]
        self.change = str("%.2f" % (float(self.price) - float(self.previous_close)))
        self.change_percent = str('%.2f' % (float(self.change) / float(self.previous_close) * 100))+"%"
        self.name = resultsdict[self.ticker]['Name'].split(",")[0]
        self.daily_change = resultsdict[self.ticker]['Change_PercentChange']
        self.y_range = resultsdict[self.ticker]['YearRange']
        self.currency = resultsdict[self.ticker]["Currency"]

        return [self.name, self.ticker, self.change+"/"+self.change_percent, self.price, self.y_range]

    def hist_dividend(self, start_date, end_date):
        try:
            query = 'select * from yahoo.finance.dividendhistory where symbol = "' + self.ticker + \
                    '" and startDate = "' + start_date + '" and endDate = "' + end_date + '"'

            parameters = {'q': query, 'format': 'json', 'diagnostics': 'false',
                          'env': 'store://datatables.org/alltableswithkeys', 'callback': ''}

            response = requests.get('https://query.yahooapis.com/v1/public/yql', parameters).json()

            resultslist = {self.ticker: response['query']['results']['quote']}[self.ticker]

            for items in resultslist:
                del items["Symbol"]

            return resultslist

        except TypeError:
            return None


if __name__ == '__main__':
    start = date(2016, 6, 25)
    end = date(2017, 2, 2)
    s1 = Stock("BBD-B.TO")
    dividend = s1.hist_dividend(start.isoformat(), end.isoformat())
    exchange_rate = us_to_can(start, end)

    print("Stock data:\n", s1.get_data())
    print("Dividend:\n", dividend)
    print("Exchancge rate:\n", exchange_rate)

