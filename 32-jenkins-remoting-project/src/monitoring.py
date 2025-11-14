import time
import threading
from typing import Dict, List
from src.jenkins_controller import JenkinsController

class MonitoringSystem:
    """Monitor Jenkins nodes and remoting performance"""
    
    def __init__(self, jenkins_controller: JenkinsController):
        self.jc = jenkins_controller
        self.logger = jenkins_controller.logger
        self.monitoring_data = {}
        self.is_monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self) -> bool:
        """Start the monitoring system"""
        try:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            self.logger.info("Started Jenkins remoting monitoring")
            return True
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop the monitoring system"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("Stopped Jenkins remoting monitoring")
        return True
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                self._collect_node_metrics()
                self._check_node_health()
                self._log_performance_metrics()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)
    
    def _collect_node_metrics(self):
        """Collect metrics from all nodes"""
        nodes = self.jc.get_all_nodes()
        for node in nodes:
            node_name = node.get('name', 'unknown')
            self.monitoring_data[node_name] = {
                'online': not node.get('offline', True),
                'executors': node.get('numExecutors', 0),
                'load': self._calculate_node_load(node),
                'last_updated': time.time()
            }
    
    def _calculate_node_load(self, node: Dict) -> float:
        """Calculate current load on node (placeholder implementation)"""
        # In production, this would check actual running builds
        return 0.0
    
    def _check_node_health(self):
        """Check health of all nodes"""
        for node_name, metrics in self.monitoring_data.items():
            if not metrics['online']:
                self.logger.warning(f"Node {node_name} is offline")
            
            # Check if node hasn't been updated recently
            last_update = metrics.get('last_updated', 0)
            if time.time() - last_update > 300:  # 5 minutes
                self.logger.error(f"Node {node_name} appears to be unresponsive")
    
    def _log_performance_metrics(self):
        """Log performance metrics"""
        online_nodes = sum(1 for metrics in self.monitoring_data.values() 
                          if metrics['online'])
        total_nodes = len(self.monitoring_data)
        
        self.logger.info(
            f"Monitoring: {online_nodes}/{total_nodes} nodes online, "
            f"Total executors: {sum(m.get('executors', 0) for m in self.monitoring_data.values())}"
        )