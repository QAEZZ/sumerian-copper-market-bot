from econ_types.trader import Trader
import unittest

class TestTrader(unittest.TestCase):
    def ptm(self, message):
        print(f'[test_trd] {message}')

    def test_initialization(self):
        print('\n') # dumbass dot 
        self.ptm('Running test: test_initialization')

        trader = Trader(user_id=1, bal_low_grade=10, bal_medium_grade=20, bal_high_grade=30)

        self.assertEqual(trader.user_id, 1)
        self.ptm('TEST [1/4]: user_id')

        self.assertEqual(trader.low_grade_balance, 10)
        self.ptm('TEST [2/4]: low_grade_balance')

        self.assertEqual(trader.medium_grade_balance, 20)
        self.ptm('TEST [3/4]: medium_grade_balance')

        self.assertEqual(trader.high_grade_balance, 30)
        self.ptm('TEST [4/4]: high_grade_balance')

        self.ptm('Passed all test_initialization tests.')

    def test_balance_setters(self):
        print('\n') # dumbass dot
        self.ptm('Running test: test_balance_setters')

        trader = Trader(user_id=1)
        trader.low_grade_balance = 10
        trader.medium_grade_balance = 20
        trader.high_grade_balance = 30

        self.assertEqual(trader.low_grade_balance, 10)
        self.ptm('TEST [1/3]: low_grade_balance')

        self.assertEqual(trader.medium_grade_balance, 20)
        self.ptm('TEST [2/3]: medium_grade_balance')

        self.assertEqual(trader.high_grade_balance, 30)
        self.ptm('TEST [3/3]: high_grade_balance')

        self.ptm('Passed all test_balance_setters tests.')

    def test_string_representation(self):
        print('\n') # dumbass dot 
        self.ptm('Running test: test_string_representation')

        trader = Trader(user_id=1, bal_low_grade=10, bal_medium_grade=20, bal_high_grade=30)

        self.assertEqual(
            str(trader),
            "Trader(user_id=1, low_grade_balance=10, medium_grade_balance=20, high_grade_balance=30)"
        )
        self.ptm('TEST [1/1]: trader balances match')
        self.ptm('Passed all test_string_representation tests.')
