import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const pluginApi = {
  // Get all plugins
  getPlugins: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/plugins/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching plugins:', error);
      throw error;
    }
  },

  // Get a specific plugin by ID
  getPlugin: async (pluginId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/plugins/${pluginId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching plugin ${pluginId}:`, error);
      throw error;
    }
  },

  // Activate a plugin
  activatePlugin: async (pluginId) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/plugins/${pluginId}/activate`);
      return response.data;
    } catch (error) {
      console.error(`Error activating plugin ${pluginId}:`, error);
      throw error;
    }
  },

  // Deactivate a plugin
  deactivatePlugin: async (pluginId) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/plugins/${pluginId}/deactivate`);
      return response.data;
    } catch (error) {
      console.error(`Error deactivating plugin ${pluginId}:`, error);
      throw error;
    }
  },

  // Update plugin configuration
  updatePluginConfig: async (pluginId, config) => {
    try {
      const response = await axios.patch(`${API_BASE_URL}/api/plugins/${pluginId}/config`, { config });
      return response.data;
    } catch (error) {
      console.error(`Error updating plugin ${pluginId} config:`, error);
      throw error;
    }
  },

  // Send a message to a plugin
  sendPluginMessage: async (pluginId, message) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/plugins/${pluginId}/message`, { message });
      return response.data;
    } catch (error) {
      console.error(`Error sending message to plugin ${pluginId}:`, error);
      throw error;
    }
  },

  // Get plugin logs
  getPluginLogs: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/plugins/logs`);
      return response.data;
    } catch (error) {
      console.error('Error fetching plugin logs:', error);
      throw error;
    }
  }
};

export default pluginApi;
