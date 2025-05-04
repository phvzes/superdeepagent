"""Base interface for knowledge abstraction in the metalearning system."""

import abc
from typing import Any, Dict


class KnowledgeAbstracter(abc.ABC):
    """Abstract base class for knowledge abstraction.
    
    Knowledge abstracters transform raw knowledge data into abstract representations
    that can be transferred between different agent models.
    """
    
    @abc.abstractmethod
    def abstract(self, knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Abstract knowledge data into a transferable representation.
        
        Args:
            knowledge_data: Raw knowledge data to be abstracted.
            
        Returns:
            Abstracted knowledge representation.
        """
        pass
