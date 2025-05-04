
import { useState } from 'react';
import { Card, Title, LineChart, BarChart, Grid, Tab, TabGroup, TabList, TabPanel, TabPanels } from '@tremor/react';
import useSWR from 'swr';

// Mock data - replace with actual API calls
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

export default function FeedbackPanel({ agentId }) {
  const [timeRange, setTimeRange] = useState('month');

  // Replace with actual API call
  // const { data, error } = useSWR(`/api/feedback/agent/${agentId}?timeRange=${timeRange}`);
  const data = mockFeedbackData; // Mock data

  if (!data) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Title>Agent Feedback</Title>
        <div className="flex space-x-2">
          <button 
            className={`px-3 py-1 rounded-md ${timeRange === 'week' ? 'bg-primary text-black' : 'bg-surface'}`}
            onClick={() => setTimeRange('week')}
          >
            Week
          </button>
          <button 
            className={`px-3 py-1 rounded-md ${timeRange === 'month' ? 'bg-primary text-black' : 'bg-surface'}`}
            onClick={() => setTimeRange('month')}
          >
            Month
          </button>
          <button 
            className={`px-3 py-1 rounded-md ${timeRange === 'year' ? 'bg-primary text-black' : 'bg-surface'}`}
            onClick={() => setTimeRange('year')}
          >
            Year
          </button>
        </div>
      </div>

      <TabGroup>
        <TabList className="mb-4">
          <Tab>Overview</Tab>
          <Tab>Categories</Tab>
          <Tab>Recent Feedback</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <Card>
              <Title>Feedback Metrics</Title>
              <LineChart
                data={data.metrics}
                index="date"
                categories={["userSatisfaction", "taskCompletion"]}
                colors={["cyan", "amber"]}
                valueFormatter={(value) => `${value}%`}
                yAxisWidth={40}
                className="mt-6 h-80"
              />
            </Card>
          </TabPanel>

          <TabPanel>
            <Card>
              <Title>Feedback by Category</Title>
              <BarChart
                data={data.categories}
                index="name"
                categories={["value"]}
                colors={["cyan"]}
                valueFormatter={(value) => `${value}%`}
                yAxisWidth={40}
                className="mt-6 h-80"
              />
            </Card>
          </TabPanel>

          <TabPanel>
            <Card>
              <Title>Recent Feedback</Title>
              <div className="mt-6 space-y-4">
                {data.recent.map((item) => (
                  <div key={item.id} className="p-4 bg-surface rounded-lg">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-gray-400">{item.timestamp}</span>
                      <span className="flex items-center">
                        <span className="text-amber-400 mr-1">★</span>
                        {item.rating}
                      </span>
                    </div>
                    <p>{item.comment}</p>
                  </div>
                ))}
              </div>
            </Card>
          </TabPanel>
        </TabPanels>
      </TabGroup>

      <Card>
        <Title>Submit Feedback</Title>
        <div className="mt-4 space-y-4">
          <div>
            <label className="block mb-2 text-sm font-medium">Rating</label>
            <div className="flex space-x-1">
              {[1, 2, 3, 4, 5].map((rating) => (
                <button key={rating} className="text-2xl text-amber-400">
                  ★
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block mb-2 text-sm font-medium">Comment</label>
            <textarea 
              className="w-full p-2 bg-background border border-gray-700 rounded-md"
              rows={3}
              placeholder="Enter your feedback..."
            />
          </div>

          <button className="btn-primary">Submit Feedback</button>
        </div>
      </Card>
    </div>
  );
}
