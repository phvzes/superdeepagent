"""Performance evaluator implementation for the SuperDeepAgent feedback system."""

from superdeepagent.feedback.evaluators.base import FeedbackEvaluator


class PerformanceEvaluator(FeedbackEvaluator):
    """
    Evaluates agent performance based on collected feedback data.
    
    This evaluator analyzes user feedback and system metrics to produce
    comprehensive performance assessments that can guide agent improvements.
    """
    
    def __init__(self, config=None):
        """
        Initialize the performance evaluator.
        
        Args:
            config (dict, optional): Configuration parameters for the evaluator.
                May include weighting factors for different metrics.
        """
        self.config = config or {}
        # Default weights for different metric categories
        self.weights = self.config.get('weights', {
            'user_satisfaction': 0.4,
            'task_completion': 0.3,
            'system_performance': 0.2,
            'reliability': 0.1
        })
    
    def evaluate(self, feedback_data):
        """
        Evaluate agent performance based on collected feedback data.
        
        Args:
            feedback_data (dict): Combined feedback data from various collectors.
                Expected to contain:
                - User feedback metrics (satisfaction, sentiment, etc.)
                - System performance metrics (response times, resource usage, etc.)
                
        Returns:
            dict: Evaluation results including:
                - 'overall_score': Weighted performance score
                - 'dimension_scores': Scores for individual performance dimensions
                - 'strengths': Identified performance strengths
                - 'improvement_areas': Identified areas for improvement
                - 'trend': Performance trend compared to previous evaluations
        """
        # Extract relevant metrics from feedback data
        user_metrics = feedback_data.get('user_feedback', {})
        system_metrics = feedback_data.get('system_metrics', {})
        
        # Calculate dimension scores
        dimension_scores = {
            'user_satisfaction': self._evaluate_user_satisfaction(user_metrics),
            'task_completion': self._evaluate_task_completion(user_metrics),
            'system_performance': self._evaluate_system_performance(system_metrics),
            'reliability': self._evaluate_reliability(system_metrics)
        }
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(dimension_scores)
        
        # Identify strengths and improvement areas
        strengths = self._identify_strengths(dimension_scores)
        improvement_areas = self._identify_improvement_areas(dimension_scores)
        
        # Determine performance trend
        trend = self._determine_trend(feedback_data)
        
        return {
            'overall_score': overall_score,
            'dimension_scores': dimension_scores,
            'strengths': strengths,
            'improvement_areas': improvement_areas,
            'trend': trend
        }
    
    def _evaluate_user_satisfaction(self, user_metrics):
        """Evaluate user satisfaction dimension."""
        satisfaction_scores = user_metrics.get('satisfaction_scores', {})
        sentiment_analysis = user_metrics.get('sentiment_analysis', {})
        
        # Calculate score based on explicit ratings and sentiment
        avg_rating = satisfaction_scores.get('average', 0.0)
        sentiment_score = self._sentiment_to_score(sentiment_analysis.get('sentiment', 'neutral'))
        
        # Combine metrics with configurable weights
        rating_weight = 0.7
        sentiment_weight = 0.3
        
        return (avg_rating * rating_weight) + (sentiment_score * sentiment_weight)
    
    def _sentiment_to_score(self, sentiment):
        """Convert sentiment label to numerical score."""
        sentiment_scores = {
            'very_negative': 0.0,
            'negative': 0.25,
            'neutral': 0.5,
            'positive': 0.75,
            'very_positive': 1.0
        }
        return sentiment_scores.get(sentiment, 0.5)
    
    def _evaluate_task_completion(self, user_metrics):
        """Evaluate task completion dimension."""
        engagement_metrics = user_metrics.get('engagement_metrics', {})
        correction_patterns = user_metrics.get('correction_patterns', {})
        
        # Calculate score based on response acceptance and corrections
        acceptance_rate = engagement_metrics.get('response_acceptance_rate', 0.0)
        correction_factor = 1.0 - (min(correction_patterns.get('count', 0), 10) / 10)
        
        return (acceptance_rate * 0.6) + (correction_factor * 0.4)
    
    def _evaluate_system_performance(self, system_metrics):
        """Evaluate system performance dimension."""
        performance_metrics = system_metrics.get('performance_metrics', {})
        resource_metrics = system_metrics.get('resource_metrics', {})
        
        # Normalize response time (lower is better)
        avg_response_time = performance_metrics.get('avg_response_time', 0.0)
        max_acceptable_time = self.config.get('max_acceptable_response_time', 5.0)
        response_time_score = 1.0 - min(avg_response_time / max_acceptable_time, 1.0)
        
        # Normalize resource usage (lower is better)
        cpu_usage = resource_metrics.get('avg_cpu_usage', 0.0)
        memory_usage = resource_metrics.get('avg_memory_usage', 0.0)
        resource_score = 1.0 - ((cpu_usage + memory_usage) / 2)
        
        return (response_time_score * 0.7) + (resource_score * 0.3)
    
    def _evaluate_reliability(self, system_metrics):
        """Evaluate reliability dimension."""
        reliability_metrics = system_metrics.get('reliability_metrics', {})
        dependency_metrics = system_metrics.get('external_dependencies', {})
        
        # Error rate (lower is better)
        error_rate = reliability_metrics.get('error_rate', 0.0)
        error_score = 1.0 - min(error_rate * 10, 1.0)  # Scale up for sensitivity
        
        # External dependency reliability
        dependency_scores = []
        for service, metrics in dependency_metrics.items():
            if metrics.get('count', 0) > 0:
                dependency_scores.append(metrics.get('success_rate', 0.0))
        
        dependency_score = sum(dependency_scores) / len(dependency_scores) if dependency_scores else 1.0
        
        return (error_score * 0.6) + (dependency_score * 0.4)
    
    def _calculate_overall_score(self, dimension_scores):
        """Calculate overall performance score from dimension scores."""
        weighted_sum = 0.0
        for dimension, score in dimension_scores.items():
            weight = self.weights.get(dimension, 0.25)  # Default equal weight
            weighted_sum += score * weight
            
        return weighted_sum
    
    def _identify_strengths(self, dimension_scores):
        """Identify performance strengths based on dimension scores."""
        strengths = []
        for dimension, score in dimension_scores.items():
            if score >= 0.8:  # Threshold for considering a dimension a strength
                strengths.append(dimension)
                
        return strengths
    
    def _identify_improvement_areas(self, dimension_scores):
        """Identify areas for improvement based on dimension scores."""
        improvement_areas = []
        for dimension, score in dimension_scores.items():
            if score < 0.6:  # Threshold for considering a dimension needs improvement
                improvement_areas.append(dimension)
                
        return improvement_areas
    
    def _determine_trend(self, feedback_data):
        """Determine performance trend compared to previous evaluations."""
        # In a real implementation, this would compare with historical data
        # Simplified placeholder implementation
        previous_score = feedback_data.get('previous_evaluation', {}).get('overall_score')
        current_score = self._calculate_overall_score(feedback_data.get('dimension_scores', {}))
        
        if previous_score is None:
            return 'initial'
        elif current_score > previous_score + 0.05:
            return 'improving'
        elif current_score < previous_score - 0.05:
            return 'declining'
        else:
            return 'stable'
