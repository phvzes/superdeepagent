"""
Tests for the Phase3Manager class of the SuperDeepAgent project.

This module contains tests for the Phase3Manager class, which provides a unified API
for interacting with Phase 3 components.
"""

import unittest
from unittest.mock import MagicMock, patch
import time
import threading

from superdeepagent.phase3_manager import Phase3Manager


class TestPhase3Manager(unittest.TestCase):
    """Tests for the Phase3Manager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a Phase3Manager instance with default config
        self.manager = Phase3Manager()
        
        # Sample interaction data for testing
        self.interaction_data = {
            'explicit_ratings': [4, 5, 3, 4, 5],
            'comments': ['Great response!', 'Could be better'],
            'interaction_patterns': {
                'session_duration': 120,
                'response_acceptance_rate': 0.8,
                'follow_up_questions': 3
            },
            'response_times': [0.5, 0.8, 1.2, 0.7, 0.9],
            'resource_usage': {
                'avg_cpu': 0.3,
                'max_memory': 512,
                'avg_memory': 256
            },
            'error_logs': [
                {'type': 'api_error', 'message': 'API timeout'}
            ],
            'total_interactions': 100,
            'timestamp': 1620000000
        }
        
        # Sample agent for testing
        self.agent = {
            'behavior': {
                'verbosity': 0.5,
                'empathy': 0.5,
                'thoroughness': 0.5,
                'precision': 0.5,
                'conciseness': 0.5
            },
            'model': {
                'name': 'TestModel',
                'version': '1.0',
                'parameters': {
                    'temperature': 0.7,
                    'top_p': 0.9
                }
            },
            'id': 'test-agent-123',
            'name': 'Test Agent'
        }
    
    def test_initialization(self):
        """Test that the manager initializes correctly."""
        self.assertIsInstance(self.manager, Phase3Manager)
        
        # Check that the integration is initialized
        self.assertIsNotNone(self.manager.integration)
        
        # Check initial state
        self.assertFalse(self.manager.running)
        self.assertFalse(self.manager.auto_update)
        self.assertEqual(self.manager.update_interval, 3600)
        self.assertIsNone(self.manager.last_update_time)
        self.assertIsNone(self.manager.update_thread)
        self.assertIsNone(self.manager.agent)
        
        # Check history collections
        self.assertEqual(self.manager.feedback_history, [])
        self.assertEqual(self.manager.improvement_history, [])
        self.assertEqual(self.manager.metalearning_history, [])
        self.assertEqual(self.manager.cycle_history, [])
    
    def test_start(self):
        """Test the start method."""
        # Start the manager
        result = self.manager.start(self.agent)
        
        # Check that the start was successful
        self.assertTrue(result)
        self.assertTrue(self.manager.running)
        self.assertEqual(self.manager.agent, self.agent)
        self.assertIsNotNone(self.manager.last_update_time)
        
        # Check that auto-update thread is not started (auto_update is False)
        self.assertIsNone(self.manager.update_thread)
    
    def test_start_with_auto_update(self):
        """Test the start method with auto_update enabled."""
        # Configure auto_update
        self.manager.auto_update = True
        
        # Start the manager
        result = self.manager.start(self.agent)
        
        try:
            # Check that the start was successful
            self.assertTrue(result)
            self.assertTrue(self.manager.running)
            
            # Check that auto-update thread is started
            self.assertIsNotNone(self.manager.update_thread)
            self.assertTrue(self.manager.update_thread.is_alive())
            
        finally:
            # Stop the manager to clean up the thread
            self.manager.stop()
    
    def test_start_already_running(self):
        """Test the start method when already running."""
        # Start the manager
        self.manager.start(self.agent)
        
        # Try to start again
        result = self.manager.start(self.agent)
        
        # Check that the second start failed
        self.assertFalse(result)
        
        # Clean up
        self.manager.stop()
    
    def test_stop(self):
        """Test the stop method."""
        # Start the manager
        self.manager.start(self.agent)
        
        # Stop the manager
        result = self.manager.stop()
        
        # Check that the stop was successful
        self.assertTrue(result)
        self.assertFalse(self.manager.running)
    
    def test_stop_not_running(self):
        """Test the stop method when not running."""
        # Try to stop without starting
        result = self.manager.stop()
        
        # Check that the stop failed
        self.assertFalse(result)
    
    def test_step(self):
        """Test the step method."""
        # Mock the integration.run_complete_cycle method
        original_run_complete_cycle = self.manager.integration.run_complete_cycle
        self.manager.integration.run_complete_cycle = MagicMock(
            return_value=(self.agent, {'updated': True, 'test': 'data'})
        )
        
        try:
            # Start the manager
            self.manager.start(self.agent)
            
            # Run a step
            result = self.manager.step(self.interaction_data)
            
            # Check that the step was successful
            self.assertIn('updated', result)
            self.assertIn('test', result)
            self.assertTrue(result['updated'])
            self.assertEqual(result['test'], 'data')
            
            # Check that the cycle history is updated
            self.assertEqual(len(self.manager.cycle_history), 1)
            self.assertEqual(self.manager.cycle_history[0], result)
            
        finally:
            # Restore the original method and stop the manager
            self.manager.integration.run_complete_cycle = original_run_complete_cycle
            self.manager.stop()
    
    def test_step_not_running(self):
        """Test the step method when not running."""
        # Try to step without starting
        result = self.manager.step(self.interaction_data)
        
        # Check that the step failed
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Manager not running')
    
    def test_collect_feedback(self):
        """Test the collect_feedback method."""
        # Mock the integration.collect_feedback method
        original_collect_feedback = self.manager.integration.collect_feedback
        self.manager.integration.collect_feedback = MagicMock(
            return_value={'test': 'feedback'}
        )
        
        try:
            # Start the manager
            self.manager.start(self.agent)
            
            # Collect feedback
            result = self.manager.collect_feedback(self.interaction_data)
            
            # Check that the feedback collection was successful
            self.assertIn('test', result)
            self.assertEqual(result['test'], 'feedback')
            
            # Check that the feedback history is updated
            self.assertEqual(len(self.manager.feedback_history), 1)
            self.assertEqual(self.manager.feedback_history[0], result)
            
        finally:
            # Restore the original method and stop the manager
            self.manager.integration.collect_feedback = original_collect_feedback
            self.manager.stop()
    
    def test_collect_feedback_not_running(self):
        """Test the collect_feedback method when not running."""
        # Try to collect feedback without starting
        result = self.manager.collect_feedback(self.interaction_data)
        
        # Check that the collection failed
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Manager not running')
    
    def test_improve(self):
        """Test the improve method."""
        # Mock the integration.run_improvement_cycle method
        original_run_improvement_cycle = self.manager.integration.run_improvement_cycle
        self.manager.integration.run_improvement_cycle = MagicMock(
            return_value=(self.agent['behavior'], {'test': 'improvement'})
        )
        
        try:
            # Start the manager
            self.manager.start(self.agent)
            
            # Add feedback data to history
            self.manager.feedback_history.append({'test': 'feedback'})
            
            # Run improvement
            result = self.manager.improve()
            
            # Check that the improvement was successful
            self.assertIn('test', result)
            self.assertEqual(result['test'], 'improvement')
            
            # Check that the improvement history is updated
            self.assertEqual(len(self.manager.improvement_history), 1)
            self.assertEqual(self.manager.improvement_history[0], result)
            
        finally:
            # Restore the original method and stop the manager
            self.manager.integration.run_improvement_cycle = original_run_improvement_cycle
            self.manager.stop()
    
    def test_improve_with_feedback(self):
        """Test the improve method with provided feedback data."""
        # Mock the integration.run_improvement_cycle method
        original_run_improvement_cycle = self.manager.integration.run_improvement_cycle
        self.manager.integration.run_improvement_cycle = MagicMock(
            return_value=(self.agent['behavior'], {'test': 'improvement'})
        )
        
        try:
            # Start the manager
            self.manager.start(self.agent)
            
            # Run improvement with provided feedback
            feedback_data = {'custom': 'feedback'}
            result = self.manager.improve(feedback_data)
            
            # Check that the improvement was successful
            self.assertIn('test', result)
            self.assertEqual(result['test'], 'improvement')
            
            # Check that the integration method was called with the provided feedback
            self.manager.integration.run_improvement_cycle.assert_called_with(
                self.agent['behavior'], feedback_data
            )
            
        finally:
            # Restore the original method and stop the manager
            self.manager.integration.run_improvement_cycle = original_run_improvement_cycle
            self.manager.stop()
    
    def test_improve_no_feedback(self):
        """Test the improve method with no feedback data available."""
        # Start the manager
        self.manager.start(self.agent)
        
        # Run improvement without any feedback in history
        result = self.manager.improve()
        
        # Check that the improvement failed
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'No feedback data available')
        
        # Clean up
        self.manager.stop()
    
    def test_adapt(self):
        """Test the adapt method."""
        # Mock the integration methods
        original_run_reflection = self.manager.integration.run_reflection
        original_run_metalearning_cycle = self.manager.integration.run_metalearning_cycle
        
        self.manager.integration.run_reflection = MagicMock(
            return_value={'test': 'reflection'}
        )
        self.manager.integration.run_metalearning_cycle = MagicMock(
            return_value=(self.agent['model'], {'test': 'metalearning'})
        )
        
        try:
            # Start the manager
            self.manager.start(self.agent)
            
            # Add improvement data to history
            self.manager.improvement_history.append({'test': 'improvement'})
            
            # Run adaptation
            result = self.manager.adapt()
            
            # Check that the adaptation was successful
            self.assertIn('test', result)
            self.assertEqual(result['test'], 'metalearning')
            
            # Check that the metalearning history is updated
            self.assertEqual(len(self.manager.metalearning_history), 1)
            self.assertEqual(self.manager.metalearning_history[0], result)
            
        finally:
            # Restore the original methods and stop the manager
            self.manager.integration.run_reflection = original_run_reflection
            self.manager.integration.run_metalearning_cycle = original_run_metalearning_cycle
            self.manager.stop()
    
    def test_adapt_with_insights(self):
        """Test the adapt method with provided reflection insights."""
        # Mock the integration.run_metalearning_cycle method
        original_run_metalearning_cycle = self.manager.integration.run_metalearning_cycle
        self.manager.integration.run_metalearning_cycle = MagicMock(
            return_value=(self.agent['model'], {'test': 'metalearning'})
        )
        
        try:
            # Start the manager
            self.manager.start(self.agent)
            
            # Run adaptation with provided insights
            insights = {'custom': 'insights'}
            result = self.manager.adapt(insights)
            
            # Check that the adaptation was successful
            self.assertIn('test', result)
            self.assertEqual(result['test'], 'metalearning')
            
            # Check that the integration method was called with the provided insights
            self.manager.integration.run_metalearning_cycle.assert_called_with(
                self.agent['model'], insights
            )
            
        finally:
            # Restore the original method and stop the manager
            self.manager.integration.run_metalearning_cycle = original_run_metalearning_cycle
            self.manager.stop()
    
    def test_adapt_no_improvement_results(self):
        """Test the adapt method with no improvement results available."""
        # Start the manager
        self.manager.start(self.agent)
        
        # Run adaptation without any improvement results in history
        result = self.manager.adapt()
        
        # Check that the adaptation failed
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'No improvement results available for reflection')
        
        # Clean up
        self.manager.stop()
    
    def test_get_metrics(self):
        """Test the get_metrics method."""
        # Start the manager
        self.manager.start(self.agent)
        
        # Add some data to history
        self.manager.feedback_history.append({'test': 'feedback'})
        self.manager.improvement_history.append({'test': 'improvement'})
        self.manager.metalearning_history.append({'test': 'metalearning'})
        self.manager.cycle_history.append({'test': 'cycle'})
        
        # Get metrics
        metrics = self.manager.get_metrics()
        
        # Check that the metrics contain the expected keys
        self.assertIn('status', metrics)
        self.assertIn('history_sizes', metrics)
        self.assertIn('latest_results', metrics)
        
        # Check status
        status = metrics['status']
        self.assertTrue(status['running'])
        self.assertFalse(status['auto_update'])
        self.assertEqual(status['update_interval'], 3600)
        self.assertIsNotNone(status['last_update_time'])
        
        # Check history sizes
        history_sizes = metrics['history_sizes']
        self.assertEqual(history_sizes['feedback'], 1)
        self.assertEqual(history_sizes['improvement'], 1)
        self.assertEqual(history_sizes['metalearning'], 1)
        self.assertEqual(history_sizes['cycle'], 1)
        
        # Check latest results
        latest_results = metrics['latest_results']
        self.assertEqual(latest_results['feedback'], {'test': 'feedback'})
        self.assertEqual(latest_results['improvement'], {'test': 'improvement'})
        self.assertEqual(latest_results['metalearning'], {'test': 'metalearning'})
        self.assertEqual(latest_results['cycle'], {'test': 'cycle'})
        
        # Clean up
        self.manager.stop()
    
    def test_configure(self):
        """Test the configure method."""
        # Start the manager
        self.manager.start(self.agent)
        
        # Configure the manager
        config_updates = {
            'auto_update': True,
            'update_interval': 1800,
            'custom_key': 'custom_value'
        }
        result = self.manager.configure(config_updates)
        
        # Check that the configuration was successful
        self.assertTrue(result)
        self.assertTrue(self.manager.auto_update)
        self.assertEqual(self.manager.update_interval, 1800)
        self.assertEqual(self.manager.config.get('custom_key'), 'custom_value')
        
        # Clean up
        self.manager.stop()
    
    def test_reset_history(self):
        """Test the reset_history method."""
        # Start the manager
        self.manager.start(self.agent)
        
        # Add some data to history
        self.manager.feedback_history.append({'test': 'feedback'})
        self.manager.improvement_history.append({'test': 'improvement'})
        self.manager.metalearning_history.append({'test': 'metalearning'})
        self.manager.cycle_history.append({'test': 'cycle'})
        
        # Reset history
        result = self.manager.reset_history()
        
        # Check that the reset was successful
        self.assertTrue(result)
        self.assertEqual(self.manager.feedback_history, [])
        self.assertEqual(self.manager.improvement_history, [])
        self.assertEqual(self.manager.metalearning_history, [])
        self.assertEqual(self.manager.cycle_history, [])
        
        # Clean up
        self.manager.stop()


if __name__ == '__main__':
    unittest.main()
