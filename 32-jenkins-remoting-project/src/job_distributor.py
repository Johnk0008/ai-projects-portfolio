import random
from typing import Dict, List
from src.jenkins_controller import JenkinsController

class JobDistributor:
    """Distribute build loads across nodes intelligently"""
    
    def __init__(self, jenkins_controller: JenkinsController):
        self.jc = jenkins_controller
        self.logger = jenkins_controller.logger
    
    def distribute_job(self, job_name: str, parameters: Dict = None) -> str:
        """Distribute job to appropriate node"""
        try:
            # Get available nodes
            nodes = self.jc.get_all_nodes()
            available_nodes = [node for node in nodes if self._is_node_available(node)]
            
            if not available_nodes:
                self.logger.error("No available nodes for job distribution")
                return ""
            
            # Select best node based on strategy
            selected_node = self._select_best_node(available_nodes, job_name)
            
            # Build job parameters
            job_params = parameters or {}
            job_params['target_node'] = selected_node['name']
            
            # Trigger job
            queue_item = self.jc.jenkins.build_job(job_name, parameters=job_params)
            self.logger.info(f"Distributed job {job_name} to node {selected_node['name']}")
            
            return queue_item
            
        except Exception as e:
            self.logger.error(f"Error distributing job {job_name}: {e}")
            return ""
    
    def _is_node_available(self, node: Dict) -> bool:
        """Check if node is available for builds"""
        return (node.get('offline') is False and 
                node.get('temporarilyOffline') is False)
    
    def _select_best_node(self, nodes: List[Dict], job_name: str) -> Dict:
        """Select the best node for the job based on strategy"""
        strategies = {
            'round_robin': self._round_robin_strategy,
            'load_based': self._load_based_strategy,
            'architecture_based': self._architecture_based_strategy
        }
        
        strategy = self.jc.config.get('distribution_strategy', 'round_robin')
        strategy_func = strategies.get(strategy, self._round_robin_strategy)
        
        return strategy_func(nodes, job_name)
    
    def _round_robin_strategy(self, nodes: List[Dict], job_name: str) -> Dict:
        """Round-robin node selection"""
        return random.choice(nodes)
    
    def _load_based_strategy(self, nodes: List[Dict], job_name: str) -> Dict:
        """Select node based on current load"""
        # Simple implementation - in production, you'd check actual load metrics
        return min(nodes, key=lambda x: x.get('numExecutors', 1))
    
    def _architecture_based_strategy(self, nodes: List[Dict], job_name: str) -> Dict:
        """Select node based on architecture requirements"""
        # Check if job has specific architecture requirements
        if 'arm64' in job_name.lower():
            arm_nodes = [node for node in nodes if 'arm' in str(node.get('labels', [])).lower()]
            return arm_nodes[0] if arm_nodes else nodes[0]
        
        return nodes[0]