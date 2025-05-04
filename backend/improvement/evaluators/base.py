"""Base interface for self-evaluation components in the SuperDeepAgent improvement system."""

from abc import ABC, abstractmethod


class SelfEvaluator(ABC):
    """
    Base interface for agent self-evaluation components.
    
    Self-evaluators analyze feedback data to produce evaluation metrics
    that can be used to improve agent behavior.
    """
    
    @abstractmethod
    def evaluate(self, feedback_data):
        """
        Evaluate agent performance based on feedback data.
        
        Args:
            feedback_data: Data containing user feedback, interaction logs,
                          or other performance indicators.
                          
        Returns:
            dict: Evaluation metrics derived from the feedback data.
        """
        pass
