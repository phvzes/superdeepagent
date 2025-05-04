#!/usr/bin/env python3
"""
Test runner for the SuperDeepAgent project.

This script runs all the test cases for the SuperDeepAgent project components.
"""

import unittest
import sys
import os

# Add the parent directory to the path so that imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all test modules
from tests.test_feedback import *
from tests.test_improvement import *
from tests.test_metalearning import *
from tests.test_phase3_integration import *
from tests.test_phase3_manager import *


if __name__ == '__main__':
    # Create a test suite with all tests
    test_suite = unittest.defaultTestLoader.discover('tests', pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())
