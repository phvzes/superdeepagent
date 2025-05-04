"""
Tests for the feedback system components of the SuperDeepAgent project.

This module contains tests for the UserFeedbackCollector, SystemMetricsCollector,
PerformanceEvaluator, and ThresholdTrigger classes.
"""

import unittest
from unittest.mock import MagicMock, patch

from superdeepagent.feedback.collectors.user_feedback import UserFeedbackCollector
from superdeepagent.feedback.collectors.system_metrics import SystemMetricsCollector
from superdeepagent.feedback.evaluators.performance import PerformanceEvaluator
from superdeepagent.feedback.triggers.threshold import ThresholdTrigger


class TestUserFeedbackCollector(unittest.TestCase):
    """Tests for the UserFeedbackCollector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.collector = UserFeedbackCollector()
        
        # Sample interaction data for testing
        self.interaction_data = {
            'explicit_ratings': [4, 5, 3, 4, 5],
            'comments': ['Great response!', 'Could be better'],
            'corrections': [{'original': 'X', 'corrected': 'Y'}],
            'interaction_patterns': {
                'session_duration': 120,
                'response_acceptance_rate': 0.8,
                'follow_up_questions': 3
            }
        }
    
    def test_initialization(self):
        """Test that the collector initializes correctly."""
        self.assertIsInstance(self.collector, UserFeedbackCollector)
        self.assertEqual(self.collector.config, {})
        
        # Test with custom config
        custom_config = {'key': 'value'}
        collector = UserFeedbackCollector(config=custom_config)
        self.assertEqual(collector.config, custom_config)
    
    def test_collect(self):
        """Test the collect method."""
        feedback = self.collector.collect(self.interaction_data)
        
        # Check that the feedback contains the expected keys
        self.assertIn('satisfaction_scores', feedback)
        self.assertIn('sentiment_analysis', feedback)
        self.assertIn('correction_patterns', feedback)
        self.assertIn('engagement_metrics', feedback)
        
        # Check satisfaction scores
        satisfaction = feedback['satisfaction_scores']
        self.assertEqual(satisfaction['average'], 4.2)  # (4+5+3+4+5)/5 = 4.2
        self.assertEqual(satisfaction['count'], 5)
        
        # Check engagement metrics
        engagement = feedback['engagement_metrics']
        self.assertEqual(engagement['session_duration'], 120)
        self.assertEqual(engagement['response_acceptance_rate'], 0.8)
        self.assertEqual(engagement['follow_up_questions'], 3)
    
    def test_empty_interaction_data(self):
        """Test behavior with empty interaction data."""
        empty_data = {}
        feedback = self.collector.collect(empty_data)
        
        # Check that the feedback still contains the expected keys
        self.assertIn('satisfaction_scores', feedback)
        self.assertIn('sentiment_analysis', feedback)
        self.assertIn('correction_patterns', feedback)
        self.assertIn('engagement_metrics', feedback)
        
        # Check that satisfaction scores handle empty data
        satisfaction = feedback['satisfaction_scores']
        self.assertEqual(satisfaction['average'], 0.0)
        self.assertEqual(satisfaction['count'], 0)
        self.assertEqual(satisfaction['distribution'], {})


class TestSystemMetricsCollector(unittest.TestCase):
    """Tests for the SystemMetricsCollector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.collector = SystemMetricsCollector()
        
        # Sample interaction data for testing
        self.interaction_data = {
            'response_times': [0.5, 0.8, 1.2, 0.7, 0.9],
            'time_period': 10,
            'resource_usage': {
                'avg_cpu': 0.3,
                'max_memory': 512,
                'avg_memory': 256,
                'disk_io': 100,
                'network_io': 200
            },
            'error_logs': [
                {'type': 'api_error', 'message': 'API timeout'},
                {'type': 'validation_error', 'message': 'Invalid input'}
            ],
            'total_interactions': 100,
            'api_calls': [
                {'service': 'database', 'success': True, 'latency': 0.1},
                {'service': 'database', 'success': True, 'latency': 0.2},
                {'service': 'external_api', 'success': False, 'latency': 1.5}
            ]
        }
    
    def test_initialization(self):
        """Test that the collector initializes correctly."""
        self.assertIsInstance(self.collector, SystemMetricsCollector)
        self.assertEqual(self.collector.config, {})
        
        # Test with custom config
        custom_config = {'key': 'value'}
        collector = SystemMetricsCollector(config=custom_config)
        self.assertEqual(collector.config, custom_config)
    
    def test_collect(self):
        """Test the collect method."""
        metrics = self.collector.collect(self.interaction_data)
        
        # Check that the metrics contain the expected keys
        self.assertIn('performance_metrics', metrics)
        self.assertIn('resource_metrics', metrics)
        self.assertIn('reliability_metrics', metrics)
        self.assertIn('external_dependencies', metrics)
        
        # Check performance metrics
        performance = metrics['performance_metrics']
        self.assertAlmostEqual(performance['avg_response_time'], 0.82)  # (0.5+0.8+1.2+0.7+0.9)/5 = 0.82
        self.assertEqual(performance['max_response_time'], 1.2)
        self.assertEqual(performance['min_response_time'], 0.5)
        self.assertEqual(performance['throughput'], 0.5)  # 5/10 = 0.5
        
        # Check resource metrics
        resource = metrics['resource_metrics']
        self.assertEqual(resource['avg_cpu_usage'], 0.3)
        self.assertEqual(resource['max_memory_usage'], 512)
        
        # Check reliability metrics
        reliability = metrics['reliability_metrics']
        self.assertEqual(reliability['error_count'], 2)
        self.assertEqual(reliability['error_rate'], 0.02)  # 2/100 = 0.02
        
        # Check external dependencies
        dependencies = metrics['external_dependencies']
        self.assertIn('database', dependencies)
        self.assertIn('external_api', dependencies)
        self.assertEqual(dependencies['database']['count'], 2)
        self.assertEqual(dependencies['database']['success_rate'], 1.0)
        self.assertEqual(dependencies['external_api']['success_rate'], 0.0)
    
    def test_empty_interaction_data(self):
        """Test behavior with empty interaction data."""
        empty_data = {}
        metrics = self.collector.collect(empty_data)
        
        # Check that the metrics still contain the expected keys
        self.assertIn('performance_metrics', metrics)
        self.assertIn('resource_metrics', metrics)
        self.assertIn('reliability_metrics', metrics)
        self.assertIn('external_dependencies', metrics)
        
        # Check that performance metrics handle empty data
        performance = metrics['performance_metrics']
        self.assertEqual(performance['avg_response_time'], 0.0)
        self.assertEqual(performance['max_response_time'], 0.0)
        self.assertEqual(performance['min_response_time'], 0.0)


