# Usage Examples

## Overview

This document provides practical examples of how to use the SuperDeepAgent Phase 3 components in common scenarios. These examples demonstrate the integration and application of the Improvement System, Metalearning System, and Feedback System to solve real-world problems.

## Basic Setup

Before diving into specific scenarios, here's a basic setup that initializes all Phase 3 components:

```python
from superdeepagent.phase3 import Phase3Integration
from superdeepagent.config import load_config

# Load configuration
config = load_config("phase3_config.yaml")

# Initialize Phase 3 integration
phase3 = Phase3Integration(config=config)

# Initialize all systems
initialization_status = phase3.initialize_systems()

# Check initialization status
if all(initialization_status.values()):
    print("All Phase 3 systems initialized successfully")
else:
    failed_systems = [system for system, success in initialization_status.items() if not success]
    print(f"Failed to initialize: {failed_systems}")
```

## Example 1: Implementing a Self-Improving Chatbot

This example demonstrates how to create a chatbot that improves its responses based on user feedback.

```python
from superdeepagent.phase3 import Phase3Integration
from superdeepagent.utils import ChatSession

# Initialize Phase 3 integration
phase3 = Phase3Integration(config={
    "improvement_system": {
        "evaluation_criteria": {
            "response_quality": 2.0,
            "helpfulness": 1.5,
            "accuracy": 2.0
        }
    },
    "feedback_system": {
        "feedback_categories": ["helpful", "accurate", "clear", "relevant"]
    }
})

# Initialize systems
phase3.initialize_systems()

# Create a chat session
session = ChatSession(user_id="user123")

def process_user_message(user_message):
    # Process the user message using Phase 3 capabilities
    response = phase3.process_user_interaction(
        interaction_data={
            "user_id": session.user_id,
            "query": user_message,
            "session_id": session.session_id,
            "history": session.history
        }
    )
    
    # Update session history
    session.add_interaction(user_message, response["response"])
    
    return response["response"]

def collect_user_feedback(rating, comments=None, categories=None):
    # Collect feedback on the last interaction
    feedback_data = {
        "user_id": session.user_id,
        "session_id": session.session_id,
        "interaction_id": session.last_interaction_id,
        "rating": rating,
        "comments": comments,
        "categories": categories
    }
    
    # Submit feedback to the feedback system
    feedback_result = phase3.collect_feedback(
        feedback_data=feedback_data,
        feedback_type="user"
    )
    
    # If feedback indicates issues, trigger an improvement cycle
    if rating < 3:  # Rating below 3 out of 5
        improvement_results = phase3.trigger_improvement_cycle(
            trigger_source="feedback",
            performance_data={"user_rating": rating}
        )
        
        print(f"Improvement cycle triggered. Results: {improvement_results['summary']}")
    
    return feedback_result

# Example usage
response = process_user_message("What is machine learning?")
print(f"Bot: {response}")

# User provides feedback
feedback_result = collect_user_feedback(
    rating=2,  # 2 out of 5
    comments="The explanation was too technical",
    categories=["clear"]
)

# Next interaction should show improvement
improved_response = process_user_message("Can you explain machine learning again, but simpler?")
print(f"Bot: {improved_response}")
```

## Example 2: Knowledge Transfer Between Domains

This example shows how to use the Metalearning System to transfer knowledge from one domain to another.

