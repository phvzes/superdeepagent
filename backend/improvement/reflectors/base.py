"""Base interface for reflection components in the SuperDeepAgent improvement system."""

from abc import ABC, abstractmethod


class Reflector(ABC):
    """
    Base interface for agent reflection components.
    
    Reflectors analyze the results of improvement cycles to generate insights
    and meta-learning that can guide future improvement processes.
    """
    
    @abstractmethod
    def reflect(self, cycle_results):
        """
        Reflect on the results of improvement cycles to generate insights.
        
        Args:
            cycle_results: Data containing the results of one or more
                          improvement cycles, including before/after metrics.
                          
        Returns:
            dict: Reflection insights and meta-learning outcomes.
        """
        pass
