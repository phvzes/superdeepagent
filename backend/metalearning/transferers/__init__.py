"""Knowledge transfer module for the metalearning system."""

from .base import KnowledgeTransferer
from .simple import SimpleKnowledgeTransferer

# Default implementation
DefaultKnowledgeTransferer = SimpleKnowledgeTransferer
