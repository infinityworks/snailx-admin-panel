import unittest
import xmlrunner
import sys
from tests import test_login
from tests import test_session_persistence
from tests import test_rounds
from tests import test_rounds_races
from tests import test_logout
from tests import test_add_round
from tests import test_add_snail
from tests import test_add_race
from tests import test_results
from tests import test_add_trainer

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
suite.addTests(loader.loadTestsFromModule(test_add_snail))
suite.addTests(loader.loadTestsFromModule(test_add_trainer))

# initialize a runner, pass it your suite and run it
runner = xmlrunner.XMLTestRunner(verbosity=3, output='test-reports/unittest')

ret = not runner.run(suite).wasSuccessful()
sys.exit(ret)
