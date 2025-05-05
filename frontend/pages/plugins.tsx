import React from 'react';
import Head from 'next/head';
import PluginManager from '../components/plugin/PluginManager';

const PluginsPage: React.FC = () => {
  return (
    <div>
      <Head>
        <title>Plugin Manager - SuperDeepAgent</title>
        <meta name="description" content="Manage plugins for SuperDeepAgent" />
      </Head>

      <main>
        <PluginManager />
      </main>
    </div>
  );
};

export default PluginsPage;
