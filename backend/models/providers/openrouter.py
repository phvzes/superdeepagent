"""
OpenRouter provider for LLM interactions in SuperDeepAgent.

This module implements the OpenRouter API integration for accessing
various LLM models through a unified API.
"""

import os
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

from .base import BaseProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenRouterProvider(BaseProvider):
    """
    OpenRouter provider for LLM interactions.
    
    Implements the OpenRouter API for accessing various LLM models.
    """
    
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(
        self,
        name: str,
        model: str,
        api_key_env: str = "OPENROUTER_API_KEY",
        **kwargs
    ):
        """
        Initialize the OpenRouter provider.
        
        Args:
            name: The name of the provider.
            model: The model identifier.
            api_key_env: The environment variable name for the API key.
            **kwargs: Additional provider-specific configuration.
        """
        super().__init__(name, model, **kwargs)
        self.api_key_env = api_key_env
        self.api_key = None
        
    def initialize(self) -> None:
        """
        Initialize the provider with necessary setup.
        
        Raises:
            ValueError: If the API key is not found.
        """
        self.api_key = os.environ.get(self.api_key_env)
        if not self.api_key:
            raise ValueError(f"API key not found in environment variable {self.api_key_env}")
        
        super().initialize()
    
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
        # Convert to chat format for OpenRouter
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, max_tokens, temperature, **kwargs)
    
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
        if not self.is_initialized:
            self.initialize()
        
        url = f"{self.BASE_URL}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        # Add any additional parameters
        for key, value in kwargs.items():
            payload[key] = value
        
        try:
            response = self._post_json(url, payload, headers)
            
            # Extract the response text
            if "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"]
                
                # Extract metadata
                metadata = {
                    "model": response.get("model", self.model),
                    "usage": response.get("usage", {}),
                    "id": response.get("id", ""),
                    "provider": self.name
                }
                
                return content, metadata
            else:
                raise Exception(f"Unexpected response format from OpenRouter: {response}")
                
        except Exception as e:
            logger.error(f"OpenRouter API call failed: {e}")
            raise
