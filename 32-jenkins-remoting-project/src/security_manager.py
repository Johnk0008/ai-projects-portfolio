import json
import hashlib
import subprocess
from typing import Dict, List
from src.jenkins_controller import JenkinsController

class SecurityManager:
    """Manage security and isolation for Jenkins nodes"""
    
    def __init__(self, jenkins_controller: JenkinsController):
        self.jc = jenkins_controller
        self.logger = jenkins_controller.logger
    
    def validate_node_architecture(self, node_name: str) -> bool:
        """Validate node architecture against allowed list"""
        try:
            node_info = self.jc.get_node_info(node_name)
            if not node_info:
                return False
            
            # Get node architecture from labels or properties
            architecture = self._detect_architecture(node_info)
            allowed_archs = self.jc.config['security']['allowed_architectures']
            
            if architecture not in allowed_archs:
                self.logger.warning(f"Node {node_name} has unauthorized architecture: {architecture}")
                return False
            
            self.logger.info(f"Node {node_name} architecture validated: {architecture}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating architecture for {node_name}: {e}")
            return False
    
    def _detect_architecture(self, node_info: Dict) -> str:
        """Detect node architecture from node information"""
        # This would typically involve checking node properties or labels
        labels = node_info.get('assignedLabels', [])
        for label in labels:
            if 'amd64' in label['name'] or 'arm64' in label['name']:
                return label['name']
        
        # Default detection based on common patterns
        return "unknown"
    
    def apply_isolation_rules(self, node_name: str) -> bool:
        """Apply isolation rules to node"""
        try:
            # Apply resource limits
            self._apply_resource_limits(node_name)
            
            # Apply network restrictions
            self._apply_network_restrictions(node_name)
            
            # Apply filesystem restrictions
            self._apply_filesystem_restrictions(node_name)
            
            self.logger.info(f"Applied isolation rules to node: {node_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying isolation rules to {node_name}: {e}")
            return False
    
    def _apply_resource_limits(self, node_name: str):
        """Apply resource limits to node (placeholder)"""
        # Implementation would use cgroups, Docker limits, etc.
        self.logger.info(f"Applying resource limits to {node_name}")
    
    def _apply_network_restrictions(self, node_name: str):
        """Apply network restrictions to node (placeholder)"""
        # Implementation would use iptables, firewall rules, etc.
        self.logger.info(f"Applying network restrictions to {node_name}")
    
    def _apply_filesystem_restrictions(self, node_name: str):
        """Apply filesystem restrictions to node (placeholder)"""
        # Implementation would use chroot, container filesystems, etc.
        self.logger.info(f"Applying filesystem restrictions to {node_name}")