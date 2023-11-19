import os
import sys
import unittest
from logger import Logger

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from test_db import TestDb
from test_setup_db import TestSetupDB
from test_trader import TestTrader

logger: Logger = Logger('[unittest]')

def suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestSetupDB))
    logger.info('Added TestSetupDB to queue')

    test_suite.addTest(unittest.makeSuite(TestTrader))
    logger.info('Added TestTrader to queue')

    test_suite.addTest(unittest.makeSuite(TestDb))
    logger.info('Added TestDb to queue')

    return test_suite

def start(force_start: bool = False):
    all_tests_suite = suite()
    logger.important('Starting test queue')
    
    result = unittest.TextTestRunner().run(all_tests_suite)

    if not result.wasSuccessful():
        if not force_start: logger.error('\n\nTest(s) failed, not starting bot.\nTo force start the bot, pass in `force_start=True`'); sys.exit(1)
        if force_start: logger.error('\n\nTest(s) failed, force_start parameter is present.')

if __name__ == '__main__':
    start()
