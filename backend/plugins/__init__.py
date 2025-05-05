"""
SuperDeepAgent Plugin System

This module provides the core functionality for the plugin system,
allowing users to extend the functionality of SuperDeepAgent through custom plugins.
"""

import os
import importlib.util
import sys
from typing import Dict, List, Any, Optional

class PluginManager:
    """Manager for SuperDeepAgent plugins"""
    
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_plugins")
        self.discover_plugins()
    
    def discover_plugins(self) -> None:
        """Discover available plugins in the user_plugins directory"""
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir, exist_ok=True)
            return
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]  # Remove .py extension
                self.load_plugin(plugin_name)
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin by name"""
        plugin_path = os.path.join(self.plugin_dir, f"{plugin_name}.py")
        
        if not os.path.exists(plugin_path):
            return False
        
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                return False
                
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)
            
            if hasattr(module, "plugin_instance"):
                self.plugins[plugin_name] = module.plugin_instance
                return True
            return False
        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {str(e)}")
            return False
    
    def get_plugin(self, plugin_name: str) -> Optional[Any]:
        """Get a plugin instance by name"""
        return self.plugins.get(plugin_name)
    
    def get_all_plugins(self) -> Dict[str, Any]:
        """Get all loaded plugins"""
        return self.plugins
    
    def activate_plugin(self, plugin_name: str) -> bool:
        """Activate a plugin by name"""
        plugin = self.get_plugin(plugin_name)
        if plugin and hasattr(plugin, "activate"):
            return plugin.activate()
        return False
    
    def deactivate_plugin(self, plugin_name: str) -> bool:
        """Deactivate a plugin by name"""
        plugin = self.get_plugin(plugin_name)
        if plugin and hasattr(plugin, "deactivate"):
            return plugin.deactivate()
        return False
    
    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """Get configuration for a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin and hasattr(plugin, "get_config"):
            return plugin.get_config()
        return {}
    
    def update_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> bool:
        """Update configuration for a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin and hasattr(plugin, "update_config"):
            return plugin.update_config(config)
        return False
    
    def execute_plugin(self, plugin_name: str, input_data: Any) -> Any:
        """Execute a plugin with the given input data"""
        plugin = self.get_plugin(plugin_name)
        if plugin and hasattr(plugin, "execute"):
            return plugin.execute(input_data)
        return {"error": f"Plugin {plugin_name} not found or does not have execute method"}

# Create a singleton instance of the plugin manager
plugin_manager = PluginManager()
