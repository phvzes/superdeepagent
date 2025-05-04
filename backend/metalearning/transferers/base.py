"""Base interface for knowledge transfer in the metalearning system."""

import abc
from typing import Any, Dict


class KnowledgeTransferer(abc.ABC):
    """Abstract base class for knowledge transfer.
    
    Knowledge transferers take abstracted knowledge and prepare it for
    adaptation to specific agent models.
    """
    
    @abc.abstractmethod
    def transfer(self, abstracted_knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """Transform abstracted knowledge into a transferable format.
        
        Args:
            abstracted_knowledge: Knowledge in abstracted form.
            
        Returns:
            Knowledge in a format ready for adaptation to specific agent models.
        """
        pass
