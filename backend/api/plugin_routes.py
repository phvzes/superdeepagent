from fastapi import APIRouter, HTTPException, Depends
import os
import importlib.util
import sys
from typing import List, Dict, Any

# Create router
router = APIRouter(
    prefix="/api/plugins",
    tags=["plugins"],
    responses={404: {"description": "Not found"}},
)

# Plugin management functions
def get_available_plugins() -> List[Dict[str, Any]]:
    """Get list of available plugins in the user_plugins directory"""
    plugins = []
    plugin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_plugins")
    
    if not os.path.exists(plugin_dir):
        return plugins
    
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            plugin_name = filename[:-3]  # Remove .py extension
            plugins.append({
                "name": plugin_name,
                "status": "inactive",  # Default status
                "path": os.path.join(plugin_dir, filename)
            })
    
    return plugins

# API Routes
@router.get("/")
async def list_plugins():
    """List all available plugins"""
    plugins = get_available_plugins()
    return {"plugins": plugins}

@router.post("/{plugin_name}/activate")
async def activate_plugin(plugin_name: str):
    """Activate a specific plugin"""
    plugins = get_available_plugins()
    for plugin in plugins:
        if plugin["name"] == plugin_name:
            # Here would be the logic to activate the plugin
            return {"status": "success", "message": f"Plugin {plugin_name} activated"}
    
    raise HTTPException(status_code=404, detail=f"Plugin {plugin_name} not found")

@router.post("/{plugin_name}/deactivate")
async def deactivate_plugin(plugin_name: str):
    """Deactivate a specific plugin"""
    plugins = get_available_plugins()
    for plugin in plugins:
        if plugin["name"] == plugin_name:
            # Here would be the logic to deactivate the plugin
            return {"status": "success", "message": f"Plugin {plugin_name} deactivated"}
    
    raise HTTPException(status_code=404, detail=f"Plugin {plugin_name} not found")

@router.get("/{plugin_name}/config")
async def get_plugin_config(plugin_name: str):
    """Get configuration for a specific plugin"""
    plugins = get_available_plugins()
    for plugin in plugins:
        if plugin["name"] == plugin_name:
            # Here would be the logic to get plugin configuration
            return {"config": {}, "plugin_name": plugin_name}
    
    raise HTTPException(status_code=404, detail=f"Plugin {plugin_name} not found")

@router.post("/{plugin_name}/config")
async def update_plugin_config(plugin_name: str, config: Dict[str, Any]):
    """Update configuration for a specific plugin"""
    plugins = get_available_plugins()
    for plugin in plugins:
        if plugin["name"] == plugin_name:
            # Here would be the logic to update plugin configuration
            return {"status": "success", "message": f"Plugin {plugin_name} configuration updated"}
    
    raise HTTPException(status_code=404, detail=f"Plugin {plugin_name} not found")
