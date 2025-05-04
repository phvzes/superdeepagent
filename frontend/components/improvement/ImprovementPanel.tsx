
import { useState } from 'react';
import { Card, Title, BarChart, Grid, Tab, TabGroup, TabList, TabPanel, TabPanels, Badge } from '@tremor/react';
import useSWR from 'swr';

// Mock data - replace with actual API calls
const mockImprovementData = {
  suggestions: [
    { 
      id: 1, 
      title: 'Enhance Response Clarity', 
      description: 'Improve clarity by using simpler language and more examples.',
      impact: 'high',
      category: 'communication',
      status: 'pending'
    },
    { 
      id: 2, 
      title: 'Optimize Knowledge Retrieval', 
      description: 'Implement more efficient knowledge retrieval to reduce response time.',
      impact: 'medium',
      category: 'performance',
      status: 'pending'
    },
    { 
      id: 3, 
      title: 'Expand Domain Knowledge', 
      description: 'Add more specialized knowledge in the finance domain.',
      impact: 'medium',
      category: 'knowledge',
      status: 'pending'
    },
  ],
  history: [
    { 
      id: 101, 
      title: 'Improved Error Handling', 
      description: 'Enhanced error handling for edge cases.',
      impact: 'medium',
      category: 'reliability',
      status: 'applied',
      appliedDate: '2023-05-01',
      performanceChange: '+12%'
    },
    { 
      id: 102, 
      title: 'Response Time Optimization', 
      description: 'Optimized response generation algorithm.',
      impact: 'high',
      category: 'performance',
      status: 'applied',
      appliedDate: '2023-04-15',
      performanceChange: '+8%'
    },
  ],
  metrics: [
    { category: 'Accuracy', before: 82, after: 88 },
    { category: 'Response Time', before: 75, after: 92 },
    { category: 'Reliability', before: 80, after: 85 },
    { category: 'Knowledge Coverage', before: 70, after: 78 },
  ]
};

export default function ImprovementPanel({ agentId }) {
  // Replace with actual API call
  // const { data, error } = useSWR(`/api/improvements/agent/${agentId}`);
  const data = mockImprovementData; // Mock data

  if (!data) return <div>Loading...</div>;

  const getImpactColor = (impact) => {
    switch (impact) {
      case 'high': return 'rose';
      case 'medium': return 'amber';
      case 'low': return 'emerald';
      default: return 'gray';
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'performance': return 'cyan';
      case 'reliability': return 'emerald';
      case 'communication': return 'violet';
      case 'knowledge': return 'amber';
      default: return 'gray';
    }
  };

  return (
    <div className="space-y-6">
      <Title>Agent Improvements</Title>

      <TabGroup>
        <TabList className="mb-4">
          <Tab>Suggested Improvements</Tab>
          <Tab>Applied Improvements</Tab>
          <Tab>Performance Impact</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <div className="space-y-4">
              {data.suggestions.map((item) => (
                <Card key={item.id} className="p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-medium">{item.title}</h3>
                    <div className="flex space-x-2">
                      <Badge color={getImpactColor(item.impact)}>
                        {item.impact} impact
                      </Badge>
                      <Badge color={getCategoryColor(item.category)}>
                        {item.category}
                      </Badge>
                    </div>
                  </div>
                  <p className="mb-4 text-gray-300">{item.description}</p>
                  <div className="flex justify-end space-x-2">
                    <button className="px-3 py-1 bg-surface rounded-md">Dismiss</button>
                    <button className="btn-primary">Apply Improvement</button>
                  </div>
                </Card>
              ))}
            </div>
          </TabPanel>

          <TabPanel>
            <div className="space-y-4">
              {data.history.map((item) => (
                <Card key={item.id} className="p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-medium">{item.title}</h3>
                    <div className="flex space-x-2">
                      <Badge color={getImpactColor(item.impact)}>
                        {item.impact} impact
                      </Badge>
                      <Badge color={getCategoryColor(item.category)}>
                        {item.category}
                      </Badge>
                      <Badge color="emerald">
                        {item.performanceChange}
                      </Badge>
                    </div>
                  </div>
                  <p className="mb-2 text-gray-300">{item.description}</p>
                  <p className="text-sm text-gray-400">Applied on {item.appliedDate}</p>
                </Card>
              ))}
            </div>
          </TabPanel>

          <TabPanel>
            <Card>
              <Title>Performance Before & After Improvements</Title>
              <BarChart
                data={data.metrics}
                index="category"
                categories={["before", "after"]}
                colors={["gray", "cyan"]}
                valueFormatter={(value) => `${value}%`}
                yAxisWidth={40}
                className="mt-6 h-80"
              />
            </Card>
          </TabPanel>
        </TabPanels>
      </TabGroup>
    </div>
  );
}
