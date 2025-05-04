"""Metalearning system for the SuperDeepAgent project.

This package provides components for knowledge abstraction, transfer, and adaptation
to enable metalearning capabilities in agent models.
"""

from .abstractors import KnowledgeAbstracter, SimpleKnowledgeAbstracter, DefaultKnowledgeAbstracter
from .transferers import KnowledgeTransferer, SimpleKnowledgeTransferer, DefaultKnowledgeTransferer
from .adapters import LearningAdapter, SimpleLearningAdapter, DefaultLearningAdapter

__all__ = [
    'KnowledgeAbstracter',
    'SimpleKnowledgeAbstracter',
    'DefaultKnowledgeAbstracter',
    'KnowledgeTransferer',
    'SimpleKnowledgeTransferer',
    'DefaultKnowledgeTransferer',
    'LearningAdapter',
    'SimpleLearningAdapter',
    'DefaultLearningAdapter',
]
