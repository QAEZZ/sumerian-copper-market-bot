import unittest

from econ_types.trader import Trader
from logger import Logger

logger: Logger = Logger('[test_trd]')

class TestTrader(unittest.TestCase):

    def test_initialization(self):
        logger.info('Running test: test_initialization', True)

        trader = Trader(user_id=1, bal_low_grade=10, bal_medium_grade=20, bal_high_grade=30)

        self.assertEqual(trader.user_id, 1)
        logger.success('TEST [1/4]: user_id')

        self.assertEqual(trader.low_grade_balance, 10)
        logger.success('TEST [2/4]: low_grade_balance')

        self.assertEqual(trader.medium_grade_balance, 20)
        logger.success('TEST [3/4]: medium_grade_balance')

        self.assertEqual(trader.high_grade_balance, 30)
        logger.success('TEST [4/4]: high_grade_balance')

        logger.important('Passed all test_initialization tests.')

    def test_balance_setters(self):
        print('\n') # dumbass dot
        logger.info('Running test: test_balance_setters')

        trader = Trader(user_id=1)
        trader.low_grade_balance = 10
        trader.medium_grade_balance = 20
        trader.high_grade_balance = 30

        self.assertEqual(trader.low_grade_balance, 10)
        logger.success('TEST [1/3]: low_grade_balance')

        self.assertEqual(trader.medium_grade_balance, 20)
        logger.success('TEST [2/3]: medium_grade_balance')

        self.assertEqual(trader.high_grade_balance, 30)
        logger.success('TEST [3/3]: high_grade_balance')

        logger.important('Passed all test_balance_setters tests.')

    def test_string_representation(self):
        print('\n') # dumbass dot 
        logger.info('Running test: test_string_representation')

        trader = Trader(user_id=1, bal_low_grade=10, bal_medium_grade=20, bal_high_grade=30)

        self.assertEqual(
            str(trader),
            "Trader(user_id=1, low_grade_balance=10, medium_grade_balance=20, high_grade_balance=30)"
        )
        logger.success('TEST [1/1]: trader balances match')
        logger.important('Passed all test_string_representation tests.')
