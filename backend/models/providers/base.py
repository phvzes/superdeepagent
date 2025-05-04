"""
Base provider class for LLM interactions in SuperDeepAgent.

This module defines the base class for LLM providers, with common functionality
and abstract methods that must be implemented by specific providers.
"""

import abc
import json
import logging
import requests
from typing import Dict, List, Any, Optional, Union, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseProvider(abc.ABC):
    """
    Base class for LLM providers.
    
    Defines the common interface and functionality for all LLM providers.
    """
    
    def __init__(
        self,
        name: str,
        model: str,
        **kwargs
    ):
        """
        Initialize the base provider.
        
        Args:
            name: The name of the provider.
            model: The model identifier.
            **kwargs: Additional provider-specific configuration.
        """
        self.name = name
        self.model = model
        self.config = kwargs
        self.is_initialized = False
        
    def initialize(self) -> None:
        """Initialize the provider with necessary setup."""
        self.is_initialized = True
        logger.info(f"Initialized {self.name} provider with model {self.model}")
    
    @abc.abstractmethod
    def completion(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a text completion for the given prompt.
        
        Args:
            prompt: The input prompt.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            **kwargs: Additional provider-specific parameters.
            
        Returns:
            A tuple containing the generated text and metadata.
        """
        pass
    
    @abc.abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a response for the given chat messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            **kwargs: Additional provider-specific parameters.
            
        Returns:
            A tuple containing the generated response and metadata.
        """
        pass
    
    def _post_json(
        self,
        url: str,
        payload: Dict[str, Any],
        headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Helper method to make a POST request with JSON payload.
        
        Args:
            url: The URL to send the request to.
            payload: The JSON payload.
            headers: The request headers.
            
        Returns:
            The JSON response.
            
        Raises:
            Exception: If the request fails.
        """
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            raise Exception(f"Request to {url} failed: {str(e)}")
