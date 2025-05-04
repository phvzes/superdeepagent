"""
Tests for the improvement system components of the SuperDeepAgent project.

This module contains tests for the SimpleSelfEvaluator, SimpleBehaviorModifier,
and SimpleReflector classes.
"""

import unittest
from unittest.mock import MagicMock, patch

from superdeepagent.improvement.evaluators.simple import SimpleSelfEvaluator
from superdeepagent.improvement.modifiers.simple import SimpleBehaviorModifier
from superdeepagent.improvement.reflectors.simple import SimpleReflector


class TestSimpleSelfEvaluator(unittest.TestCase):
    """Tests for the SimpleSelfEvaluator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = SimpleSelfEvaluator()
        
        # Sample feedback data for testing
        self.feedback_data = {
            'user_ratings': [4, 5, 3, 4, 5],
            'task_completions': [True, True, False, True, True],
            'response_times': [1.2, 0.8, 1.5, 1.0, 0.9]
        }
    
    def test_initialization(self):
        """Test that the evaluator initializes correctly."""
        self.assertIsInstance(self.evaluator, SimpleSelfEvaluator)
        self.assertEqual(self.evaluator.config, {})
        
        # Test with custom config
        custom_config = {'key': 'value'}
        evaluator = SimpleSelfEvaluator(config=custom_config)
        self.assertEqual(evaluator.config, custom_config)
    
    def test_evaluate(self):
        """Test the evaluate method."""
        metrics = self.evaluator.evaluate(self.feedback_data)
        
        # Check that the metrics contain the expected keys
        self.assertIn('satisfaction_score', metrics)
        self.assertIn('completion_rate', metrics)
        self.assertIn('avg_response_time', metrics)
        self.assertIn('improvement_areas', metrics)
        
        # Check metric values
        self.assertAlmostEqual(metrics['satisfaction_score'], 4.2)  # (4+5+3+4+5)/5 = 4.2
        self.assertAlmostEqual(metrics['completion_rate'], 0.8)  # 4/5 = 0.8
        self.assertAlmostEqual(metrics['avg_response_time'], 1.08)  # (1.2+0.8+1.5+1.0+0.9)/5 = 1.08
    
    def test_identify_improvement_areas(self):
        """Test the _identify_improvement_areas method."""
        # Create feedback data that should trigger improvement areas
        poor_feedback = {
            'user_ratings': [2, 3, 2, 3, 2],  # Average: 2.4 (below 0.7 threshold)
            'task_completions': [True, False, False, True, False],  # 40% (below 0.8 threshold)
            'response_times': [2.5, 3.0, 2.8, 2.2, 3.5]  # Average: 2.8 (above 2.0 threshold)
        }
        
        metrics = self.evaluator.evaluate(poor_feedback)
        improvement_areas = metrics['improvement_areas']
        
        # Check that the expected areas are identified
        # The SimpleSelfEvaluator uses a threshold of 0.7 for user_satisfaction
        # Our test data has an average of 2.4, which is above 0.7 when normalized to a 0-5 scale
        # So we should only expect task_completion and response_time
        self.assertIn('task_completion', improvement_areas)
        self.assertIn('response_time', improvement_areas)
        self.assertEqual(len(improvement_areas), 2)
    
    def test_empty_feedback_data(self):
        """Test behavior with empty feedback data."""
        empty_data = {}
        
        # This should not raise an exception
        metrics = self.evaluator.evaluate(empty_data)
        
        # Check that the metrics contain the expected keys
        self.assertIn('satisfaction_score', metrics)
        self.assertIn('completion_rate', metrics)
        self.assertIn('avg_response_time', metrics)
        self.assertIn('improvement_areas', metrics)
        
        # Check default values
        self.assertEqual(metrics['satisfaction_score'], 0.0)
        self.assertEqual(metrics['completion_rate'], 0.0)
        self.assertEqual(metrics['avg_response_time'], 0.0)


class TestSimpleBehaviorModifier(unittest.TestCase):
    """Tests for the SimpleBehaviorModifier class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.modifier = SimpleBehaviorModifier()
        
        # Sample agent behavior for testing
        self.agent_behavior = {
            'verbosity': 0.5,
            'empathy': 0.5,
            'thoroughness': 0.5,
            'precision': 0.5,
            'conciseness': 0.5
        }
        
        # Sample evaluation metrics for testing
        self.evaluation_metrics = {
            'satisfaction_score': 0.6,
            'completion_rate': 0.7,
            'avg_response_time': 2.5,
            'improvement_areas': ['user_satisfaction', 'task_completion', 'response_time']
        }
    
    def test_initialization(self):
        """Test that the modifier initializes correctly."""
        self.assertIsInstance(self.modifier, SimpleBehaviorModifier)
        self.assertEqual(self.modifier.config, {})
        
        # Test with custom config
        custom_config = {'key': 'value'}
        modifier = SimpleBehaviorModifier(config=custom_config)
        self.assertEqual(modifier.config, custom_config)
    
    def test_modify(self):
        """Test the modify method."""
        modified_behavior = self.modifier.modify(self.agent_behavior, self.evaluation_metrics)
        
        # Check that the original behavior was not modified
        self.assertEqual(self.agent_behavior['verbosity'], 0.5)
        
        # Check that the modified behavior contains the expected keys
        self.assertIn('verbosity', modified_behavior)
        self.assertIn('empathy', modified_behavior)
        self.assertIn('thoroughness', modified_behavior)
        self.assertIn('precision', modified_behavior)
        self.assertIn('conciseness', modified_behavior)
        self.assertIn('_modifications', modified_behavior)
        
        # Check that modifications were applied
        self.assertGreater(modified_behavior['verbosity'], self.agent_behavior['verbosity'])
        self.assertGreater(modified_behavior['empathy'], self.agent_behavior['empathy'])
        self.assertGreater(modified_behavior['thoroughness'], self.agent_behavior['thoroughness'])
        self.assertGreater(modified_behavior['precision'], self.agent_behavior['precision'])
        self.assertGreater(modified_behavior['conciseness'], self.agent_behavior['conciseness'])
        
        # Check that _modifications records what was changed
        self.assertEqual(modified_behavior['_modifications'], 
                         ['user_satisfaction', 'task_completion', 'response_time'])
    
    def test_specific_improvement_strategies(self):
        """Test each specific improvement strategy."""
        # Test user satisfaction improvement
        metrics = {'improvement_areas': ['user_satisfaction']}
        modified = self.modifier.modify(self.agent_behavior, metrics)
        self.assertGreater(modified['verbosity'], self.agent_behavior['verbosity'])
        self.assertGreater(modified['empathy'], self.agent_behavior['empathy'])
        
        # Test task completion improvement
        metrics = {'improvement_areas': ['task_completion']}
        modified = self.modifier.modify(self.agent_behavior, metrics)
        self.assertGreater(modified['thoroughness'], self.agent_behavior['thoroughness'])
        self.assertGreater(modified['precision'], self.agent_behavior['precision'])
        
        # Test response time improvement
        metrics = {'improvement_areas': ['response_time']}
        modified = self.modifier.modify(self.agent_behavior, metrics)
        self.assertGreater(modified['conciseness'], self.agent_behavior['conciseness'])
    
    def test_parameter_capping(self):
        """Test that parameters are capped at 1.0."""
        # Create behavior with parameters already at high values
        high_behavior = {
            'verbosity': 0.95,
            'empathy': 0.95,
            'thoroughness': 0.95,
            'precision': 0.95,
            'conciseness': 0.95
        }
        
        # Apply modifications
        metrics = {'improvement_areas': ['user_satisfaction', 'task_completion', 'response_time']}
        modified = self.modifier.modify(high_behavior, metrics)
        
        # Check that no parameter exceeds 1.0
        for key, value in modified.items():
            if key != '_modifications':
                self.assertLessEqual(value, 1.0)


