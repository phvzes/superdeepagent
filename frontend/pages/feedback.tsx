
import Head from 'next/head';
import { useState } from 'react';
import FeedbackPanel from '../components/feedback/FeedbackPanel';

export default function FeedbackPage() {
  // In a real implementation, this would come from route params or query
  const [agentId, setAgentId] = useState('agent-123');

  return (
    <div className="min-h-screen bg-background">
      <Head>
        <title>Feedback System | SuperDeepAgent</title>
        <meta name="description" content="SuperDeepAgent Feedback System" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-primary mb-8">
          Feedback System
        </h1>

        <FeedbackPanel agentId={agentId} />
      </main>
    </div>
  );
}
