"""
Tests for the metalearning system components of the SuperDeepAgent project.

This module contains tests for the SimpleKnowledgeAbstracter, SimpleKnowledgeTransferer,
and SimpleLearningAdapter classes.
"""

import unittest
from unittest.mock import MagicMock, patch

from superdeepagent.metalearning.abstractors.simple import SimpleKnowledgeAbstracter
from superdeepagent.metalearning.transferers.simple import SimpleKnowledgeTransferer
from superdeepagent.metalearning.adapters.simple import SimpleLearningAdapter


class TestSimpleKnowledgeAbstracter(unittest.TestCase):
    """Tests for the SimpleKnowledgeAbstracter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.abstracter = SimpleKnowledgeAbstracter()
        
        # Sample knowledge data for testing
        self.knowledge_data = {
            'effective_strategies': ['user_satisfaction', 'task_completion'],
            'ineffective_strategies': ['response_time'],
            'improvement_trends': {
                'avg_satisfaction_improvement': 0.15,
                'consistent_improvement': True
            },
            'recommendations': [
                'Continue applying these effective strategies: user_satisfaction, task_completion',
                'Revise these less effective strategies: response_time',
                'Current improvement trajectory is positive, maintain approach'
            ]
        }
    
    def test_initialization(self):
        """Test that the abstracter initializes correctly."""
        self.assertIsInstance(self.abstracter, SimpleKnowledgeAbstracter)
        self.assertEqual(self.abstracter.config, {})
        
        # Test with custom config
        custom_config = {'key': 'value'}
        abstracter = SimpleKnowledgeAbstracter(config=custom_config)
        self.assertEqual(abstracter.config, custom_config)
    
    def test_abstract(self):
        """Test the abstract method."""
        abstracted = self.abstracter.abstract(self.knowledge_data)
        
        # Check that the abstracted knowledge contains the expected keys
        self.assertIn('metadata', abstracted)
        self.assertIn('content', abstracted)
        
        # Check metadata
        metadata = abstracted['metadata']
        self.assertEqual(metadata['abstraction_type'], 'simple')
        self.assertEqual(metadata['version'], '1.0')
        
        # Check that content preserves the original data
        content = abstracted['content']
        self.assertEqual(content, self.knowledge_data)
    
    def test_empty_knowledge_data(self):
        """Test behavior with empty knowledge data."""
        empty_data = {}
        abstracted = self.abstracter.abstract(empty_data)
        
        # Check that the abstracted knowledge still contains the expected keys
        self.assertIn('metadata', abstracted)
        self.assertIn('content', abstracted)
        
        # Check that content preserves the empty data
        self.assertEqual(abstracted['content'], empty_data)


class TestSimpleKnowledgeTransferer(unittest.TestCase):
    """Tests for the SimpleKnowledgeTransferer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.transferer = SimpleKnowledgeTransferer()
        
        # Sample abstracted knowledge for testing
        self.abstracted_knowledge = {
            'metadata': {
                'abstraction_type': 'simple',
                'version': '1.0'
            },
            'content': {
                'effective_strategies': ['user_satisfaction', 'task_completion'],
                'ineffective_strategies': ['response_time'],
                'improvement_trends': {
                    'avg_satisfaction_improvement': 0.15,
                    'consistent_improvement': True
                },
                'recommendations': [
                    'Continue applying these effective strategies: user_satisfaction, task_completion',
                    'Revise these less effective strategies: response_time'
                ]
            }
        }
    
    def test_initialization(self):
        """Test that the transferer initializes correctly."""
        self.assertIsInstance(self.transferer, SimpleKnowledgeTransferer)
        self.assertEqual(self.transferer.config, {})
        
        # Test with custom config
        custom_config = {'key': 'value'}
        transferer = SimpleKnowledgeTransferer(config=custom_config)
        self.assertEqual(transferer.config, custom_config)
    
    def test_transfer(self):
        """Test the transfer method."""
        transferable = self.transferer.transfer(self.abstracted_knowledge)
        
        # Check that the transferable knowledge contains the expected keys
        self.assertIn('metadata', transferable)
        self.assertIn('transferable_content', transferable)
        
        # Check metadata
        metadata = transferable['metadata']
        self.assertEqual(metadata['transfer_type'], 'simple')
        self.assertEqual(metadata['version'], '1.0')
        self.assertEqual(metadata['original_abstraction']['abstraction_type'], 'simple')
        
        # Check that transferable_content preserves the original content
        content = transferable['transferable_content']
        self.assertEqual(content, self.abstracted_knowledge['content'])
    
    def test_empty_abstracted_knowledge(self):
        """Test behavior with empty abstracted knowledge."""
        empty_data = {}
        transferable = self.transferer.transfer(empty_data)
        
        # Check that the transferable knowledge still contains the expected keys
        self.assertIn('metadata', transferable)
        self.assertIn('transferable_content', transferable)
        
        # Check that transferable_content is an empty dict
        self.assertEqual(transferable['transferable_content'], {})


