import os
import sqlite3
import unittest
from typing import Union

import helpers.db as db
import setup_db
from econ_types.trader import Trader


class TestDb(unittest.TestCase):

    def ptm(self, message):
        print(f'[ test_db] {message}')

    def setUp(self):
        print('\n') # dumbass dot
        self.ptm('Setting up the test...')

        self.test_db_path = "tests/db/traders_test.db"
        os.makedirs(os.path.dirname(self.test_db_path), exist_ok=True)

        setup_db.setup(os.path.abspath(self.test_db_path), False)

        self.conn = sqlite3.connect(os.path.abspath(self.test_db_path))

        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='traders'")
        table_exists = cursor.fetchone()

        if table_exists:
            cursor.execute("DROP TABLE traders")
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS traders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                low_grade_balance INTEGER NOT NULL DEFAULT 0,
                medium_grade_balance INTEGER NOT NULL DEFAULT 0,
                high_grade_balance INTEGER NOT NULL DEFAULT 0
            )
            """
            )

            trader = Trader(user_id=1, bal_low_grade=10, bal_medium_grade=20, bal_high_grade=30)
            db.create_trader(trader, self.conn)

            self.conn.commit()
        
        trader = Trader(user_id=1, bal_low_grade=10, bal_medium_grade=20, bal_high_grade=30)
        db.create_trader(trader, self.conn)

        cursor.close()

    def tearDown(self):
        if self.conn:
            self.conn.close()

        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_create_trader(self):
        self.ptm('Running test: test_create_trader')

        retrieved_trader = db.get_trader(1, self.conn)

        self.assertEqual(retrieved_trader.user_id, 1)
        self.ptm('TEST [1/4]: user_id')

        self.assertEqual(retrieved_trader.low_grade_balance, 10)
        self.ptm('TEST [2/4]: low_grade_balance')

        self.assertEqual(retrieved_trader.medium_grade_balance, 20)
        self.ptm('TEST [3/4]: medium_grade_balance')

        self.assertEqual(retrieved_trader.high_grade_balance, 30)
        self.ptm('TEST [4/4]: high_grade_balance')

        self.ptm('Passed all test_create_trader tests.')

    def test_get_trader(self):
        self.ptm('Running test: test_get_trader')

        test_result = db.get_trader(1, self.conn)

        if not type(test_result).__name__ == 'Trader':
            self.fail(
                f"get_trader did not return an object of type `Trader`.\n"
                f"It returned type: {type(test_result)}\n"
                f"type.__name__...: {type(test_result).__name__}")

        self.assertEqual(test_result.user_id, 1)
        self.ptm('TEST [1/4]: user_id')

        self.assertEqual(test_result.low_grade_balance, 10)
        self.ptm('TEST [2/4]: low_grade_balance')

        self.assertEqual(test_result.medium_grade_balance, 20)
        self.ptm('TEST [3/4]: medium_grade_balance')

        self.assertEqual(test_result.high_grade_balance, 30)
        self.ptm('TEST [4/4]: high_grade_balance')

        self.ptm('Passed all test_get_trader tests.')
    
    def test_update_trader(self):
        self.ptm('Running test: test_update_trader')

        test_result = db.update_trader(1, self.conn,
                                       low_grade_balance=111,
                                       medium_grade_balance=222,
                                       high_grade_balance=333)
        
        if test_result is not True:
            self.fail('test_update_trader FAILED, it did not return a bool of True.\n'
                      f'It returned type {type(test_result).__name__}: {test_result}')
        
        self.assertTrue(test_result)
        self.ptm('TEST [1/1]: True received')

        self.ptm('Passed all test_update_trader tests.')

    def test_delete_trader(self):
        self.ptm('Running test: test_delete_trader')

        # verify the trader exists before deleting
        retrieved_trader_before = db.get_trader(1, self.conn)
        self.assertIsNotNone(retrieved_trader_before)
        self.ptm('TEST [1/3]: Trader exists')

        test_result = db.delete_trader(1, self.conn)

        self.assertTrue(test_result)
        self.ptm('TEST [2/3]: Trader deleted')

        # verify that the trader no longer exists after deletion
        retrieved_trader_after = db.get_trader(1, self.conn)
        self.assertFalse(retrieved_trader_after)
        self.ptm('TEST [3/3]: Trader does not exist after deletion')

        self.ptm('Passed all test_delete_trader tests.')
    
    def test_reset_trader_all_balances(self):
        self.ptm('Running test: test_reset_trader_all_balances')

        test_result = db.reset_trader_all_balances(1, self.conn)

        if test_result is not True:
            self.fail('test_reset_trader_all_balances FAILED, it did not return a bool of True.\n'
                      f'It returned type {type(test_result).__name__}: {test_result}')
        
        self.assertTrue(test_result)
        self.ptm('TEST [1/4]: True received')

        test_result_confirm = db.get_trader(1, self.conn)

        self.assertEqual(test_result_confirm.low_grade_balance, 0)
        self.ptm('TEST [2/4]: low_grade_balance is 0')

        self.assertEqual(test_result_confirm.medium_grade_balance, 0)
        self.ptm('TEST [3/4]: medium_grade_balance is 0')

        self.assertEqual(test_result_confirm.high_grade_balance, 0)
        self.ptm('TEST [4/4]: high_grade_balance is 0')

        self.ptm('Passed all test_reset_trader_all_balances tests.')
    
    def test_reset_trader_grade_balance(self):
        self.ptm('Running test: test_reset_trader_grade_balance')

        test_result_low_grade = db.reset_trader_grade_balance(1, 'low_grade_balance', self.conn)
        test_result_medium_grade = db.reset_trader_grade_balance(1, 'medium_grade_balance', self.conn)
        test_result_high_grade = db.reset_trader_grade_balance(1, 'high_grade_balance', self.conn)

        if test_result_low_grade is not True:
            self.fail('test_reset_trader_grade_balance FAILED, it did not return a bool of True.\n'
                      f'It returned type {type(test_result_low_grade).__name__}: {test_result_low_grade}')
        
        elif test_result_medium_grade is not True:
            self.fail('test_reset_trader_grade_balance FAILED, it did not return a bool of True.\n'
                      f'It returned type {type(test_result_medium_grade).__name__}: {test_result_medium_grade}')
        
        elif test_result_high_grade is not True:
            self.fail('test_reset_trader_grade_balance FAILED, it did not return a bool of True.\n'
                      f'It returned type {type(test_result_high_grade).__name__}: {test_result_high_grade}')
        
        self.assertTrue(test_result_low_grade)
        self.ptm('TEST [1/6]: True received from test_result_low_grade')

        self.assertTrue(test_result_medium_grade)
        self.ptm('TEST [2/6]: True received from test_result_medium_grade')

        self.assertTrue(test_result_high_grade)
        self.ptm('TEST [3/6]: True received from test_result_high_grade')

        test_result = db.get_trader(1, self.conn)

        self.assertEqual(test_result.low_grade_balance, 0)
        self.ptm('TEST [4/6]: low_grade_balance is 0')

        self.assertEqual(test_result.medium_grade_balance, 0)
        self.ptm('TEST [4/6]: medium_grade_balance is 0')

        self.assertEqual(test_result.high_grade_balance, 0)
        self.ptm('TEST [4/6]: high_grade_balance is 0')

        self.ptm('Passed all test_reset_trader_grade_balance tests.')

