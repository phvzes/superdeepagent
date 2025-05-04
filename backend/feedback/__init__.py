"""Feedback system for the SuperDeepAgent project.

This module provides components for collecting, evaluating, and triggering updates
based on feedback from various sources including user interactions and system metrics.
"""

from superdeepagent.feedback.collectors import FeedbackCollector, UserFeedbackCollector, SystemMetricsCollector
from superdeepagent.feedback.evaluators import FeedbackEvaluator, PerformanceEvaluator
from superdeepagent.feedback.triggers import UpdateTrigger, ThresholdTrigger

__all__ = [
    # Base interfaces
    'FeedbackCollector',
    'FeedbackEvaluator',
    'UpdateTrigger',
    
    # Collectors
    'UserFeedbackCollector',
    'SystemMetricsCollector',
    
    # Evaluators
    'PerformanceEvaluator',
    
    # Triggers
    'ThresholdTrigger'
]
