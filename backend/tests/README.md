# SuperDeepAgent Tests

This directory contains test cases for the SuperDeepAgent project components.

## Test Files

- `test_feedback.py`: Tests for the feedback system components (UserFeedbackCollector, SystemMetricsCollector, PerformanceEvaluator, ThresholdTrigger)
- `test_improvement.py`: Tests for the improvement system components (SimpleSelfEvaluator, SimpleBehaviorModifier, SimpleReflector)
- `test_metalearning.py`: Tests for the metalearning system components (SimpleKnowledgeAbstracter, SimpleKnowledgeTransferer, SimpleLearningAdapter)
- `test_phase3_integration.py`: Tests for the Phase3Integration class
- `test_phase3_manager.py`: Tests for the Phase3Manager class

## Running Tests

You can run all tests using the provided `run_tests.py` script:

```bash
./run_tests.py
```

Or you can use pytest directly:

```bash
# Run all tests
pytest

# Run a specific test file
pytest test_feedback.py

# Run a specific test class
pytest test_feedback.py::TestUserFeedbackCollector

# Run a specific test method
pytest test_feedback.py::TestUserFeedbackCollector::test_collect
```

## Test Coverage

To run tests with coverage reporting:

```bash
# Install coverage if not already installed
pip install coverage

# Run tests with coverage
coverage run -m pytest

# Generate coverage report
coverage report
```
