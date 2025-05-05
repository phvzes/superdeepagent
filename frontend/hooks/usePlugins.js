import { useState, useEffect, useCallback } from 'react';
import pluginApi from '../api/plugin_api';

export const usePlugins = () => {
  const [plugins, setPlugins] = useState([]);
  const [selectedPlugin, setSelectedPlugin] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all plugins
  const fetchPlugins = useCallback(async () => {
    try {
      setLoading(true);
      const data = await pluginApi.getPlugins();
      setPlugins(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch plugins');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch a specific plugin
  const fetchPlugin = useCallback(async (pluginId) => {
    try {
      setLoading(true);
      const data = await pluginApi.getPlugin(pluginId);
      setSelectedPlugin(data);
      setError(null);
    } catch (err) {
      setError(`Failed to fetch plugin ${pluginId}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch plugin logs
  const fetchPluginLogs = useCallback(async () => {
    try {
      setLoading(true);
      const data = await pluginApi.getPluginLogs();
      setLogs(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch plugin logs');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Toggle plugin activation status
  const togglePluginStatus = useCallback(async (plugin) => {
    try {
      setLoading(true);
      if (plugin.active) {
        await pluginApi.deactivatePlugin(plugin.id);
      } else {
        await pluginApi.activatePlugin(plugin.id);
      }
      await fetchPlugins(); // Refresh the list
      setError(null);
    } catch (err) {
      setError(`Failed to ${plugin.active ? 'deactivate' : 'activate'} plugin`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [fetchPlugins]);

  // Update plugin configuration
  const updatePluginConfig = useCallback(async (pluginId, config) => {
    try {
      setLoading(true);
      await pluginApi.updatePluginConfig(pluginId, config);
      await fetchPlugins(); // Refresh the list
      if (selectedPlugin && selectedPlugin.id === pluginId) {
        await fetchPlugin(pluginId); // Refresh the selected plugin
      }
      setError(null);
    } catch (err) {
      setError('Failed to update plugin configuration');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [fetchPlugins, fetchPlugin, selectedPlugin]);

  // Send message to plugin
  const sendPluginMessage = useCallback(async (pluginId, message) => {
    try {
      setLoading(true);
      await pluginApi.sendPluginMessage(pluginId, message);
      setError(null);
    } catch (err) {
      setError('Failed to send message to plugin');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Load plugins on initial render
  useEffect(() => {
    fetchPlugins();
  }, [fetchPlugins]);

  return {
    plugins,
    selectedPlugin,
    logs,
    loading,
    error,
    fetchPlugins,
    fetchPlugin,
    fetchPluginLogs,
    togglePluginStatus,
    updatePluginConfig,
    sendPluginMessage,
    setSelectedPlugin
  };
};

export default usePlugins;
