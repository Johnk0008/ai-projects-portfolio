import subprocess
import platform
import socket
from typing import Dict, List
import paramiko
from src.jenkins_controller import JenkinsController

class NodeManager:
    """Manage Jenkins nodes and agents"""
    
    def __init__(self, jenkins_controller: JenkinsController):
        self.jc = jenkins_controller
        self.logger = jenkins_controller.logger
    
    def create_node(self, node_name: str, node_config: Dict) -> bool:
        """Create a new Jenkins node"""
        try:
            self.jc.jenkins.create_node(
                name=node_name,
                numExecutors=node_config.get('executors', 2),
                nodeDescription=node_config.get('description', ''),
                remoteFS=node_config.get('remote_fs', '/home/jenkins'),
                labels=node_config.get('labels', []),
                exclusive=node_config.get('exclusive', False)
            )
            self.logger.info(f"Successfully created node: {node_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating node {node_name}: {e}")
            return False
    
    def delete_node(self, node_name: str) -> bool:
        """Delete a Jenkins node"""
        try:
            self.jc.jenkins.delete_node(node_name)
            self.logger.info(f"Successfully deleted node: {node_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting node {node_name}: {e}")
            return False
    
    def launch_agent(self, node_name: str, java_path: str = "java") -> bool:
        """Launch Jenkins agent on remote machine"""
        try:
            node_info = self.jc.get_node_info(node_name)
            if not node_info:
                return False
            
            # Get agent JAR and secret
            agent_jar = self._download_agent_jar()
            secret = node_info.get('secret', '')
            
            # Construct agent command
            jenkins_url = self.jc.config['jenkins']['base_url']
            command = self._build_agent_command(
                jenkins_url, node_name, secret, agent_jar, java_path
            )
            
            # Execute agent (this would typically be on remote machine)
            self.logger.info(f"Launching agent for node: {node_name}")
            # In production, this would use SSH or similar to execute on remote
            return self._execute_remote_agent(command, node_info)
            
        except Exception as e:
            self.logger.error(f"Error launching agent for {node_name}: {e}")
            return False
    
    def _build_agent_command(self, jenkins_url: str, node_name: str, 
                           secret: str, agent_jar: str, java_path: str) -> str:
        """Build the Java command to launch Jenkins agent"""
        return (
            f"{java_path} -jar {agent_jar} -jnlpUrl {jenkins_url}/computer/{node_name}/slave-agent.jnlp "
            f"-secret {secret} -workDir \"/home/jenkins/agent\""
        )
    
    def _download_agent_jar(self) -> str:
        """Download Jenkins agent JAR file"""
        # Implementation for downloading agent.jar
        return "agent.jar"
    
    def _execute_remote_agent(self, command: str, node_info: Dict) -> bool:
        """Execute agent command on remote machine (placeholder implementation)"""
        # In real implementation, this would use SSH or similar
        self.logger.info(f"Would execute: {command}")
        return True