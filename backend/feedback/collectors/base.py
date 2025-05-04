"""Base interface for feedback collection components in the SuperDeepAgent feedback system."""

from abc import ABC, abstractmethod


class FeedbackCollector(ABC):
    """
    Base interface for feedback collection components.
    
    Feedback collectors gather data from various sources such as user interactions,
    system metrics, or external evaluations to provide input for the feedback system.
    """
    
    @abstractmethod
    def collect(self, interaction_data):
        """
        Collect feedback from the specified interaction data.
        
        Args:
            interaction_data: Data containing agent interactions, user inputs,
                             system metrics, or other relevant information.
                          
        Returns:
            dict: Collected feedback data.
        """
        pass
