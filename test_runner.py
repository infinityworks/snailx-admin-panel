import unittest
<<<<<<< HEAD
from tests import (test_index, test_login_page)
=======
from tests import (test_index, test_login)
>>>>>>> origin/login-page-test
import xmlrunner
import sys
from tests import test_session_persistence
# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_index))
<<<<<<< HEAD
suite.addTests(loader.loadTestsFromModule(test_login_page))
suite.addTests(loader.loadTestsFromModule(test_session_persistence))
=======
suite.addTests(loader.loadTestsFromModule(test_login))
>>>>>>> origin/login-page-test

# initialize a runner, pass it your suite and run it
# runner = unittest.TextTestRunner(verbosity=3)
runner = xmlrunner.XMLTestRunner(verbosity=3, output='test-reports/unittest')

ret = not runner.run(suite).wasSuccessful()
sys.exit(ret)
