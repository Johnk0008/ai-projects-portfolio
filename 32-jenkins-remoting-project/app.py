#!/usr/bin/env python3
"""
Main application for Jenkins Remoting Project
"""

import os
import argparse
from src.jenkins_controller import JenkinsController
from src.node_manager import NodeManager
from src.security_manager import SecurityManager
from src.job_distributor import JobDistributor
from src.monitoring import MonitoringSystem

class JenkinsRemotingApp:
    """Main application class"""
    
    def __init__(self):
        self.jc = JenkinsController()
        self.node_manager = NodeManager(self.jc)
        self.security_manager = SecurityManager(self.jc)
        self.job_distributor = JobDistributor(self.jc)
        self.monitoring = MonitoringSystem(self.jc)
    
    def setup_nodes(self, node_configs):
        """Setup multiple nodes"""
        for config in node_configs:
            self.node_manager.create_node(config['name'], config)
            self.security_manager.apply_isolation_rules(config['name'])
    
    def distribute_build(self, job_name, parameters=None):
        """Distribute build to appropriate node"""
        return self.job_distributor.distribute_job(job_name, parameters)
    
    def start_monitoring(self):
        """Start monitoring system"""
        return self.monitoring.start_monitoring()
    
    def get_status(self):
        """Get current status of all nodes"""
        return self.jc.get_all_nodes()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Jenkins Remoting Management')
    parser.add_argument('--setup', action='store_true', help='Setup sample nodes')
    parser.add_argument('--monitor', action='store_true', help='Start monitoring')
    parser.add_argument('--status', action='store_true', help='Show node status')
    parser.add_argument('--job', type=str, help='Job name to distribute')
    
    args = parser.parse_args()
    
    app = JenkinsRemotingApp()
    
    if args.setup:
        print("Setting up sample nodes...")
        # This would setup sample nodes
        from scripts.setup_nodes import setup_sample_nodes
        setup_sample_nodes()
    
    if args.monitor:
        print("Starting monitoring...")
        app.start_monitoring()
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            app.monitoring.stop_monitoring()
    
    if args.status:
        nodes = app.get_status()
        for node in nodes:
            status = "ONLINE" if not node.get('offline') else "OFFLINE"
            print(f"{node['name']}: {status}")
    
    if args.job:
        result = app.distribute_build(args.job)
        print(f"Distributed job {args.job}: {result}")

if __name__ == "__main__":
    main()