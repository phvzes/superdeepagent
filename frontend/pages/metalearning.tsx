
import Head from 'next/head';
import MetaLearningDashboard from '../components/metalearning/MetaLearningDashboard';

export default function MetaLearningPage() {
  return (
    <div className="min-h-screen bg-background">
      <Head>
        <title>Meta-Learning Framework | SuperDeepAgent</title>
        <meta name="description" content="SuperDeepAgent Meta-Learning Framework" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-primary mb-8">
          Meta-Learning Framework
        </h1>

        <MetaLearningDashboard />
      </main>
    </div>
  );
}
