
# SuperDeepAgent UI Integration Guide

This guide provides instructions for integrating the SuperDeepAgent Phase 3 UI components with the existing SuperAGI UI.

## Prerequisites

- Access to the SuperAGI repository
- Node.js and npm installed
- Basic knowledge of Next.js and React

## Integration Steps

### 1. Clone the SuperAGI Repository

```bash
git clone https://github.com/TransformerOptimus/SuperAGI.git
cd SuperAGI
```

### 2. Copy SuperDeepAgent UI Components

Copy the SuperDeepAgent UI components to the appropriate directories in the SuperAGI UI codebase:

```bash
# Create directories if they don't exist
mkdir -p gui/components/feedback
mkdir -p gui/components/improvement
mkdir -p gui/components/metalearning
mkdir -p gui/hooks
mkdir -p gui/utils

# Copy components
cp -r superdeepagent_ui/components/feedback/* gui/components/feedback/
cp -r superdeepagent_ui/components/improvement/* gui/components/improvement/
cp -r superdeepagent_ui/components/metalearning/* gui/components/metalearning/

# Copy hooks and utilities
cp -r superdeepagent_ui/hooks/* gui/hooks/
cp -r superdeepagent_ui/utils/* gui/utils/
```

### 3. Add Dependencies

Update the package.json file to include the required dependencies:

```bash
npm install @tremor/react reactflow socket.io-client
```

### 4. Update Tailwind Configuration

Update the tailwind.config.js file to include the SuperDeepAgent UI color scheme:

```javascript
// Add to the existing tailwind.config.js
module.exports = {
  // ... existing config
  theme: {
    extend: {
      // ... existing theme
      colors: {
        // ... existing colors
        primary: '#00e0ff',
        secondary: '#6c5dd3',
        background: '#121212',
        surface: '#1e1e1e',
      },
    },
  },
}
```

### 5. Add Routes to the Navigation

Update the sidebar navigation to include links to the new pages:

```javascript
// In gui/components/sidebar.js or equivalent
<div className={styles.menu_item} onClick={() => handleSelectionEvent('feedback')}>
  <Image src="/images/feedback_icon.svg" height={20} width={20} alt="Feedback"/>
  <span>Feedback</span>
</div>

<div className={styles.menu_item} onClick={() => handleSelectionEvent('improvement')}>
  <Image src="/images/improvement_icon.svg" height={20} width={20} alt="Improvement"/>
  <span>Improvement</span>
</div>

<div className={styles.menu_item} onClick={() => handleSelectionEvent('metalearning')}>
  <Image src="/images/metalearning_icon.svg" height={20} width={20} alt="Meta-Learning"/>
  <span>Meta-Learning</span>
</div>
```

### 6. Add Tab Components to Agent Workspace

Update the agent workspace to include tabs for feedback and improvement:

```javascript
// In gui/components/agent_workspace.js or equivalent
<div className={styles.tabs_container}>
  {/* Existing tabs */}
  <div 
    onClick={() => setActiveTab('feedback')} 
    className={`${styles.tab} ${activeTab === 'feedback' ? styles.active : ''}`}
  >
    Feedback
  </div>
  <div 
    onClick={() => setActiveTab('improvements')} 
    className={`${styles.tab} ${activeTab === 'improvements' ? styles.active : ''}`}
  >
    Improvements
  </div>
</div>

{/* Tab content */}
{activeTab === 'feedback' && (
  <FeedbackPanel 
    agentId={agentId} 
    runId={currentRun?.id} 
  />
)}
{activeTab === 'improvements' && (
  <ImprovementPanel 
    agentId={agentId} 
    agentConfig={agentConfig}
    onApplyImprovement={handleApplyImprovement}
  />
)}
```

### 7. Implement API Endpoints

Create API endpoints for the Phase 3 features:

```javascript
// In gui/pages/api/feedback/agent/[agentId].js
export default async function handler(req, res) {
  const { agentId } = req.query;
  const { timeRange } = req.query;

  // Fetch feedback data from backend
  // This is a placeholder - replace with actual implementation
  const feedbackData = {
    // ... mock data
  };

  res.status(200).json(feedbackData);
}

// Similar endpoints for other API routes
```

### 8. Set Up WebSocket Connection

Set up a WebSocket connection for real-time updates:

```javascript
// In gui/pages/_app.js
import { initializeSocket } from '../utils/websocket';

function MyApp({ Component, pageProps }) {
  // Initialize WebSocket connection
  useEffect(() => {
    const socket = initializeSocket();

    return () => {
      socket.disconnect();
    };
  }, []);

  return <Component {...pageProps} />;
}
```

### 9. Add Icons and Assets

Add the necessary icons and assets for the new components:

```bash
# Create icons directory if it doesn't exist
mkdir -p gui/public/images

# Copy icons
cp superdeepagent_ui/public/images/feedback_icon.svg gui/public/images/
cp superdeepagent_ui/public/images/improvement_icon.svg gui/public/images/
cp superdeepagent_ui/public/images/metalearning_icon.svg gui/public/images/
```

### 10. Test the Integration

Start the development server and test the integration:

```bash
npm run dev
```

## Troubleshooting

- If components are not rendering correctly, check the console for errors
- If API calls are failing, check the network tab in the browser developer tools
- If WebSocket connections are not working, check the server logs for errors

## Next Steps

After integrating the UI components, you'll need to:

1. Implement the backend API endpoints for the Phase 3 features
2. Set up WebSocket events for real-time updates
3. Connect the UI components to the actual data sources
4. Test the complete integration with real data

## Resources

- [SuperAGI Documentation](https://github.com/TransformerOptimus/SuperAGI)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tremor Documentation](https://www.tremor.so/docs)
- [React Flow Documentation](https://reactflow.dev/docs)
