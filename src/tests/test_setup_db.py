import unittest
import os
import sqlite3
import setup_db

class TestSetupDB(unittest.TestCase):
    
    def ptm(self, message):
        print(f'[test_sdb] {message}')
    
    def setUp(self):
        print("\n[test_sdb] Setting up the test...")

        self.test_db_path = "tests/db/traders_test.db"
        os.makedirs(os.path.dirname(self.test_db_path), exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_setup_creates_table(self):
        self.ptm("Running test: test_setup_creates_table")

        setup_db.setup(self.test_db_path)

        with sqlite3.connect(self.test_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            self.ptm(f"Existing tables: {tables}")

            cursor.execute("PRAGMA table_info(traders)")
            columns = cursor.fetchall()

        self.ptm("Actual columns created:")
        for column in columns:
            self.ptm(f'     {column}')

        self.assertEqual(len(columns), 5)
        self.ptm('TEST [1/6]: column length')

        self.assertIn((0, 'id', 'INTEGER', 0, None, 1), columns)
        self.ptm('TEST [2/6]: id')
        
        self.assertIn((1, 'user_id', 'INTEGER', 1, None, 0), columns)
        self.ptm('TEST [3/6]: user_id')

        self.assertIn((2, 'low_grade_balance', 'INTEGER', 1, '0', 0), columns)
        self.ptm('TEST [4/6]: low_grade_balance')

        self.assertIn((3, 'medium_grade_balance', 'INTEGER', 1, '0', 0), columns)
        self.ptm('TEST [5/6]: medium_grade_balance')

        self.assertIn((4, 'high_grade_balance', 'INTEGER', 1, '0', 0), columns)
        self.ptm('TEST [6/6]: high_grade_balance')

        self.ptm('Passed all test_setup_creates_table tests.')
