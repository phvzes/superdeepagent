"""Threshold-based update trigger implementation for the SuperDeepAgent feedback system."""

from superdeepagent.feedback.triggers.base import UpdateTrigger


class ThresholdTrigger(UpdateTrigger):
    """
    Triggers agent updates based on threshold conditions in evaluation results.
    
    This trigger monitors evaluation metrics and initiates updates when
    specific thresholds are crossed, indicating a need for agent improvement.
    """
    
    def __init__(self, config=None):
        """
        Initialize the threshold trigger.
        
        Args:
            config (dict, optional): Configuration parameters for the trigger.
                May include threshold values for different metrics.
        """
        self.config = config or {}
        # Default thresholds
        self.thresholds = self.config.get('thresholds', {
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
        })
    
    def should_update(self, evaluation_results):
        """
        Determine if an agent update should be triggered based on evaluation results.
        
        Args:
            evaluation_results (dict): Results from feedback evaluation.
                Expected to contain:
                - 'overall_score': Overall performance score
                - 'dimension_scores': Scores for individual performance dimensions
                - 'improvement_areas': Identified areas for improvement
                
        Returns:
            bool: True if an update should be triggered, False otherwise.
        """
        # Check overall score threshold
        overall_score = evaluation_results.get('overall_score', 1.0)
        if overall_score < self.thresholds.get('overall_score', {}).get('min', 0.6):
            return True
        
        # Check dimension-specific thresholds
        dimension_scores = evaluation_results.get('dimension_scores', {})
        for dimension, score in dimension_scores.items():
            if dimension in self.thresholds and 'min' in self.thresholds[dimension]:
                if score < self.thresholds[dimension]['min']:
                    return True
        
        # Check error rate threshold
        reliability_score = dimension_scores.get('reliability', 1.0)
        error_rate = 1.0 - reliability_score  # Approximate error rate from reliability score
        if error_rate > self.thresholds.get('error_rate', {}).get('max', 0.05):
            return True
        
        # Check improvement areas threshold
        improvement_areas = evaluation_results.get('improvement_areas', [])
        if len(improvement_areas) > self.thresholds.get('improvement_areas', {}).get('max_count', 2):
            return True
        
        # Check trend-based conditions
        trend = evaluation_results.get('trend', 'stable')
        if trend == 'declining' and overall_score < self.thresholds.get('overall_score', {}).get('target', 0.8):
            return True
        
        # No threshold conditions met
        return False
    
    def get_update_priority(self, evaluation_results):
        """
        Determine the priority level for the triggered update.
        
        Args:
            evaluation_results (dict): Results from feedback evaluation.
                
        Returns:
            str: Priority level ('low', 'medium', 'high', or 'critical').
        """
        # This is an additional method not in the base interface
        # It provides more detailed information when an update is triggered
        
        overall_score = evaluation_results.get('overall_score', 1.0)
        
        if overall_score < 0.4:
            return 'critical'
        elif overall_score < 0.6:
            return 'high'
        elif overall_score < 0.7:
            return 'medium'
        else:
            return 'low'
