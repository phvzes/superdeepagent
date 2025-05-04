"""
LLM pipeline for SuperDeepAgent.

This module provides the main LLM pipeline implementation, which handles
model selection, fallback logic, and integration with the memory system.
"""

import logging
import os
from typing import Dict, List, Any, Optional, Union, Tuple

from ..config.loader import LLMPipelineConfig, load_llm_config
from ..providers.factory import ProviderFactory
from ..providers.base import BaseProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMPipeline:
    """
    LLM pipeline for SuperDeepAgent.
    
    Provides a unified API for model interactions, with support for
    model selection based on task requirements and fallback logic.
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        memory_manager: Optional[Any] = None
    ):
        """
        Initialize the LLM pipeline.
        
        Args:
            config_path: Optional path to the LLM pipeline configuration file.
                         If None, uses the default path.
            memory_manager: Optional memory manager instance for context-aware responses.
        """
        self.config = load_llm_config(config_path)
        self.memory_manager = memory_manager
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self) -> None:
        """Initialize the LLM providers from the configuration."""
        for name, llm_config in self.config.llms.items():
            try:
                provider = ProviderFactory.create_provider(
                    llm_config.provider,
                    llm_config.to_dict()
                )
                self.providers[name] = provider
                logger.info(f"Initialized provider {name} ({llm_config.provider}/{llm_config.model})")
            except Exception as e:
                logger.warning(f"Failed to initialize provider {name}: {e}")
    
    def _get_provider_chain(
        self,
        provider_name: Optional[str] = None,
        task_metadata: Optional[Dict[str, Any]] = None
    ) -> List[BaseProvider]:
        """
        Get the provider chain for the given task.
        
        Args:
            provider_name: Optional name of the provider to use.
            task_metadata: Optional task metadata for provider selection.
            
        Returns:
            A list of provider instances in the fallback chain.
        """
        # If provider name is specified, use it
        if provider_name and provider_name in self.providers:
            start_name = provider_name
        # Otherwise, select based on task metadata
        elif task_metadata:
            start_name = self._select_provider_for_task(task_metadata)
        # Otherwise, use default
        else:
            start_name = "default"
        
        # Get the fallback chain
        fallback_configs = self.config.get_fallback_chain(start_name)
        
        # Convert configs to provider instances
        provider_chain = []
        for config in fallback_configs:
            provider_name = next(
                (name for name, llm_config in self.config.llms.items() 
                 if llm_config == config),
                None
            )
            if provider_name and provider_name in self.providers:
                provider_chain.append(self.providers[provider_name])
        
        if not provider_chain:
            # If no providers in chain, try to use default
            if "default" in self.providers:
                provider_chain = [self.providers["default"]]
            # If no default, use the first available provider
            elif self.providers:
                provider_chain = [next(iter(self.providers.values()))]
            else:
                raise ValueError("No available LLM providers")
        
        return provider_chain
    
    def _select_provider_for_task(
        self,
        task_metadata: Dict[str, Any]
    ) -> str:
        """
        Select the appropriate provider for the given task.
        
        Args:
            task_metadata: Task metadata for provider selection.
            
        Returns:
            The name of the selected provider.
        """
        # Simple selection logic based on task type
        task_type = task_metadata.get("type", "")
        domain = task_metadata.get("domain", "")
        
        # For now, use a simple mapping
        # This can be expanded with more sophisticated logic
        if task_type == "chat":
            return "default"
        elif task_type == "completion":
            return "default"
        elif task_type == "local" or domain == "local":
            return "local" if "local" in self.providers else "default"
        
        # Default fallback
        return "default"
    
    def _fetch_relevant_context(
        self,
        query: str,
        task_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Fetch relevant context from the memory system.
        
        Args:
            query: The query to fetch context for.
            task_metadata: Optional task metadata.
            
        Returns:
            The relevant context as a string.
        """
        if not self.memory_manager:
            return ""
        
        try:
            # Determine memory types to search based on task metadata
            memory_type = None
            if task_metadata:
                if task_metadata.get("memory_type"):
                    memory_type = task_metadata.get("memory_type")
                elif task_metadata.get("type") == "factual":
                    memory_type = "semantic"
                elif task_metadata.get("type") == "procedural":
                    memory_type = "procedural"
            
            # Search for relevant memories
            if memory_type:
                if memory_type == "semantic":
                    results = self.memory_manager.search_semantic_memories(query, k=3)
                elif memory_type == "episodic":
                    results = self.memory_manager.search_episodic_memories(query, k=3)
                elif memory_type == "procedural":
                    results = self.memory_manager.search_procedural_memories(query, k=3)
                else:
                    results = self.memory_manager.search_memories(query, k=5)
            else:
                results = self.memory_manager.search_memories(query, k=5)
            
            # Format the results as context
            if results:
                context_parts = []
                for i, result in enumerate(results):
                    if hasattr(result, "page_content"):
                        # LangChain document format
                        content = result.page_content
                        metadata = result.metadata
                    else:
                        # Direct dictionary format
                        content = result.get("content", "")
                        metadata = result.get("metadata", {})
                    
                    context_parts.append(f"[Memory {i+1}] {content}")
                
                return "\n\n".join(context_parts)
            
            return ""
        except Exception as e:
            logger.warning(f"Failed to fetch relevant context: {e}")
            return ""
    
    def completion(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        provider_name: Optional[str] = None,
        task_metadata: Optional[Dict[str, Any]] = None,
        include_context: bool = True,
        **kwargs
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a text completion for the given prompt.
        
        Args:
            prompt: The input prompt.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            provider_name: Optional name of the provider to use.
            task_metadata: Optional task metadata for provider selection.
            include_context: Whether to include relevant context from memory.
            **kwargs: Additional provider-specific parameters.
            
        Returns:
            A tuple containing the generated text and metadata.
            
        Raises:
            Exception: If all providers in the fallback chain fail.
        """
        # Get the provider chain
        provider_chain = self._get_provider_chain(provider_name, task_metadata)
        
        # Fetch relevant context if needed
        context = ""
        if include_context and self.memory_manager:
            context = self._fetch_relevant_context(prompt, task_metadata)
        
        # Prepare the full prompt with context
        full_prompt = prompt
        if context:
            full_prompt = f"Context:\n{context}\n\nPrompt:\n{prompt}"
        
        # Try each provider in the chain
        last_error = None
        for provider in provider_chain:
            try:
                result, metadata = provider.completion(
                    full_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
                
                # Add context information to metadata
                metadata["context_included"] = bool(context)
                
                return result, metadata
            except Exception as e:
                logger.warning(f"Provider {provider.name} failed: {e}")
                last_error = e
        
        # If all providers failed, raise the last error
        raise Exception(f"All providers in the fallback chain failed. Last error: {last_error}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        provider_name: Optional[str] = None,
        task_metadata: Optional[Dict[str, Any]] = None,
        include_context: bool = True,
        **kwargs
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a response for the given chat messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            provider_name: Optional name of the provider to use.
            task_metadata: Optional task metadata for provider selection.
            include_context: Whether to include relevant context from memory.
            **kwargs: Additional provider-specific parameters.
            
        Returns:
            A tuple containing the generated response and metadata.
            
        Raises:
            Exception: If all providers in the fallback chain fail.
        """
        # Get the provider chain
        provider_chain = self._get_provider_chain(provider_name, task_metadata)
        
        # Fetch relevant context if needed
        context = ""
        if include_context and self.memory_manager and messages:
            # Use the last user message as the query
            user_messages = [m for m in messages if m.get("role") == "user"]
            if user_messages:
                query = user_messages[-1].get("content", "")
                context = self._fetch_relevant_context(query, task_metadata)
        
        # Prepare the messages with context
        processed_messages = messages.copy()
        if context and processed_messages:
            # Find the first message
            if processed_messages[0].get("role") == "system":
                # Add context to system message
                system_content = processed_messages[0].get("content", "")
                processed_messages[0]["content"] = f"{system_content}\n\nRelevant context:\n{context}"
            else:
                # Add a new system message with context
                processed_messages.insert(0, {
                    "role": "system",
                    "content": f"Relevant context:\n{context}"
                })
        
        # Try each provider in the chain
        last_error = None
        for provider in provider_chain:
            try:
                result, metadata = provider.chat(
                    processed_messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
                
                # Add context information to metadata
                metadata["context_included"] = bool(context)
                
                return result, metadata
            except Exception as e:
                logger.warning(f"Provider {provider.name} failed: {e}")
                last_error = e
        
        # If all providers failed, raise the last error
        raise Exception(f"All providers in the fallback chain failed. Last error: {last_error}")
