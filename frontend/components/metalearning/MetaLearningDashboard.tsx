
import { useState } from 'react';
import { Card, Title, LineChart, BarChart, DonutChart, Grid, Tab, TabGroup, TabList, TabPanel, TabPanels, Badge, Metric, Text } from '@tremor/react';
import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';
import useSWR from 'swr';

// Mock data - replace with actual API calls
const mockMetaLearningData = {
  metrics: {
    learningEfficiency: [
      { date: '2023-01', newTasks: 65, similarTasks: 82 },
      { date: '2023-02', newTasks: 68, similarTasks: 85 },
      { date: '2023-03', newTasks: 72, similarTasks: 87 },
      { date: '2023-04', newTasks: 75, similarTasks: 90 },
      { date: '2023-05', newTasks: 80, similarTasks: 93 },
    ],
    knowledgeTransfer: [
      { agentType: 'Customer Service', direct: 75, adapted: 62 },
      { agentType: 'Research', direct: 82, adapted: 70 },
      { agentType: 'Creative', direct: 68, adapted: 58 },
      { agentType: 'Technical', direct: 88, adapted: 76 },
    ],
    adaptationSuccess: [
      { category: 'Successful', value: 68 },
      { category: 'Partial', value: 22 },
      { category: 'Failed', value: 10 },
    ]
  },
  knowledgeGraph: {
    nodes: [
      { id: '1', data: { label: 'Agent A' }, position: { x: 250, y: 5 } },
      { id: '2', data: { label: 'Agent B' }, position: { x: 100, y: 100 } },
      { id: '3', data: { label: 'Agent C' }, position: { x: 400, y: 100 } },
      { id: '4', data: { label: 'Agent D' }, position: { x: 250, y: 200 } },
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2', animated: true, label: '85%' },
      { id: 'e1-3', source: '1', target: '3', animated: true, label: '72%' },
      { id: 'e2-4', source: '2', target: '4', animated: true, label: '65%' },
      { id: 'e3-4', source: '3', target: '4', animated: true, label: '78%' },
    ]
  },
  settings: {
    learningRate: 0.05,
    knowledgeRetention: 0.8,
    adaptationThreshold: 0.6,
    transferWeight: 0.7
  }
};

export default function MetaLearningDashboard() {
  const [timeRange, setTimeRange] = useState('month');

  // Replace with actual API call
  // const { data, error } = useSWR(`/api/meta-learning/metrics?timeRange=${timeRange}`);
  const data = mockMetaLearningData; // Mock data

  if (!data) return <div>Loading...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Title>Meta-Learning Framework</Title>
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

      <Grid numItems={1} numItemsSm={2} numItemsLg={3} className="gap-6">
        <Card>
          <Title>Learning Efficiency</Title>
          <LineChart
            data={data.metrics.learningEfficiency}
            index="date"
            categories={["newTasks", "similarTasks"]}
            colors={["cyan", "amber"]}
            valueFormatter={(value) => `${value}%`}
            yAxisWidth={40}
            className="mt-6 h-64"
          />
        </Card>

        <Card>
          <Title>Knowledge Transfer</Title>
          <BarChart
            data={data.metrics.knowledgeTransfer}
            index="agentType"
            categories={["direct", "adapted"]}
            colors={["violet", "indigo"]}
            valueFormatter={(value) => `${value}%`}
            yAxisWidth={40}
            className="mt-6 h-64"
          />
        </Card>

        <Card>
          <Title>Adaptation Success</Title>
          <DonutChart
            data={data.metrics.adaptationSuccess}
            category="value"
            index="category"
            colors={["emerald", "amber", "rose"]}
            valueFormatter={(value) => `${value}%`}
            className="mt-6 h-64"
          />
        </Card>
      </Grid>

      <Card>
        <Title>Knowledge Transfer Network</Title>
        <div style={{ height: 400 }} className="mt-4">
          <ReactFlow
            nodes={data.knowledgeGraph.nodes}
            edges={data.knowledgeGraph.edges}
            fitView
          >
            <Background />
            <Controls />
          </ReactFlow>
        </div>
      </Card>

      <Card>
        <Title>Meta-Learning Configuration</Title>
        <Grid numItems={1} numItemsSm={2} numItemsLg={4} className="gap-6 mt-4">
          <Card>
            <Text>Learning Rate</Text>
            <Metric>{data.settings.learningRate}</Metric>
            <input 
              type="range" 
              min="0.01" 
              max="0.1" 
              step="0.01" 
              value={data.settings.learningRate}
              className="w-full mt-2"
              // onChange handler would go here
            />
          </Card>

          <Card>
            <Text>Knowledge Retention</Text>
            <Metric>{data.settings.knowledgeRetention}</Metric>
            <input 
              type="range" 
              min="0.5" 
              max="1" 
              step="0.05" 
              value={data.settings.knowledgeRetention}
              className="w-full mt-2"
              // onChange handler would go here
            />
          </Card>

          <Card>
            <Text>Adaptation Threshold</Text>
            <Metric>{data.settings.adaptationThreshold}</Metric>
            <input 
              type="range" 
              min="0.3" 
              max="0.9" 
              step="0.05" 
              value={data.settings.adaptationThreshold}
              className="w-full mt-2"
              // onChange handler would go here
            />
          </Card>

          <Card>
            <Text>Transfer Weight</Text>
            <Metric>{data.settings.transferWeight}</Metric>
            <input 
              type="range" 
              min="0.3" 
              max="0.9" 
              step="0.05" 
              value={data.settings.transferWeight}
              className="w-full mt-2"
              // onChange handler would go here
            />
          </Card>
        </Grid>

        <div className="flex justify-end mt-6">
          <button className="btn-primary">Save Configuration</button>
        </div>
      </Card>
    </div>
  );
}