```python
from superdeepagent.phase3 import Phase3Integration
from superdeepagent.knowledge import DomainKnowledgeBase

# Initialize Phase 3 integration
phase3 = Phase3Integration(config={
    "metalearning_system": {
        "abstraction_strategies": {
            "conceptual": "default",
            "structural": "default"
        },
        "transfer_strategies": {
            "analogical": "default"
        }
    }
})

# Initialize systems
phase3.initialize_systems(systems_to_initialize=["metalearning_system"])

# Initialize domain knowledge bases
chess_knowledge = DomainKnowledgeBase("chess")
business_knowledge = DomainKnowledgeBase("business_strategy")

# Load existing knowledge into the chess domain
chess_knowledge.load_from_file("chess_concepts.json")

# Check if we have sufficient knowledge in the business domain
if business_knowledge.get_knowledge_size() < 100:  # Arbitrary threshold
    print("Business strategy knowledge base is limited. Attempting knowledge transfer...")
    
    # Apply metalearning to transfer knowledge from chess to business
    transfer_results = phase3.apply_metalearning(
        source_domain="chess",
        target_domain="business_strategy",
        context={
            "transfer_purpose": "strategic_thinking",
            "abstraction_level": "high",
            "transfer_strategy": "analogical"
        }
    )
    
    if transfer_results["success"]:
        # Add the transferred knowledge to the business knowledge base
        business_knowledge.add_knowledge(
            transfer_results["transferred_knowledge"],
            source="knowledge_transfer_from_chess"
        )
        
        print(f"Successfully transferred {len(transfer_results['transferred_knowledge'])} concepts")
        
        # Example of using the transferred knowledge
        strategic_concepts = business_knowledge.query_knowledge(
            query="strategic positioning",
            limit=5
        )
        
        print("Top strategic concepts transferred from chess:")
        for concept in strategic_concepts:
            print(f"- {concept['name']}: {concept['description']}")
    else:
        print(f"Knowledge transfer failed: {transfer_results['message']}")
```

## Example 3: Setting Up a Comprehensive Feedback System

This example demonstrates how to set up a comprehensive feedback system that collects both explicit user feedback and implicit system metrics.

```python
from superdeepagent.phase3 import Phase3Integration
from superdeepagent.feedback import FeedbackDashboard
from superdeepagent.metrics import MetricsCollector
import time

# Initialize Phase 3 integration
phase3 = Phase3Integration(config={
    "feedback_system": {
        "feedback_categories": [
            "accuracy", "helpfulness", "clarity", "relevance", "speed"
        ],
        "metrics_config": {
            "response_time": {"type": "histogram", "frequency": "per_request"},
            "memory_usage": {"type": "gauge", "frequency": "every_minute"},
            "error_rate": {"type": "counter", "frequency": "continuous"}
        },
        "threshold_values": {
            "user_satisfaction": 0.8,  # 80% satisfaction target
            "response_time": 2.0,  # 2 seconds max
            "error_rate": 0.05  # 5% error rate max
        }
    }
})

# Initialize just the feedback system
phase3.initialize_systems(systems_to_initialize=["feedback_system"])

# Create a metrics collector that will feed into the feedback system
metrics_collector = MetricsCollector(
    agent_id="agent001",
    metrics_config=phase3.get_system_status()["feedback_system"]["metrics_config"]
)

# Create a feedback dashboard for visualization
dashboard = FeedbackDashboard(
    feedback_system=phase3.get_system_status()["feedback_system"]["instance"]
)

# Function to process a user query and collect metrics
def process_query(user_id, query):
    # Start timing the response
    start_time = time.time()
    
    try:
        # Process the query (simplified for example)
        response = f"Response to: {query}"
        
        # Record successful query
        metrics_collector.increment_counter("successful_queries")
    except Exception as e:
        # Record error
        metrics_collector.increment_counter("error_rate")
        response = f"Error processing query: {str(e)}"
    
    # Calculate response time
    response_time = time.time() - start_time
    
    # Record response time
    metrics_collector.record_histogram("response_time", response_time)
    
    # Record memory usage
    current_memory = get_current_memory_usage()  # Placeholder function
    metrics_collector.record_gauge("memory_usage", current_memory)
    
    # Submit metrics to the feedback system
    phase3.collect_feedback(
        feedback_data=metrics_collector.get_current_metrics(),
        feedback_type="system"
    )
    
    return response

# Function to collect explicit user feedback
def collect_explicit_feedback(user_id, interaction_id, rating, comments=None, categories=None):
    feedback_data = {
        "user_id": user_id,
        "interaction_id": interaction_id,
        "rating": rating,
        "comments": comments,
        "categories": categories
    }
    
    # Submit user feedback
    feedback_result = phase3.collect_feedback(
        feedback_data=feedback_data,
        feedback_type="user"
    )
    
    # Update the dashboard
    dashboard.refresh_data()
    
    return feedback_result

# Set up performance evaluation and triggers
def setup_performance_triggers():
    # Configure the system to automatically trigger improvements
    phase3.configure_system(
        system="feedback_system",
        configuration={
            "auto_triggers": {
                "low_satisfaction": {
                    "dimension": "user_satisfaction",
                    "threshold": 0.7,
                    "comparison": "<",
                    "action": "improvement_cycle",
                    "cooldown": 86400  # 24 hours in seconds
                },
                "high_response_time": {
                    "dimension": "response_time",
                    "threshold": 3.0,  # 3 seconds
                    "comparison": ">",
                    "action": "alert_engineering",
                    "cooldown": 3600  # 1 hour in seconds
                }
            }
        }
    )
    
    print("Performance triggers configured")

# Example usage
setup_performance_triggers()

# Process some queries
for i in range(10):
    query = f"Test query {i}"
    response = process_query("test_user", query)
    print(f"Query: {query} -> Response: {response}")

# Collect explicit feedback
feedback_result = collect_explicit_feedback(
    user_id="test_user",
    interaction_id="interaction_001",
    rating=4,  # 4 out of 5
    comments="Good response but a bit slow",
    categories=["clarity", "speed"]
)

# Generate a performance report
performance_report = phase3.get_system_status()["feedback_system"]["instance"].generate_performance_report(
    time_period="last_hour",
    include_recommendations=True
)

print("\nPerformance Report:")
print(performance_report)
```

