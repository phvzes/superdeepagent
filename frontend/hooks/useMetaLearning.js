
import useSWR from 'swr';
import axios from 'axios';

// API endpoints
const API_ENDPOINTS = {
  getMetrics: (timeRange) => `/api/meta-learning/metrics?timeRange=${timeRange}`,
  getKnowledgeGraph: '/api/meta-learning/knowledge-graph',
  getSettings: '/api/meta-learning/settings',
  updateSettings: '/api/meta-learning/settings',
};

// Fetcher function for SWR
const fetcher = (url) => axios.get(url).then(res => res.data);

export function useMetaLearningMetrics(timeRange = 'month') {
  const { data, error } = useSWR(
    API_ENDPOINTS.getMetrics(timeRange),
    fetcher
  );

  return {
    metrics: data,
    isLoading: !error && !data,
    isError: error,
  };
}

export function useKnowledgeGraph() {
  const { data, error } = useSWR(
    API_ENDPOINTS.getKnowledgeGraph,
    fetcher
  );

  return {
    graph: data,
    isLoading: !error && !data,
    isError: error,
  };
}

export function useMetaLearningSettings() {
  const { data, error, mutate } = useSWR(
    API_ENDPOINTS.getSettings,
    fetcher
  );

  const updateSettings = async (settings) => {
    try {
      const response = await axios.post(API_ENDPOINTS.updateSettings, settings);

      // Revalidate the cache after update
      mutate();

      return response.data;
    } catch (error) {
      console.error('Error updating meta-learning settings:', error);
      throw error;
    }
  };

  return {
    settings: data,
    isLoading: !error && !data,
    isError: error,
    updateSettings,
  };
}