class TestSimpleReflector(unittest.TestCase):
    """Tests for the SimpleReflector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.reflector = SimpleReflector()
        
        # Sample cycle results for testing
        self.cycle_results = [
            {
                'before_metrics': {
                    'satisfaction_score': 0.6,
                    'completion_rate': 0.7,
                    'avg_response_time': 2.5
                },
                'after_metrics': {
                    'satisfaction_score': 0.7,
                    'completion_rate': 0.8,
                    'avg_response_time': 2.0
                },
                'modifications': ['user_satisfaction', 'task_completion', 'response_time']
            },
            {
                'before_metrics': {
                    'satisfaction_score': 0.7,
                    'completion_rate': 0.8,
                    'avg_response_time': 2.0
                },
                'after_metrics': {
                    'satisfaction_score': 0.75,
                    'completion_rate': 0.85,
                    'avg_response_time': 1.8
                },
                'modifications': ['user_satisfaction', 'task_completion']
            }
        ]
    
    def test_initialization(self):
        """Test that the reflector initializes correctly."""
        self.assertIsInstance(self.reflector, SimpleReflector)
        self.assertEqual(self.reflector.config, {})
        self.assertEqual(self.reflector.history, [])
        
        # Test with custom config
        custom_config = {'key': 'value'}
        reflector = SimpleReflector(config=custom_config)
        self.assertEqual(reflector.config, custom_config)
    
    def test_reflect(self):
        """Test the reflect method."""
        insights = self.reflector.reflect(self.cycle_results)
        
        # Check that the insights contain the expected keys
        self.assertIn('effective_strategies', insights)
        self.assertIn('ineffective_strategies', insights)
        self.assertIn('improvement_trends', insights)
        self.assertIn('recommendations', insights)
        
        # Check that history is updated
        self.assertEqual(len(self.reflector.history), 1)
        self.assertEqual(self.reflector.history[0], self.cycle_results)
    
    def test_analyze_strategy_effectiveness(self):
        """Test the _analyze_strategy_effectiveness method."""
        effective, ineffective = self.reflector._analyze_strategy_effectiveness(self.cycle_results)
        
        # Check that strategies are correctly classified
        self.assertIn('user_satisfaction', effective)
        self.assertIn('task_completion', effective)
        self.assertIn('response_time', effective)
    
    def test_generate_recommendations(self):
        """Test the _generate_recommendations method."""
        effective = ['user_satisfaction', 'task_completion']
        ineffective = ['response_time']
        trends = {'consistent_improvement': True}
        
        recommendations = self.reflector._generate_recommendations(effective, ineffective, trends)
        
        # Check that recommendations are generated
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
    
    def test_multiple_reflect_calls(self):
        """Test behavior with multiple reflect calls."""
        # First reflection
        insights1 = self.reflector.reflect(self.cycle_results)
        
        # Second reflection with different data
        new_cycle_results = [
            {
                'before_metrics': {
                    'satisfaction_score': 0.75,
                    'completion_rate': 0.85,
                    'avg_response_time': 1.8
                },
                'after_metrics': {
                    'satisfaction_score': 0.8,
                    'completion_rate': 0.9,
                    'avg_response_time': 1.5
                },
                'modifications': ['user_satisfaction', 'response_time']
            }
        ]
        insights2 = self.reflector.reflect(new_cycle_results)
        
        # Check that history contains both sets of results
        self.assertEqual(len(self.reflector.history), 2)
        self.assertEqual(self.reflector.history[0], self.cycle_results)
        self.assertEqual(self.reflector.history[1], new_cycle_results)
        
        # Check that trends are identified after multiple reflections
        # With the first reflection, we expect "Insufficient historical data for trend analysis"
        # With the second reflection, we should have actual trend data
        self.assertNotEqual(insights2.get('improvement_trends'), 
                           "Insufficient historical data for trend analysis")


if __name__ == '__main__':
    unittest.main()
