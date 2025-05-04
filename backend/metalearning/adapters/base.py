"""Base interface for learning adaptation in the metalearning system."""

import abc
from typing import Any, Dict


class LearningAdapter(abc.ABC):
    """Abstract base class for learning adaptation.
    
    Learning adapters take transferable knowledge and adapt it to
    specific agent models.
    """
    
    @abc.abstractmethod
    def adapt(self, agent_model: Any, transferable_knowledge: Dict[str, Any]) -> Any:
        """Adapt transferable knowledge to a specific agent model.
        
        Args:
            agent_model: The agent model to adapt knowledge to.
            transferable_knowledge: Knowledge in a transferable format.
            
        Returns:
            Updated agent model with adapted knowledge.
        """
        pass