## Example 4: Implementing a Self-Evaluation and Improvement Cycle

This example shows how to set up a regular self-evaluation and improvement cycle for the agent.

```python
from superdeepagent.phase3 import Phase3Integration
from superdeepagent.improvement import ImprovementLog
import schedule
import time

# Initialize Phase 3 integration
phase3 = Phase3Integration(config={
    "improvement_system": {
        "evaluation_criteria": {
            "response_quality": 2.0,
            "efficiency": 1.0,
            "adaptability": 1.5,
            "knowledge_application": 1.8
        },
        "behavior_registry": {
            "response_generation": {
                "current_config": {
                    "temperature": 0.7,
                    "max_tokens": 150,
                    "top_p": 0.9
                },
                "constraints": {
                    "temperature": {"min": 0.1, "max": 1.0},
                    "max_tokens": {"min": 50, "max": 500},
                    "top_p": {"min": 0.1, "max": 1.0}
                }
            },
            "knowledge_retrieval": {
                "current_config": {
                    "relevance_threshold": 0.75,
                    "max_results": 5,
                    "include_metadata": True
                },
                "constraints": {
                    "relevance_threshold": {"min": 0.5, "max": 0.95},
                    "max_results": {"min": 3, "max": 20}
                }
            }
        }
    }
})

# Initialize the improvement system
phase3.initialize_systems(systems_to_initialize=["improvement_system"])

# Create an improvement log
improvement_log = ImprovementLog(log_file="improvement_history.json")

# Function to run a complete improvement cycle
def run_improvement_cycle():
    print("Starting scheduled improvement cycle...")
    
    # Collect performance data (in a real system, this would come from actual usage)
    performance_data = {
        "response_quality": 0.82,
        "efficiency": 0.75,
        "adaptability": 0.68,
        "knowledge_application": 0.79
    }
    
    # Trigger the improvement cycle
    improvement_results = phase3.trigger_improvement_cycle(
        trigger_source="schedule",
        performance_data=performance_data
    )
    
    # Log the improvement results
    improvement_log.add_entry(
        cycle_id=improvement_results["cycle_id"],
        timestamp=improvement_results["timestamp"],
        performance_before=performance_data,
        identified_areas=improvement_results["improvement_areas"],
        modifications=improvement_results["modifications"],
        insights=improvement_results["insights"]
    )
    
    # Apply the modifications
    if improvement_results["modifications"]:
        print(f"Applying {len(improvement_results['modifications'])} modifications:")
        for mod in improvement_results["modifications"]:
            print(f"- {mod['behavior_id']}: {mod['parameter']} = {mod['new_value']} (was {mod['old_value']})")
            
            # In a real system, you would apply these modifications to the actual agent
            # apply_modification_to_agent(mod)
    else:
        print("No modifications suggested in this cycle")
    
    # Print key insights
    print("\nKey insights from this improvement cycle:")
    for insight in improvement_results["insights"][:3]:  # Top 3 insights
        print(f"- {insight}")
    
    print(f"Improvement cycle completed. Log updated with cycle ID: {improvement_results['cycle_id']}")

# Schedule regular improvement cycles
def schedule_improvement_cycles(frequency="daily"):
    if frequency == "hourly":
        schedule.every().hour.do(run_improvement_cycle)
    elif frequency == "daily":
        schedule.every().day.at("03:00").do(run_improvement_cycle)  # Run at 3 AM
    elif frequency == "weekly":
        schedule.every().monday.at("02:00").do(run_improvement_cycle)  # Run at 2 AM on Mondays
    
    print(f"Improvement cycles scheduled to run {frequency}")

# Example usage
schedule_improvement_cycles(frequency="daily")

# Run an initial improvement cycle immediately
run_improvement_cycle()

# In a real application, you would keep this running
print("Scheduler running. Press Ctrl+C to exit.")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    print("Scheduler stopped.")
```

