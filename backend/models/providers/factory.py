"""
Factory for creating LLM providers in SuperDeepAgent.

This module provides a factory for creating LLM provider instances
based on configuration.
"""

import logging
from typing import Dict, Any, Optional, List, Union

from .base import BaseProvider
from .openrouter import OpenRouterProvider
from .ollama import OllamaProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProviderFactory:
    """
    Factory for creating LLM provider instances.
    
    Provides methods for creating provider instances based on configuration.
    """
    
    @staticmethod
    def create_provider(
        provider_type: str,
        provider_config: Dict[str, Any]
    ) -> BaseProvider:
        """
        Create a provider instance based on the provider type and configuration.
        
        Args:
            provider_type: The type of provider to create.
            provider_config: The provider configuration.
            
        Returns:
            A provider instance.
            
        Raises:
            ValueError: If the provider type is not supported.
        """
        provider_name = provider_config.get("name", provider_type)
        model = provider_config.get("model")
        
        if not model:
            raise ValueError(f"Model not specified for provider {provider_name}")
        
        if provider_type == "openrouter":
            api_key_env = provider_config.get("api_key_env", "OPENROUTER_API_KEY")
            return OpenRouterProvider(
                name=provider_name,
                model=model,
                api_key_env=api_key_env,
                **provider_config
            )
        elif provider_type == "ollama":
            endpoint = provider_config.get("endpoint", "http://localhost:11434")
            return OllamaProvider(
                name=provider_name,
                model=model,
                endpoint=endpoint,
                **provider_config
            )
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
    
    @staticmethod
    def create_provider_from_config(
        config: Dict[str, Any]
    ) -> BaseProvider:
        """
        Create a provider instance from a configuration dictionary.
        
        Args:
            config: The provider configuration dictionary.
            
        Returns:
            A provider instance.
        """
        provider_type = config.get("provider")
        if not provider_type:
            raise ValueError("Provider type not specified in configuration")
        
        return ProviderFactory.create_provider(provider_type, config)
    
    @staticmethod
    def create_providers_with_fallback(
        configs: List[Dict[str, Any]]
    ) -> List[BaseProvider]:
        """
        Create a list of provider instances with fallback.
        
        Args:
            configs: List of provider configurations.
            
        Returns:
            A list of provider instances.
        """
        providers = []
        
        for config in configs:
            try:
                provider = ProviderFactory.create_provider_from_config(config)
                providers.append(provider)
            except Exception as e:
                logger.warning(f"Failed to create provider from config {config}: {e}")
        
        if not providers:
            raise ValueError("No valid providers could be created from the configurations")
        
        return providers