class TestSimpleLearningAdapter(unittest.TestCase):
    """Tests for the SimpleLearningAdapter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.adapter = SimpleLearningAdapter()
        
        # Sample transferable knowledge for testing
        self.transferable_knowledge = {
            'metadata': {
                'transfer_type': 'simple',
                'version': '1.0',
                'original_abstraction': {
                    'abstraction_type': 'simple',
                    'version': '1.0'
                }
            },
            'transferable_content': {
                'effective_strategies': ['user_satisfaction', 'task_completion'],
                'ineffective_strategies': ['response_time'],
                'improvement_trends': {
                    'avg_satisfaction_improvement': 0.15,
                    'consistent_improvement': True
                },
                'recommendations': [
                    'Continue applying these effective strategies: user_satisfaction, task_completion',
                    'Revise these less effective strategies: response_time'
                ]
            }
        }
    
    def test_initialization(self):
        """Test that the adapter initializes correctly."""
        self.assertIsInstance(self.adapter, SimpleLearningAdapter)
        self.assertEqual(self.adapter.config, {})
        
        # Test with custom config
        custom_config = {'key': 'value'}
        adapter = SimpleLearningAdapter(config=custom_config)
        self.assertEqual(adapter.config, custom_config)
    
    def test_adapt_dict_model(self):
        """Test the adapt method with a dictionary model."""
        # Create a simple dictionary model
        agent_model = {'name': 'TestModel', 'version': '1.0'}
        
        adapted_model = self.adapter.adapt(agent_model, self.transferable_knowledge)
        
        # Check that the original model properties are preserved
        self.assertEqual(adapted_model['name'], 'TestModel')
        self.assertEqual(adapted_model['version'], '1.0')
        
        # Check that knowledge was added
        self.assertIn('knowledge_store', adapted_model)
        self.assertIn('adapted_knowledge', adapted_model['knowledge_store'])
        self.assertEqual(
            adapted_model['knowledge_store']['adapted_knowledge'],
            self.transferable_knowledge['transferable_content']
        )
    
    def test_adapt_object_model(self):
        """Test the adapt method with an object model."""
        # Create a simple object model
        class AgentModel:
            def __init__(self):
                self.name = 'TestModel'
                self.version = '1.0'
                self.knowledge_store = {}
        
        agent_model = AgentModel()
        
        adapted_model = self.adapter.adapt(agent_model, self.transferable_knowledge)
        
        # Check that the original model properties are preserved
        self.assertEqual(adapted_model.name, 'TestModel')
        self.assertEqual(adapted_model.version, '1.0')
        
        # Check that knowledge was added
        self.assertTrue(hasattr(adapted_model, 'knowledge_store'))
        self.assertIn('adapted_knowledge', adapted_model.knowledge_store)
        self.assertEqual(
            adapted_model.knowledge_store['adapted_knowledge'],
            self.transferable_knowledge['transferable_content']
        )
    
    def test_adapt_model_without_knowledge_store(self):
        """Test the adapt method with a model that doesn't have a knowledge store."""
        # Create a model without a knowledge store
        class SimpleModel:
            def __init__(self):
                self.name = 'SimpleModel'
        
        agent_model = SimpleModel()
        
        adapted_model = self.adapter.adapt(agent_model, self.transferable_knowledge)
        
        # Check that a knowledge store was added
        self.assertTrue(hasattr(adapted_model, 'knowledge_store'))
        self.assertIn('adapted_knowledge', adapted_model.knowledge_store)
    
    def test_empty_transferable_knowledge(self):
        """Test behavior with empty transferable knowledge."""
        empty_knowledge = {'transferable_content': {}}
        agent_model = {'name': 'TestModel'}
        
        adapted_model = self.adapter.adapt(agent_model, empty_knowledge)
        
        # Check that knowledge store was still added
        self.assertIn('knowledge_store', adapted_model)
        self.assertIn('adapted_knowledge', adapted_model['knowledge_store'])
        self.assertEqual(adapted_model['knowledge_store']['adapted_knowledge'], {})


if __name__ == '__main__':
    unittest.main()
