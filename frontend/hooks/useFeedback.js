
import useSWR from 'swr';
import axios from 'axios';

// API endpoints
const API_ENDPOINTS = {
  getFeedback: (agentId, timeRange) => `/api/feedback/agent/${agentId}?timeRange=${timeRange}`,
  submitFeedback: '/api/feedback/submit',
  getFeedbackMetrics: (timeRange) => `/api/feedback/metrics?timeRange=${timeRange}`,
};

// Fetcher function for SWR
const fetcher = (url) => axios.get(url).then(res => res.data);

export function useFeedback(agentId, timeRange = 'month') {
  const { data, error, mutate } = useSWR(
    API_ENDPOINTS.getFeedback(agentId, timeRange),
    fetcher
  );

  const submitFeedback = async (feedbackData) => {
    try {
      const response = await axios.post(API_ENDPOINTS.submitFeedback, {
        ...feedbackData,
        agentId,
      });

      // Revalidate the cache after submission
      mutate();

      return response.data;
    } catch (error) {
      console.error('Error submitting feedback:', error);
      throw error;
    }
  };

  return {
    feedback: data,
    isLoading: !error && !data,
    isError: error,
    submitFeedback,
    mutate,
  };
}

export function useFeedbackMetrics(timeRange = 'month') {
  const { data, error } = useSWR(
    API_ENDPOINTS.getFeedbackMetrics(timeRange),
    fetcher
  );

  return {
    metrics: data,
    isLoading: !error && !data,
    isError: error,
  };
}
