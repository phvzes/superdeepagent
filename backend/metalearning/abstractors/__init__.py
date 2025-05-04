"""Knowledge abstraction module for the metalearning system."""

from .base import KnowledgeAbstracter
from .simple import SimpleKnowledgeAbstracter

# Default implementation
DefaultKnowledgeAbstracter = SimpleKnowledgeAbstracter
