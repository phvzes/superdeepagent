
import useSWR from 'swr';
import axios from 'axios';

// API endpoints
const API_ENDPOINTS = {
  getImprovements: (agentId) => `/api/improvements/agent/${agentId}`,
  applyImprovement: '/api/improvements/apply',
  dismissImprovement: '/api/improvements/dismiss',
  getImprovementHistory: (agentId) => `/api/improvements/history/${agentId}`,
};

// Fetcher function for SWR
const fetcher = (url) => axios.get(url).then(res => res.data);

export function useImprovements(agentId) {
  const { data, error, mutate } = useSWR(
    API_ENDPOINTS.getImprovements(agentId),
    fetcher
  );

  const applyImprovement = async (improvementId) => {
    try {
      const response = await axios.post(API_ENDPOINTS.applyImprovement, {
        improvementId,
        agentId,
      });

      // Revalidate the cache after application
      mutate();

      return response.data;
    } catch (error) {
      console.error('Error applying improvement:', error);
      throw error;
    }
  };

  const dismissImprovement = async (improvementId) => {
    try {
      const response = await axios.post(API_ENDPOINTS.dismissImprovement, {
        improvementId,
        agentId,
      });

      // Revalidate the cache after dismissal
      mutate();

      return response.data;
    } catch (error) {
      console.error('Error dismissing improvement:', error);
      throw error;
    }
  };

  return {
    improvements: data,
    isLoading: !error && !data,
    isError: error,
    applyImprovement,
    dismissImprovement,
    mutate,
  };
}

export function useImprovementHistory(agentId) {
  const { data, error } = useSWR(
    API_ENDPOINTS.getImprovementHistory(agentId),
    fetcher
  );

  return {
    history: data,
    isLoading: !error && !data,
    isError: error,
  };
}
