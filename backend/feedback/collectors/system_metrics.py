"""System metrics collector implementation for the SuperDeepAgent feedback system."""

from superdeepagent.feedback.collectors.base import FeedbackCollector


class SystemMetricsCollector(FeedbackCollector):
    """
    Collects system performance metrics related to agent operation.
    
    This collector gathers data on response times, resource usage, error rates,
    and other system-level metrics that indicate agent performance.
    """
    
    def __init__(self, config=None):
        """
        Initialize the system metrics collector.
        
        Args:
            config (dict, optional): Configuration parameters for the collector.
        """
        self.config = config or {}
    
    def collect(self, interaction_data):
        """
        Collect system metrics from interaction data.
        
        Args:
            interaction_data (dict): Data containing system metrics.
                Expected keys:
                - 'response_times': Time taken for agent responses
                - 'resource_usage': CPU, memory, and other resource metrics
                - 'error_logs': Logs of errors encountered during operation
                - 'api_calls': Records of external API calls made
                
        Returns:
            dict: Collected system metrics including:
                - 'performance_metrics': Response time and throughput metrics
                - 'resource_metrics': Resource utilization metrics
                - 'reliability_metrics': Error rates and stability indicators
                - 'external_dependencies': Metrics related to external service usage
        """
        metrics = {
            'performance_metrics': self._process_performance_metrics(interaction_data),
            'resource_metrics': self._process_resource_metrics(interaction_data),
            'reliability_metrics': self._process_reliability_metrics(interaction_data),
            'external_dependencies': self._process_dependency_metrics(interaction_data)
        }
        
        return metrics
    
    def _process_performance_metrics(self, interaction_data):
        """Process response time and throughput metrics."""
        response_times = interaction_data.get('response_times', [])
        return {
            'avg_response_time': sum(response_times) / len(response_times) if response_times else 0.0,
            'max_response_time': max(response_times) if response_times else 0.0,
            'min_response_time': min(response_times) if response_times else 0.0,
            'p95_response_time': self._calculate_percentile(response_times, 95),
            'throughput': len(response_times) / interaction_data.get('time_period', 1)
        }
    
    def _calculate_percentile(self, values, percentile):
        """Calculate the specified percentile of a list of values."""
        if not values:
            return 0.0
            
        sorted_values = sorted(values)
        index = (len(sorted_values) - 1) * percentile / 100
        
        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            lower_value = sorted_values[lower_index]
            upper_value = sorted_values[upper_index]
            interpolation = index - lower_index
            return lower_value + (upper_value - lower_value) * interpolation
    
    def _process_resource_metrics(self, interaction_data):
        """Process resource utilization metrics."""
        resource_usage = interaction_data.get('resource_usage', {})
        return {
            'avg_cpu_usage': resource_usage.get('avg_cpu', 0.0),
            'max_memory_usage': resource_usage.get('max_memory', 0.0),
            'avg_memory_usage': resource_usage.get('avg_memory', 0.0),
            'disk_io': resource_usage.get('disk_io', 0.0),
            'network_io': resource_usage.get('network_io', 0.0)
        }
    
    def _process_reliability_metrics(self, interaction_data):
        """Process error rates and stability metrics."""
        error_logs = interaction_data.get('error_logs', [])
        total_interactions = interaction_data.get('total_interactions', 1)
        
        error_count = len(error_logs)
        error_rate = error_count / total_interactions if total_interactions > 0 else 0
        
        return {
            'error_count': error_count,
            'error_rate': error_rate,
            'error_categories': self._categorize_errors(error_logs)
        }
    
    def _categorize_errors(self, error_logs):
        """Categorize errors by type."""
        categories = {}
        for error in error_logs:
            error_type = error.get('type', 'unknown')
            categories[error_type] = categories.get(error_type, 0) + 1
            
        return categories
    
    def _process_dependency_metrics(self, interaction_data):
        """Process metrics related to external dependencies."""
        api_calls = interaction_data.get('api_calls', [])
        
        # Group by service
        services = {}
        for call in api_calls:
            service = call.get('service', 'unknown')
            if service not in services:
                services[service] = {
                    'count': 0,
                    'success_count': 0,
                    'total_latency': 0,
                    'error_count': 0
                }
                
            services[service]['count'] += 1
            if call.get('success', False):
                services[service]['success_count'] += 1
            else:
                services[service]['error_count'] += 1
                
            services[service]['total_latency'] += call.get('latency', 0)
            
        # Calculate averages and rates
        for service, metrics in services.items():
            count = metrics['count']
            if count > 0:
                metrics['avg_latency'] = metrics['total_latency'] / count
                metrics['success_rate'] = metrics['success_count'] / count
                
            del metrics['total_latency']
            
        return services