## Example 5: Integrating All Phase 3 Systems

This comprehensive example demonstrates how to integrate all Phase 3 systems to create a fully self-improving agent.

```python
from superdeepagent.phase3 import Phase3Integration
from superdeepagent.utils import AgentMonitor
import json
import threading
import time

# Load comprehensive configuration
with open("phase3_full_config.json", "r") as f:
    config = json.load(f)

# Initialize Phase 3 integration with full configuration
phase3 = Phase3Integration(config=config)

# Initialize all systems
initialization_status = phase3.initialize_systems()

# Create an agent monitor
monitor = AgentMonitor(phase3)

# Start monitoring in a separate thread
def monitoring_thread():
    while True:
        monitor.collect_metrics()
        monitor.check_health()
        time.sleep(60)  # Check every minute

monitor_thread = threading.Thread(target=monitoring_thread, daemon=True)
monitor_thread.start()

# Function to process user queries with full Phase 3 capabilities
def process_query(user_id, query, context=None):
    # Start timing
    start_time = time.time()
    
    # Process the interaction with all Phase 3 capabilities
    response = phase3.process_user_interaction(
        interaction_data={
            "user_id": user_id,
            "query": query,
            "timestamp": time.time(),
            "context": context or {}
        }
    )
    
    # Record processing time
    processing_time = time.time() - start_time
    
    # Automatically collect system metrics
    phase3.collect_feedback(
        feedback_data={
            "response_time": processing_time,
            "query_complexity": estimate_complexity(query),
            "response_length": len(response["response"])
        },
        feedback_type="system"
    )
    
    return response

# Function to handle user feedback
def handle_feedback(user_id, interaction_id, feedback):
    # Submit the feedback
    feedback_result = phase3.collect_feedback(
        feedback_data={
            "user_id": user_id,
            "interaction_id": interaction_id,
            **feedback
        },
        feedback_type="user"
    )
    
    # Check if any triggers were activated
    if feedback_result.get("triggers_activated"):
        print(f"Feedback activated triggers: {feedback_result['triggers_activated']}")
    
    return feedback_result

# Function to apply knowledge transfer between domains
def transfer_domain_knowledge(source_domain, target_domain, transfer_context=None):
    # Apply metalearning to transfer knowledge
    transfer_results = phase3.apply_metalearning(
        source_domain=source_domain,
        target_domain=target_domain,
        context=transfer_context or {}
    )
    
    if transfer_results["success"]:
        print(f"Successfully transferred knowledge from {source_domain} to {target_domain}")
        print(f"Transferred {len(transfer_results['transferred_knowledge'])} concepts/principles")
        
        # In a real system, you would integrate this knowledge into the agent
        # integrate_knowledge(transfer_results['transferred_knowledge'])
    
    return transfer_results

# Function to run a manual improvement cycle
def run_manual_improvement(focus_areas=None):
    # Get current performance metrics
    performance_data = monitor.get_performance_metrics()
    
    # Trigger an improvement cycle
    improvement_results = phase3.trigger_improvement_cycle(
        trigger_source="manual",
        performance_data=performance_data
    )
    
    print(f"Manual improvement cycle completed: {improvement_results['summary']}")
    
    return improvement_results

# Function to get system status dashboard
def get_system_dashboard():
    # Get status of all systems
    system_status = phase3.get_system_status()
    
    # Get recent improvements
    recent_improvements = system_status["improvement_system"]["recent_improvements"]
    
    # Get feedback statistics
    feedback_stats = system_status["feedback_system"]["statistics"]
    
    # Get metalearning activities
    metalearning_activities = system_status["metalearning_system"]["recent_activities"]
    
    # Compile dashboard data
    dashboard = {
        "system_health": monitor.get_health_status(),
        "performance_metrics": monitor.get_performance_metrics(),
        "recent_improvements": recent_improvements,
        "feedback_statistics": feedback_stats,
        "metalearning_activities": metalearning_activities,
        "last_updated": time.time()
    }
    
    return dashboard

# Helper function to estimate query complexity
def estimate_complexity(query):
    # Simple complexity estimation based on length and structure
    # In a real system, this would be more sophisticated
    complexity = len(query) / 100  # Base complexity on length
    
    # Add complexity for certain keywords or structures
    complexity_keywords = ["explain", "compare", "analyze", "synthesize", "evaluate"]
    for keyword in complexity_keywords:
        if keyword in query.lower():
            complexity += 0.2
    
    return min(1.0, complexity)  # Cap at 1.0

# Example usage
print("SuperDeepAgent Phase 3 fully initialized and ready")

# Process a user query
response = process_query(
    user_id="user456",
    query="Compare and contrast machine learning approaches for natural language processing",
    context={"expertise_level": "intermediate", "domain": "ai_research"}
)

print(f"Response: {response['response']}")
print(f"Response generated with insights from: {response.get('metalearning_applications', [])}")

# Handle user feedback
feedback_result = handle_feedback(
    user_id="user456",
    interaction_id=response["interaction_id"],
    feedback={
        "rating": 4,
        "categories": ["accuracy", "completeness"],
        "comments": "Good comparison but could include more recent approaches"
    }
)

# Transfer knowledge between domains
transfer_results = transfer_domain_knowledge(
    source_domain="machine_learning",
    target_domain="healthcare",
    transfer_context={"transfer_purpose": "diagnostic_applications"}
)

# Run a manual improvement cycle
improvement_results = run_manual_improvement(
    focus_areas=["response_quality", "knowledge_application"]
)

# Get system dashboard
dashboard = get_system_dashboard()
print("\nSystem Dashboard:")
print(json.dumps(dashboard, indent=2))

print("\nSuperDeepAgent Phase 3 demonstration completed")
```

