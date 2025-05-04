"""
Ollama provider for LLM interactions in SuperDeepAgent.

This module implements the Ollama API integration for accessing
local LLM models through the Ollama server.
"""

import logging
from typing import Dict, List, Any, Optional, Union, Tuple

from .base import BaseProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaProvider(BaseProvider):
    """
    Ollama provider for LLM interactions.
    
    Implements the Ollama API for accessing local LLM models.
    """
    
    def __init__(
        self,
        name: str,
        model: str,
        endpoint: str = "http://localhost:11434",
        **kwargs
    ):
        """
        Initialize the Ollama provider.
        
        Args:
            name: The name of the provider.
            model: The model identifier.
            endpoint: The Ollama API endpoint.
            **kwargs: Additional provider-specific configuration.
        """
        super().__init__(name, model, **kwargs)
        self.endpoint = endpoint.rstrip("/")  # Remove trailing slash if present
        
    def initialize(self) -> None:
        """Initialize the provider with necessary setup."""
        # No special initialization needed for Ollama
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
        url = f"{self.endpoint}/api/generate"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        # Add any additional parameters
        for key, value in kwargs.items():
            payload[key] = value
        
        try:
            response = self._post_json(url, payload, headers)
            
            # Extract the response text
            if "response" in response:
                content = response["response"]
                
                # Extract metadata
                metadata = {
                    "model": self.model,
                    "provider": self.name,
                    "eval_count": response.get("eval_count", 0),
                    "eval_duration": response.get("eval_duration", 0)
                }
                
                return content, metadata
            else:
                raise Exception(f"Unexpected response format from Ollama: {response}")
                
        except Exception as e:
            logger.error(f"Ollama API call failed: {e}")
            raise
    
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
        url = f"{self.endpoint}/api/chat"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            }
        }
        
        # Add any additional parameters to options
        for key, value in kwargs.items():
            if key not in ["model", "messages", "options"]:
                if "options" not in payload:
                    payload["options"] = {}
                payload["options"][key] = value
        
        try:
            response = self._post_json(url, payload, headers)
            
            # Extract the response text
            if "message" in response and "content" in response["message"]:
                content = response["message"]["content"]
                
                # Extract metadata
                metadata = {
                    "model": self.model,
                    "provider": self.name,
                    "eval_count": response.get("eval_count", 0),
                    "eval_duration": response.get("eval_duration", 0)
                }
                
                return content, metadata
            else:
                raise Exception(f"Unexpected response format from Ollama: {response}")
                
        except Exception as e:
            logger.error(f"Ollama API call failed: {e}")
            raise
