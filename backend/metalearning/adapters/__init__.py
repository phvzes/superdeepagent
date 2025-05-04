"""Learning adaptation module for the metalearning system."""

from .base import LearningAdapter
from .simple import SimpleLearningAdapter

# Default implementation
DefaultLearningAdapter = SimpleLearningAdapter