## Best Practices

When using the SuperDeepAgent Phase 3 components, consider the following best practices:

1. **Start with Feedback**: Begin by implementing the Feedback System to collect data before attempting to use the Improvement System
2. **Incremental Integration**: Integrate Phase 3 components incrementally rather than all at once
3. **Regular Evaluation Cycles**: Schedule regular improvement cycles rather than relying solely on triggered improvements
4. **Domain Mapping**: When using the Metalearning System, create explicit mappings between source and target domains
5. **Constraint Definition**: Define clear constraints for behavior modifications to prevent extreme changes
6. **Performance Monitoring**: Continuously monitor the performance impact of Phase 3 systems
7. **User Feedback Integration**: Combine explicit user feedback with implicit system metrics for comprehensive evaluation
8. **Knowledge Persistence**: Ensure that learned knowledge and improvements persist across agent restarts
9. **Logging and Traceability**: Maintain detailed logs of all improvements and knowledge transfers
10. **Configuration Management**: Use a centralized configuration management approach for consistency

## Common Pitfalls and Solutions

1. **Oscillating Improvements**
   - Pitfall: The agent repeatedly makes and reverts similar improvements
   - Solution: Implement cooldown periods between modifications to the same behavior

2. **Feedback Bias**
   - Pitfall: Overreacting to a small number of negative feedback instances
   - Solution: Ensure sufficient data before triggering improvements and consider statistical significance

3. **Overgeneralization in Knowledge Transfer**
   - Pitfall: Transferring knowledge that is too abstract to be useful
   - Solution: Adjust abstraction levels and validate transferred knowledge before application

4. **Resource Consumption**
   - Pitfall: Phase 3 systems consuming excessive computational resources
   - Solution: Schedule intensive operations during low-usage periods and optimize algorithms

5. **Integration Complexity**
   - Pitfall: Complex integration leading to maintenance challenges
   - Solution: Use the Phase3Integration class as a unified interface and maintain clear documentation

By following these examples and best practices, you can effectively leverage the SuperDeepAgent Phase 3 components to create sophisticated, self-improving AI systems.
