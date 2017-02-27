from datetime import datetime, date
from Basics.stock import Stock


class Portfolio(object):

    def __init__(self, name='DefaultPortfolio', cash=0.0, comments="", creation_date=datetime.now(),
                 last_mod=datetime.now()):
        """
        Default constructor
        :param name: name of the portfolio (default value is 'default_portfolio')
        :param cash: initial cash amount for the portfolio (default value is 0.0)
        :return: a portfolio instance
        """
        self.__name = None
        self.__cash = None
        self.__creation_date = creation_date
        self.__last_mod = last_mod
        self.__transactions = None
        self.__comments = None

        self.name = name
        self.cash = cash
        self.transactions = {}
        self.comments = comments

    # Properties created for read-only attributes (creation_date and last_modification_date)
    @property
    def creation_date(self):
        return self.__creation_date

    @property
    def last_mod(self):
        return self.__last_mod

    # Other properties
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        if isinstance(new_name, str):
            self.__name = new_name
        else:
            raise TypeError("The portfolio's name must be a string.")

    @property
    def cash(self):
        return self.__cash

    @cash.setter
    def cash(self, new_cash: float):
        if isinstance(new_cash, float):
            self.__cash = round(new_cash, 2)
        else:
            raise TypeError("Cash must be a float number.")

    def cash_deposit(self, amount):
        if isinstance(amount, float):
            self.__cash += round(amount, 2)

    def cash_withdrawal(self, amount):
        """
        :param amount: (float) Amount of cash to withdraw from the portfolio's cash
        :return: true if the cash is withdrawn (sufficient cash amount in the portfolio) or false otherwise
        """
        if isinstance(amount, float) and self.__cash-amount >= 0:
            self.__cash -= round(amount, 2)
            return True
        else:
            return False

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, new_comment):
        if isinstance(new_comment, str):
            self.__comments = new_comment
        else:
            raise TypeError('Comments must be a string.')

    def compute_shares(self, symbol, at_date=date.today()):
        shares = 0

        try:
            for transaction in self.transactions[symbol]:

                if transaction.transaction_type == 'SELL' and at_date >= transaction.t_date:
                    shares -= transaction.quantity

                elif transaction.transaction_type == 'BUY' and at_date >= transaction.t_date:
                    shares += transaction.quantity

        except KeyError:  # In the case you buy a stock for the first time
            pass

        return shares

    def add_transaction(self, transaction):
        if not isinstance(transaction, Transaction):
            return False

        else:
            shares = self.compute_shares(transaction.stock, transaction.t_date)
            cost = transaction.cost()

            if str.upper(transaction.transaction_type) == 'BUY' and cost + self.cash < 0:
                problem = 'Manque de Fonds'
                return False, problem

            elif str.upper(transaction.transaction_type) == 'SELL' and shares - transaction.quantity < 0:
                problem = 'Vous ne possédez pas les actions que vous voulez vendre.'
                return False, problem

            else:
                print(self.transactions)
                self.cash += cost
                if transaction.stock in self.transactions.keys():
                    self.transactions[transaction.stock].append(transaction)
                else:
                    self.transactions[transaction.stock] = [transaction]

            self.cash = round(self.cash, 2)
            return True


class Transaction(object):

    def __init__(self, stock, t_date=datetime.today(), quantity=0, transaction_type="BUY", price=0.00,
                 commission=00.00, comments=""):

        self.__stock = None
        self.__t_date = None
        self.__transaction_type = None
        self.__quantity = None
        self.__price = None
        self.__commission = None
        self.__comments = None

        self.stock = stock
        self.t_date = t_date
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.price = price
        self.commission = commission
        self.comments = comments

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, stock):
        if isinstance(stock, str):
            self.__stock = stock
        else:
            raise TypeError

    @property
    def t_date(self):
        return self.__t_date

    @t_date.setter
    def t_date(self, t_date):
        if isinstance(t_date, date):
            self.__t_date = t_date
        else:
            raise TypeError('Date must be a datetime.date object')

    @property
    def transaction_type(self):
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, transaction_type):
        if str.upper(transaction_type) == "BUY" or str.upper(transaction_type) == "SELL":
            self.__transaction_type = transaction_type
        else:
            raise NameError("Transaction type must be 'BUY' or 'SELL'")

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity):
        if isinstance(quantity, int):
            self.__quantity = quantity
        else:
            raise TypeError("Quantity must be a integer")

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        if isinstance(price, float):
            self.__price = price
        else:
            raise TypeError("Price must be a float number. Ex. 9.33")

    @property
    def commission(self):
        return self.__commission

    @commission.setter
    def commission(self, commission):
        if isinstance(commission, float):
            self.__commission = commission
        else:
            raise TypeError("COmmission must be a float number. Ex. 9.00")

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, comments):
        if isinstance(comments, str):
            self.__comments = comments
        else:
            raise TypeError('Comment must be a string')

    def cost(self):
        cost = self.price*self.quantity

        if self.transaction_type == 'BUY':
            cost = -cost - self.commission

        if self.transaction_type == 'SELL':
            cost -= self.commission

        return round(cost, 2)


if __name__ == '__main__':
    symbol = "YHOO"

    t1 = Transaction(symbol, t_date=date(2016, 1, 2), quantity=18, transaction_type="BUY", price=34.59, commission=6.0,
                     comments="Best decision I've ever made!")

    t2 = Transaction(symbol, t_date=date(2016, 1, 10), quantity=12, transaction_type="SELL", price=50.20,
                     commission=6.0, comments="Best decision I've ever made!")

    t3 = Transaction(symbol, t_date=date(2016, 1, 15), quantity=8, transaction_type="SELL", price=34.59, commission=6.0,
                     comments="Best decision I've ever made!")

    t4 = Transaction(symbol, t_date=date(2016, 1, 25), quantity=29, transaction_type="BUY", price=34.59, commission=6.0,
                     comments="Best decision I've ever made!")

    t5 = Transaction("HD", t_date=date(2016, 1, 25), quantity=25, transaction_type="BUY", price=34.59, commission=6.0,
                     comments="Best decision I've ever made!")

    transaction_list = [t1, t2, t3, t4, t5]

    p1 = Portfolio('Portfolio', 2000.0, comments="This is the best portfolio")
    p1.cash_deposit(20000000)
    print(p1.cash)

    for transaction in transaction_list:
        success = p1.add_transaction(transaction)
        print(transaction.transaction_type, transaction.quantity, transaction.stock, 'Success :', success)

    on_date = date(2016, 1, 24)
    print(p1.compute_shares(symbol, on_date), "Shares on :", on_date)

    stock1 = Stock(symbol)
    stock1.get_data()

    value = float(stock1.price) * p1.compute_shares(stock1.ticker)

    print(value)