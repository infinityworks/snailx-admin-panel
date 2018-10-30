import unittest
from tests import (test_login, test_session_persistence, test_rounds, 
                   test_rounds_races, test_logout, test_add_round, 
                   test_add_race, test_results)
import xmlrunner
import sys

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_session_persistence))
suite.addTests(loader.loadTestsFromModule(test_login))
suite.addTests(loader.loadTestsFromModule(test_logout))
suite.addTests(loader.loadTestsFromModule(test_rounds))
suite.addTests(loader.loadTestsFromModule(test_rounds_races))
suite.addTests(loader.loadTestsFromModule(test_results))
suite.addTests(loader.loadTestsFromModule(test_add_race))
suite.addTests(loader.loadTestsFromModule(test_add_round))
suite.addTests(loader.loadTestsFromModule(test_add_round))

# initialize a runner, pass it your suite and run it
runner = xmlrunner.XMLTestRunner(verbosity=3, output='test-reports/unittest')

ret = not runner.run(suite).wasSuccessful()
sys.exit(ret)
