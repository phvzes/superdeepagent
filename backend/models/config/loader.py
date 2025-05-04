"""
Configuration loader for the LLM pipeline in SuperDeepAgent.

This module provides functionality for loading and validating
LLM pipeline configuration from YAML files.
"""

import os
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LLMConfig:
    """
    Configuration for an LLM provider.
    
    Attributes:
        provider: The provider type.
        model: The model identifier.
        api_key_env: The environment variable name for the API key.
        endpoint: The API endpoint (for local models).
        fallback_to: The name of the fallback provider.
        additional_params: Additional provider-specific parameters.
    """
    provider: str
    model: str
    api_key_env: Optional[str] = None
    endpoint: Optional[str] = None
    fallback_to: Optional[str] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        result = {
            "provider": self.provider,
            "model": self.model,
        }
        
        if self.api_key_env:
            result["api_key_env"] = self.api_key_env
        
        if self.endpoint:
            result["endpoint"] = self.endpoint
        
        if self.fallback_to:
            result["fallback_to"] = self.fallback_to
        
        # Add additional parameters
        result.update(self.additional_params)
        
        return result

@dataclass
class LLMPipelineConfig:
    """
    Configuration for the LLM pipeline.
    
    Attributes:
        llms: Dictionary of LLM configurations by name.
    """
    llms: Dict[str, LLMConfig] = field(default_factory=dict)
    
    def get_llm_config(self, name: str) -> Optional[LLMConfig]:
        """
        Get the LLM configuration by name.
        
        Args:
            name: The name of the LLM configuration.
            
        Returns:
            The LLM configuration, or None if not found.
        """
        return self.llms.get(name)
    
    def get_default_llm_config(self) -> Optional[LLMConfig]:
        """
        Get the default LLM configuration.
        
        Returns:
            The default LLM configuration, or None if not found.
        """
        return self.get_llm_config("default")
    
    def get_fallback_chain(self, start_name: str) -> List[LLMConfig]:
        """
        Get the fallback chain starting from the given LLM.
        
        Args:
            start_name: The name of the starting LLM.
            
        Returns:
            A list of LLM configurations in the fallback chain.
        """
        result = []
        visited = set()
        current_name = start_name
        
        while current_name and current_name not in visited:
            visited.add(current_name)
            current_config = self.get_llm_config(current_name)
            
            if not current_config:
                break
            
            result.append(current_config)
            current_name = current_config.fallback_to
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        return {
            "llms": {
                name: config.to_dict()
                for name, config in self.llms.items()
            }
        }


def load_llm_config(config_path: Optional[str] = None) -> LLMPipelineConfig:
    """
    Load the LLM pipeline configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file.
            If None, uses the default path.
            
    Returns:
        The LLM pipeline configuration.
        
    Raises:
        FileNotFoundError: If the configuration file is not found.
        ValueError: If the configuration is invalid.
    """
    if config_path is None:
        # Use default path
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "config",
            "llm_pipeline.yaml"
        )
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
    except Exception as e:
        raise ValueError(f"Failed to load configuration file: {e}")
    
    if not isinstance(config_data, dict) or "llms" not in config_data:
        raise ValueError("Invalid configuration format: 'llms' section not found")
    
    llms_config = {}
    
    for name, llm_data in config_data["llms"].items():
        if not isinstance(llm_data, dict):
            logger.warning(f"Invalid LLM configuration for {name}: not a dictionary")
            continue
        
        provider = llm_data.get("provider")
        model = llm_data.get("model")
        
        if not provider or not model:
            logger.warning(f"Invalid LLM configuration for {name}: missing provider or model")
            continue
        
        # Extract known fields
        api_key_env = llm_data.get("api_key_env")
        endpoint = llm_data.get("endpoint")
        fallback_to = llm_data.get("fallback_to")
        
        # Extract additional parameters
        additional_params = {
            k: v for k, v in llm_data.items()
            if k not in ["provider", "model", "api_key_env", "endpoint", "fallback_to"]
        }
        
        llms_config[name] = LLMConfig(
            provider=provider,
            model=model,
            api_key_env=api_key_env,
            endpoint=endpoint,
            fallback_to=fallback_to,
            additional_params=additional_params
        )
    
    return LLMPipelineConfig(llms=llms_config)