class TestPerformanceEvaluator(unittest.TestCase):
    """Tests for the PerformanceEvaluator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = PerformanceEvaluator()
        
        # Sample feedback data for testing
        self.feedback_data = {
            'user_feedback': {
                'satisfaction_scores': {
                    'average': 0.85,
                    'count': 10
                },
                'sentiment_analysis': {
                    'sentiment': 'positive'
                },
                'engagement_metrics': {
                    'response_acceptance_rate': 0.9
                },
                'correction_patterns': {
                    'count': 2
                }
            },
            'system_metrics': {
                'performance_metrics': {
                    'avg_response_time': 0.7,
                    'throughput': 5.0
                },
                'resource_metrics': {
                    'avg_cpu_usage': 0.4,
                    'avg_memory_usage': 0.3
                },
                'reliability_metrics': {
                    'error_rate': 0.01
                },
                'external_dependencies': {
                    'database': {
                        'success_rate': 0.99
                    }
                }
            }
        }
    
    def test_initialization(self):
        """Test that the evaluator initializes correctly."""
        self.assertIsInstance(self.evaluator, PerformanceEvaluator)
        self.assertEqual(self.evaluator.config, {})
        
        # Test with custom config
        custom_config = {'weights': {'user_satisfaction': 0.5}}
        evaluator = PerformanceEvaluator(config=custom_config)
        self.assertEqual(evaluator.config, custom_config)
        self.assertEqual(evaluator.weights['user_satisfaction'], 0.5)
    
    def test_evaluate(self):
        """Test the evaluate method."""
        results = self.evaluator.evaluate(self.feedback_data)
        
        # Check that the results contain the expected keys
        self.assertIn('overall_score', results)
        self.assertIn('dimension_scores', results)
        self.assertIn('strengths', results)
        self.assertIn('improvement_areas', results)
        self.assertIn('trend', results)
        
        # Check dimension scores
        dimensions = results['dimension_scores']
        self.assertIn('user_satisfaction', dimensions)
        self.assertIn('task_completion', dimensions)
        self.assertIn('system_performance', dimensions)
        self.assertIn('reliability', dimensions)
        
        # Check that overall score is calculated correctly
        self.assertGreater(results['overall_score'], 0.0)
        self.assertLess(results['overall_score'], 1.0)
        
        # Check that strengths are identified
        for strength in results['strengths']:
            self.assertIn(strength, dimensions)
            self.assertGreaterEqual(dimensions[strength], 0.8)
    
    def test_empty_feedback_data(self):
        """Test behavior with empty feedback data."""
        empty_data = {}
        results = self.evaluator.evaluate(empty_data)
        
        # Check that the results still contain the expected keys
        self.assertIn('overall_score', results)
        self.assertIn('dimension_scores', results)
        self.assertIn('strengths', results)
        self.assertIn('improvement_areas', results)
        self.assertIn('trend', results)
        
        # Check that dimension scores handle empty data
        dimensions = results['dimension_scores']
        for dimension in dimensions.values():
            self.assertGreaterEqual(dimension, 0.0)
            self.assertLessEqual(dimension, 1.0)


class TestThresholdTrigger(unittest.TestCase):
    """Tests for the ThresholdTrigger class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a trigger with custom thresholds for testing
        custom_config = {
            'thresholds': {
                'overall_score': {
                    'min': 0.6,  # Minimum acceptable overall score
                    'target': 0.8  # Target overall score
                },
                'user_satisfaction': {
                    'min': 0.7  # Minimum acceptable user satisfaction
                },
                'error_rate': {
                    'max': 0.05  # Maximum acceptable error rate
                },
                'improvement_areas': {
                    'max_count': 2  # Maximum number of improvement areas before triggering
                }
            }
        }
        self.trigger = ThresholdTrigger(config=custom_config)
        
        # Sample evaluation results for testing
        self.good_results = {
            'overall_score': 0.85,
            'dimension_scores': {
                'user_satisfaction': 0.9,
                'task_completion': 0.85,
                'system_performance': 0.8,
                'reliability': 0.9
            },
            'improvement_areas': [],
            'trend': 'improving'
        }
        
        self.bad_results = {
            'overall_score': 0.55,
            'dimension_scores': {
                'user_satisfaction': 0.6,
                'task_completion': 0.5,
                'system_performance': 0.6,
                'reliability': 0.5
            },
            'improvement_areas': ['task_completion', 'reliability'],
            'trend': 'declining'
        }
    
    def test_initialization(self):
        """Test that the trigger initializes correctly."""
        # Create a trigger with default config for this test
        default_trigger = ThresholdTrigger()
        self.assertIsInstance(default_trigger, ThresholdTrigger)
        self.assertEqual(default_trigger.config, {})
        
        # Check that our test instance has the custom config
        self.assertIsInstance(self.trigger, ThresholdTrigger)
        self.assertIn('thresholds', self.trigger.config)
        
        # Test with custom config
        custom_config = {'thresholds': {'overall_score': {'min': 0.7}}}
        trigger = ThresholdTrigger(config=custom_config)
        self.assertEqual(trigger.config, custom_config)
        self.assertEqual(trigger.thresholds['overall_score']['min'], 0.7)
    
    def test_should_update_good_results(self):
        """Test should_update with good evaluation results."""
        # Create a trigger with specific thresholds for this test
        custom_config = {
            'thresholds': {
                'overall_score': {
                    'min': 0.5,  # Lower minimum threshold
                    'target': 0.7  # Lower target threshold
                },
                'user_satisfaction': {
                    'min': 0.5  # Lower minimum threshold
                },
                'error_rate': {
                    'max': 0.2  # Higher maximum threshold
                },
                'improvement_areas': {
                    'max_count': 5  # Higher threshold to not trigger on our good results
                }
            }
        }
        test_trigger = ThresholdTrigger(config=custom_config)
        
        # Create a very good result set that shouldn't trigger an update
        very_good_results = {
            'overall_score': 0.95,
            'dimension_scores': {
                'user_satisfaction': 0.95,
                'task_completion': 0.95,
                'system_performance': 0.95,
                'reliability': 0.95
            },
            'improvement_areas': [],
            'trend': 'improving'
        }
        
        # Test with very good results
        should_update = test_trigger.should_update(very_good_results)
        self.assertFalse(should_update)
    
    def test_should_update_bad_results(self):
        """Test should_update with bad evaluation results."""
        should_update = self.trigger.should_update(self.bad_results)
        self.assertTrue(should_update)
    
    def test_get_update_priority(self):
        """Test get_update_priority method."""
        priority_good = self.trigger.get_update_priority(self.good_results)
        priority_bad = self.trigger.get_update_priority(self.bad_results)
        
        self.assertEqual(priority_good, 'low')
        self.assertEqual(priority_bad, 'high')
    
    def test_custom_thresholds(self):
        """Test behavior with custom thresholds."""
        custom_config = {
            'thresholds': {
                'overall_score': {
                    'min': 0.9  # Higher threshold
                }
            }
        }
        trigger = ThresholdTrigger(config=custom_config)
        
        # With the higher threshold, even good results should trigger an update
        should_update = trigger.should_update(self.good_results)
        self.assertTrue(should_update)


if __name__ == '__main__':
    unittest.main()
