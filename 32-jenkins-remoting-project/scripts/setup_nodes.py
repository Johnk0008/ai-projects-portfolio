#!/usr/bin/env python3
"""
Script to setup Jenkins remoting nodes
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.jenkins_controller import JenkinsController
from src.node_manager import NodeManager
from src.security_manager import SecurityManager

def setup_sample_nodes():
    """Setup sample nodes for demonstration"""
    
    # Initialize controllers
    jc = JenkinsController()
    node_manager = NodeManager(jc)
    security_manager = SecurityManager(jc)
    
    # Sample node configurations for different architectures
    sample_nodes = [
        {
            'name': 'linux-amd64-node',
            'executors': 4,
            'description': 'Linux AMD64 build node',
            'labels': ['linux', 'amd64', 'docker', 'python-3.9'],
            'remote_fs': '/home/jenkins'
        },
        {
            'name': 'linux-arm64-node', 
            'executors': 2,
            'description': 'Linux ARM64 build node',
            'labels': ['linux', 'arm64', 'docker', 'python-3.9'],
            'remote_fs': '/home/jenkins'
        },
        {
            'name': 'windows-amd64-node',
            'executors': 2,
            'description': 'Windows AMD64 build node',
            'labels': ['windows', 'amd64', 'powershell'],
            'remote_fs': 'C:\\jenkins'
        }
    ]
    
    # Create nodes
    for node_config in sample_nodes:
        success = node_manager.create_node(
            node_config['name'], 
            node_config
        )
        
        if success:
            # Apply security and isolation
            security_manager.validate_node_architecture(node_config['name'])
            security_manager.apply_isolation_rules(node_config['name'])
            
            print(f"✓ Successfully setup node: {node_config['name']}")
        else:
            print(f"✗ Failed to setup node: {node_config['name']}")

if __name__ == "__main__":
    setup_sample_nodes()