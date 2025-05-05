"""
Sample Plugin for SuperDeepAgent

This is a demonstration of how to create a plugin for the SuperDeepAgent system.
"""

class SamplePlugin:
    """Sample plugin implementation"""
    
    def __init__(self):
        self.name = "sample_plugin"
        self.description = "A sample plugin demonstrating the plugin system"
        self.version = "0.1.0"
        self.enabled = False
        self.config = {
            "sample_parameter": "default_value"
        }
    
    def activate(self):
        """Activate the plugin"""
        self.enabled = True
        return True
    
    def deactivate(self):
        """Deactivate the plugin"""
        self.enabled = False
        return True
    
    def get_config(self):
        """Get the plugin configuration"""
        return self.config
    
    def update_config(self, new_config):
        """Update the plugin configuration"""
        self.config.update(new_config)
        return True
    
    def execute(self, input_data):
        """Execute the plugin functionality"""
        if not self.enabled:
            return {"error": "Plugin is not activated"}
        
        # Sample functionality - echo the input with a prefix
        return {
            "result": f"Sample plugin processed: {input_data}",
            "config_used": self.config
        }

# Plugin instance that will be loaded by the plugin system
plugin_instance = SamplePlugin()
