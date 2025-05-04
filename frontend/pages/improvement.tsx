
import Head from 'next/head';
import { useState } from 'react';
import ImprovementPanel from '../components/improvement/ImprovementPanel';

export default function ImprovementPage() {
  // In a real implementation, this would come from route params or query
  const [agentId, setAgentId] = useState('agent-123');

  return (
    <div className="min-h-screen bg-background">
      <Head>
        <title>Improvement System | SuperDeepAgent</title>
        <meta name="description" content="SuperDeepAgent Improvement System" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-primary mb-8">
          Improvement System
        </h1>

        <ImprovementPanel agentId={agentId} />
      </main>
    </div>
  );
}
