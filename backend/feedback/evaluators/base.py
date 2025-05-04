"""Base interface for feedback evaluation components in the SuperDeepAgent feedback system."""

from abc import ABC, abstractmethod


class FeedbackEvaluator(ABC):
    """
    Base interface for feedback evaluation components.
    
    Feedback evaluators analyze collected feedback data to produce evaluation metrics
    that can be used to assess agent performance and trigger updates.
    """
    
    @abstractmethod
    def evaluate(self, feedback_data):
        """
        Evaluate agent performance based on collected feedback data.
        
        Args:
            feedback_data: Data containing collected feedback from various sources.
                          
        Returns:
            dict: Evaluation results derived from the feedback data.
        """
        pass
