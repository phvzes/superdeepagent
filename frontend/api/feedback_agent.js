
// pages/api/feedback/agent/[agentId].js
export default function handler(req, res) {
  const { agentId } = req.query;
  const { timeRange = 'month' } = req.query;

  // Mock data - replace with actual database queries
  const mockFeedbackData = {
    metrics: [
      { date: '2023-01', userSatisfaction: 85, taskCompletion: 78 },
      { date: '2023-02', userSatisfaction: 87, taskCompletion: 82 },
      { date: '2023-03', userSatisfaction: 90, taskCompletion: 85 },
      { date: '2023-04', userSatisfaction: 92, taskCompletion: 88 },
      { date: '2023-05', userSatisfaction: 94, taskCompletion: 91 },
    ],
    categories: [
      { name: 'Accuracy', value: 85 },
      { name: 'Helpfulness', value: 92 },
      { name: 'Efficiency', value: 78 },
      { name: 'Clarity', value: 88 },
    ],
    recent: [
      { id: 1, timestamp: '2023-05-10', rating: 4.5, comment: 'Very helpful response, but took a bit too long.' },
      { id: 2, timestamp: '2023-05-09', rating: 5, comment: 'Perfect answer, exactly what I needed!' },
      { id: 3, timestamp: '2023-05-08', rating: 3, comment: 'Answer was technically correct but hard to understand.' },
    ]
  };

  res.status(200).json(mockFeedbackData);
}
