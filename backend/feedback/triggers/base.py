"""Base interface for update trigger components in the SuperDeepAgent feedback system."""

from abc import ABC, abstractmethod


class UpdateTrigger(ABC):
    """
    Base interface for update trigger components.
    
    Update triggers determine when the agent should be updated based on
    evaluation results from feedback data.
    """
    
    @abstractmethod
    def should_update(self, evaluation_results):
        """
        Determine if an agent update should be triggered based on evaluation results.
        
        Args:
            evaluation_results: Results from feedback evaluation containing
                               performance metrics and other indicators.
                          
        Returns:
            bool: True if an update should be triggered, False otherwise.
        """
        pass
