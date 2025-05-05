
import Head from 'next/head';
import Link from 'next/link';
import styles from '../styles/Home.module.css';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Head>
        <title>SuperDeepAgent UI</title>
        <meta name="description" content="SuperDeepAgent Phase 3 UI" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-primary mb-8">
          SuperDeepAgent UI
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Link href="/feedback" className="card hover:bg-opacity-80 transition-colors">
            <h2 className="text-2xl font-semibold mb-4">Feedback System</h2>
            <p>View and manage agent feedback, metrics, and performance evaluations.</p>
          </Link>

          <Link href="/improvement" className="card hover:bg-opacity-80 transition-colors">
            <h2 className="text-2xl font-semibold mb-4">Improvement System</h2>
            <p>Track agent improvements, behavior modifications, and self-evaluation results.</p>
          </Link>

          <Link href="/metalearning" className="card hover:bg-opacity-80 transition-colors">
            <h2 className="text-2xl font-semibold mb-4">Meta-Learning Framework</h2>
            <p>Explore knowledge transfer, adaptation patterns, and learning analytics.</p>
          </Link>

          <Link href="/plugins" className="card hover:bg-opacity-80 transition-colors">
            <h2 className="text-2xl font-semibold mb-4">Plugin Manager</h2>
            <p>Manage, configure, and monitor plugins to extend agent capabilities.</p>
          </Link>
        </div>
      </main>
    </div>
  );
}
