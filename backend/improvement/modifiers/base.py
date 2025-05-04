"""Base interface for behavior modification components in the SuperDeepAgent improvement system."""

from abc import ABC, abstractmethod


class BehaviorModifier(ABC):
    """
    Base interface for agent behavior modification components.
    
    Behavior modifiers take evaluation metrics and current agent behavior
    to produce modified behavior that addresses identified issues.
    """
    
    @abstractmethod
    def modify(self, agent_behavior, evaluation_metrics):
        """
        Modify agent behavior based on evaluation metrics.
        
        Args:
            agent_behavior: Current behavior configuration or model of the agent.
            evaluation_metrics (dict): Metrics from the evaluation process
                                      indicating areas for improvement.
                                      
        Returns:
            Modified agent behavior configuration or model.
        """
        pass
