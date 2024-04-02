"""Unit tests for module sssm"""
# pylint: disable=E0401
import datetime
import unittest

from sssm import StockMarket, Stock, Trade


class StockMarketTest(unittest.TestCase):
    """Unit tests for the StockMarket class."""

    def setUp(self):
        """Creates a StockMarket instance with sample stocks for testing."""
        self.market = StockMarket()
        self.market.add_stock(Stock("TEA", "Common", 0.0, 100))
        self.market.add_stock(Stock("POP", "Common", 8, 100))
        self.market.add_stock(Stock("ALE", "Common", 23, 60))
        self.market.add_stock(Stock("GIN", "Preferred", 8, 100))
        self.market.add_stock(Stock("JOE", "Common", 23, 250))

    def test_dividend_yield_common_stock_positive_price(self):
        """Tests dividend yield calculation for common stock with positive price."""
        price = 160.50
        expected_yield = self.market.stocks["TEA"].last_dividend / price
        actual_yield = self.market.stocks["TEA"].calculate_dividend_yield(price)
        self.assertEqual(expected_yield, actual_yield)

    def test_dividend_yield_common_stock_zero_price(self):
        """Tests dividend yield calculation for common stock with zero price (raises ValueError)."""
        price = 0.0
        with self.assertRaises(ValueError):
            self.market.stocks["TEA"].calculate_dividend_yield(price)

    def test_dividend_yield_preferred_stock_positive_price(self):
        """Tests dividend yield calculation for preferred stock with positive price."""
        price = 87.30
        expected_yield = (self.market.stocks["GIN"].last_dividend / self.market.stocks["GIN"]
                          .par_value)
        actual_yield = self.market.stocks["GIN"].calculate_dividend_yield(price)

        self.assertEqual(expected_yield, actual_yield)

    def test_pe_ratio_common_stock_positive_price(self):
        """Tests P/E ratio calculation for common stock with positive dividend and price."""
        price = 87.30
        expected_pe_ratio = price / self.market.stocks["POP"].last_dividend
        actual_pe_ratio = self.market.stocks["POP"].calculate_pe_ratio(price)
        self.assertEqual(expected_pe_ratio, actual_pe_ratio)

    def test_pe_ratio_common_stock_zero_dividend(self):
        """Tests P/E ratio calculation for common stock with zero dividend (raises ValueError)."""
        price = 160.50
        with self.assertRaises(ValueError):
            self.market.stocks["TEA"].calculate_pe_ratio(price)

    def test_pe_ratio_preferred_stock(self):
        """Tests P/E ratio calculation for preferred stock (raises ValueError)."""
        price = 87.30
        with self.assertRaises(ValueError):
            self.market.stocks["GIN"].calculate_pe_ratio(price)

    def test_record_trade_valid_trade(self):
        """Tests recording a valid trade."""
        time_stamp = datetime.datetime.now()
        symbol = "TEA"
        quantity = 100
        buy_sell = "Buy"
        price = 170.00
        trade = Trade(time_stamp, symbol, quantity, buy_sell, price)
        self.market.record_trade(trade)

        # Check if the trade is present in the market's trade list
        found_trade = False
        for a_trade in self.market.trades:
            if a_trade == trade:  # Compare trade objects for equality
                found_trade = True
                break
        self.assertTrue(found_trade)

    def test_record_trade_past_15_minutes(self):
        """Tests recording a trade older than 15 minutes (not recorded)."""
        time_stamp = datetime.datetime.now() - datetime.timedelta(minutes=20)  # 20 minutes ago
        symbol = "TEA"
        quantity = 50
        buy_sell = "Sell"
        price = 165.25
        trade = Trade(time_stamp, symbol, quantity, buy_sell, price)
        self.market.record_trade(trade)

        # Check if the trade is not present in the market's trade list
        found_trade = False
        for a_trade in self.market.trades:
            if a_trade == trade:
                found_trade = True
                break
        self.assertFalse(found_trade)

    def test_volume_weighted_stock_price_no_trades(self):
        """Tests volume-weighted stock price calculation with no trades."""
        symbol = "TEA"
        with self.assertRaises(ValueError):
            self.market.calculate_volume_weighted_stock_price(symbol)

    def test_volume_weighted_stock_price_past_trades(self):
        """Tests volume-weighted stock price calculation with past trades."""
        time_stamp = datetime.datetime.now() - datetime.timedelta(minutes=10)
        self.market.record_trade(Trade(time_stamp, "TEA", 100, "Buy",
                                       172.50))
        time_stamp = datetime.datetime.now() - datetime.timedelta(minutes=5)
        self.market.record_trade(Trade(time_stamp, "TEA", 50, "Sell",
                                       168.75))

        expected_price = (100 * 172.50 + 50 * 168.75) / (100 + 50)
        actual_price = self.market.calculate_volume_weighted_stock_price("TEA")
        self.assertEqual(expected_price, actual_price)


if __name__ == '__main__':
    unittest.main()
