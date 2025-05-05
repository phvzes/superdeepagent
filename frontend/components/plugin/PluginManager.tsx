import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

interface Plugin {
  id: string;
  name: string;
  description: string;
  active: boolean;
  config: Record<string, any>;
}

const PluginManager: React.FC = () => {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [selectedPlugin, setSelectedPlugin] = useState<Plugin | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const router = useRouter();

  useEffect(() => {
    fetchPlugins();
  }, []);

  const fetchPlugins = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/plugins');
      setPlugins(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch plugins');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchPluginLogs = async () => {
    try {
      const response = await axios.get('/api/plugins/logs');
      setLogs(response.data);
    } catch (err) {
      console.error('Failed to fetch plugin logs:', err);
    }
  };

  const togglePluginStatus = async (plugin: Plugin) => {
    try {
      const endpoint = plugin.active 
        ? `/api/plugins/${plugin.id}/deactivate`
        : `/api/plugins/${plugin.id}/activate`;
      
      await axios.post(endpoint);
      fetchPlugins(); // Refresh the list
    } catch (err) {
      console.error(`Failed to ${plugin.active ? 'deactivate' : 'activate'} plugin:`, err);
    }
  };

  const updatePluginConfig = async (pluginId: string, config: Record<string, any>) => {
    try {
      await axios.patch(`/api/plugins/${pluginId}/config`, { config });
      fetchPlugins(); // Refresh the list
    } catch (err) {
      console.error('Failed to update plugin config:', err);
    }
  };

  const sendMessageToPlugin = async (pluginId: string, message: string) => {
    try {
      await axios.post(`/api/plugins/${pluginId}/message`, { message });
    } catch (err) {
      console.error('Failed to send message to plugin:', err);
    }
  };

  // Plugin List Component
  const PluginList = () => (
    <div className="bg-white shadow rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Available Plugins</h2>
      {loading ? (
        <p>Loading plugins...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <ul className="space-y-2">
          {plugins.map(plugin => (
            <li 
              key={plugin.id}
              className="border p-3 rounded hover:bg-gray-50 cursor-pointer flex justify-between items-center"
              onClick={() => setSelectedPlugin(plugin)}
            >
              <div>
                <h3 className="font-medium">{plugin.name}</h3>
                <p className="text-sm text-gray-600">{plugin.description}</p>
              </div>
              <div className="flex items-center">
                <span className={`inline-block w-3 h-3 rounded-full mr-2 ${plugin.active ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <button 
                  className={`px-3 py-1 rounded text-white text-sm ${plugin.active ? 'bg-red-500' : 'bg-green-500'}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    togglePluginStatus(plugin);
                  }}
                >
                  {plugin.active ? 'Deactivate' : 'Activate'}
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );

  // Plugin Detail Component
  const PluginDetail = () => {
    if (!selectedPlugin) return null;

    const [config, setConfig] = useState(selectedPlugin.config);
    const [message, setMessage] = useState('');

    const handleConfigChange = (key: string, value: any) => {
      setConfig({ ...config, [key]: value });
    };

    const handleSaveConfig = () => {
      updatePluginConfig(selectedPlugin.id, config);
    };

    const handleSendMessage = () => {
      if (message.trim()) {
        sendMessageToPlugin(selectedPlugin.id, message);
        setMessage('');
      }
    };

    return (
      <div className="bg-white shadow rounded-lg p-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">{selectedPlugin.name}</h2>
          <button 
            className="text-gray-500 hover:text-gray-700"
            onClick={() => setSelectedPlugin(null)}
          >
            Back to List
          </button>
        </div>
        
        <div className="mb-4">
          <h3 className="font-medium mb-2">Description</h3>
          <p className="text-gray-600">{selectedPlugin.description}</p>
        </div>
        
        <div className="mb-4">
          <h3 className="font-medium mb-2">Configuration</h3>
          {Object.entries(config).map(([key, value]) => (
            <div key={key} className="mb-2">
              <label className="block text-sm font-medium text-gray-700">{key}</label>
              <input
                type={typeof value === 'number' ? 'number' : 'text'}
                value={value as string}
                onChange={(e) => handleConfigChange(key, e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              />
            </div>
          ))}
          <button
            onClick={handleSaveConfig}
            className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Save Configuration
          </button>
        </div>
        
        <div>
          <h3 className="font-medium mb-2">Send Message</h3>
          <div className="flex">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="flex-grow rounded-l-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              placeholder="Enter message..."
            />
            <button
              onClick={handleSendMessage}
              className="px-4 py-2 bg-green-500 text-white rounded-r hover:bg-green-600"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Plugin Logs Component
  const PluginLogs = () => (
    <div className="bg-white shadow rounded-lg p-4 mt-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Plugin Logs</h2>
        <button 
          onClick={fetchPluginLogs}
          className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
        >
          Refresh Logs
        </button>
      </div>
      <div className="bg-gray-100 p-3 rounded max-h-60 overflow-y-auto font-mono text-sm">
        {logs.length === 0 ? (
          <p className="text-gray-500">No logs available</p>
        ) : (
          logs.map((log, index) => (
            <div key={index} className="mb-1">
              {log}
            </div>
          ))
        )}
      </div>
    </div>
  );

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Plugin Manager</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <PluginList />
          <PluginLogs />
        </div>
        <div>
          <PluginDetail />
        </div>
      </div>
    </div>
  );
};

export default PluginManager;
