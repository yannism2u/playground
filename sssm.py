"""
Super Simple Stock Market
"""
# pylint: disable=R0903, R0913, R1705, W0703
import datetime
from math import prod


class Stock:
    """Represents a stock in the market."""

    def __init__(self, symbol, stock_type, last_dividend, par_value=None):
        """
        Args:
            symbol (str): The stock symbol.
            stock_type (str): "Common" or "Preferred" stock type.
            last_dividend (float): The last dividend paid per share.
            par_value (float, optional): The par value for preferred stocks. Defaults to None.
        """
        self.symbol = symbol
        self.type = stock_type
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.price = None

    def calculate_dividend_yield(self, price):
        """
        Calculates the dividend yield for the stock.

        Args:
            price (float): The current price of the stock.

        Returns:
            float: The dividend yield, or raises a ValueError if price is zero
                for common stock or par value is missing/zero for preferred stock.
        """
        if self.type == "Common":
            if price > 0:
                return self.last_dividend / price
            else:
                raise ValueError("Price cannot be zero for dividend yield calculation.")
        else:
            if self.par_value > 0:
                return self.last_dividend / self.par_value
            else:
                raise ValueError("Par value required "
                                 "for preferred stock dividend yield calculation.")

    def calculate_pe_ratio(self, price):
        """
        Calculates the price-to-earnings (P/E) ratio for the stock.

        Args:
            price (float): The current price of the stock.

        Returns:
            float: The P/E ratio, or raises a ValueError if the stock type is
                preferred or if the last dividend is zero for common stock.
        """
        if self.type == "Common" and self.last_dividend > 0:
            return price / self.last_dividend
        else:
            raise ValueError("Cannot calculate P/E ratio for preferred stock "
                             "or common stock with zero dividend.")


class Trade:
    """Represents a trade for a particular stock."""

    def __init__(self, timestamp,  symbol, quantity, buy_sell, price):
        """
        Args:
            timestamp (datetime.datetime): The timestamp of the trade.
            symbol (str): The symbol of the stock traded.
            quantity (int): The quantity of shares traded.
            buy_sell (str): "Buy" or "Sell" indicator.
            price (float): The price per share at which the trade occurred.
        """
        self.timestamp = timestamp
        self.symbol = symbol
        self.quantity = quantity
        self.buy_sell = buy_sell
        self.price = price


class StockMarket:
    """Represents a simulated stock market."""

    def __init__(self):
        """
        Initializes the stock market with empty stock and trade lists.
        """
        self.stocks = {}  # Dictionary to store stocks (symbol as key)
        self.trades = []  # List to store past 15 minutes of trades

    def add_stock(self, stock):
        """
        Adds a stock to the market.

        Args:
            stock (Stock): The stock object to add.
        """
        self.stocks[stock.symbol] = stock

    def record_trade(self, trade):
        """
        Records a trade in the market, keeping only the past two hours of trades.

        Args:
            trade (Trade): The trade object to record.
        """
        self.trades.append(trade)
        # Keep only the past 15 minutes of trades (adjustable time window)
        cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
        self.trades = [t for t in self.trades if t.timestamp >= cutoff_time]

    def calculate_volume_weighted_stock_price(self, symbol):
        """
        Calculates the volume-weighted stock price based on trades in the past 15 minutes.

        Args:
            symbol (str): The symbol of the stock for which to calculate the price.

        Returns:
            float: The volume-weighted stock price, or None if the stock is not found or
                there are no trades for the stock in the past 15 minutes.
        """
        if symbol not in self.stocks:
            raise ValueError(f"Stock with symbol '{symbol}' not found.")

        total_quantity = 0
        total_price_quantity = 0
        for trade in self.trades:
            if trade.symbol == symbol:
                total_quantity += trade.quantity
                total_price_quantity += trade.price * trade.quantity

        if total_quantity > 0:
            return total_price_quantity / total_quantity
        else:
            raise ValueError

    def calculate_gbce_all_share_index(self):
        """
        Calculates the GBCE All Share Index using the geometric mean of prices for all stocks.

        Returns:
            float: The GBCE All Share Index, or raises a ValueError if there are no stocks
                added to the market or no stock prices are available.
        """
        if not self.stocks:
            raise ValueError("No stocks added to the market.")

        prices = [stock.price for stock in self.stocks.values() if stock.price is not None]
        if not prices:
            raise ValueError("No stock prices available for index calculation.")

        return prod(prices) ** (1/len(prices))


if __name__ == '__main__':
    # Example usage
    market = StockMarket()

    # Add some stocks (replace with actual data)
    tea = Stock("TEA", "Common", 0.0, 100)
    pop = Stock("POP", "Common", 8, 100)
    ale = Stock("ALE", "Common", 23, 60)
    gin = Stock("GIN", "Preferred", 8, 100)
    joe = Stock("JOE", "Common", 23, 250)
    market.add_stock(tea)
    market.add_stock(pop)
    market.add_stock(ale)
    market.add_stock(gin)
    market.add_stock(joe)

    # Example trade recording
    timestamp = datetime.datetime.now()
    market.record_trade(Trade(timestamp, "TEA", 100, "Buy", 160.50))
    market.record_trade(Trade(timestamp, "POP", 50, "Sell", 87.30))

    # Example calculations (replace symbol and price as needed)
    symbol = "TEA"
    price = 170.00

    dividend_yield = market.stocks[symbol].calculate_dividend_yield(price)
    pe_ratio = market.stocks[symbol].calculate_pe_ratio

    tea.price = market.calculate_volume_weighted_stock_price("TEA")
    pop.price = market.calculate_volume_weighted_stock_price("POP")
    gbce_all_share_index = market.calculate_gbce_all_share_index()

