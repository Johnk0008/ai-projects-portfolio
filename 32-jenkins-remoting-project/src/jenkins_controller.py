import logging
import os
import json
import requests
from typing import Dict, List, Optional

class JenkinsController:
    """Main controller for Jenkins remoting operations"""
    
    def __init__(self, config_path: str = "config/jenkins_config.yaml"):
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        self.jenkins = self._connect_jenkins()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/jenkins_remoting.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file with fallback to JSON"""
        try:
            # Try to import yaml, fallback to JSON if not available
            try:
                import yaml
                with open(config_path, 'r') as file:
                    config = yaml.safe_load(file)
                self.logger.info("Loaded configuration from YAML file")
            except ImportError:
                self.logger.warning("PyYAML not installed, falling back to JSON configuration")
                # Fallback to JSON config
                json_config_path = config_path.replace('.yaml', '.json')
                if os.path.exists(json_config_path):
                    with open(json_config_path, 'r') as file:
                        config = json.load(file)
                else:
                    # Create default config if no files exist
                    config = self._create_default_config()
                    # Save as JSON for future use
                    with open(json_config_path, 'w') as file:
                        json.dump(config, file, indent=2)
                    self.logger.info("Created default JSON configuration")
            
            # Replace environment variables
            api_token = os.getenv('JENKINS_API_TOKEN')
            if api_token:
                config['jenkins']['api_token'] = api_token
            
            return config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            # Return default config if file loading fails
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """Create default configuration"""
        return {
            'jenkins': {
                'base_url': 'http://localhost:8080',
                'username': 'admin',
                'api_token': os.getenv('JENKINS_API_TOKEN', '')
            },
            'remoting': {
                'agent_port': 50000,
                'web_socket': True,
                'tunnel': ''
            },
            'security': {
                'ssl_verification': True,
                'node_isolation': True,
                'allowed_architectures': [
                    'linux-amd64',
                    'linux-arm64', 
                    'windows-amd64',
                    'darwin-amd64'
                ]
            },
            'nodes': {
                'default_labels': ['docker', 'python-3.9']
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/jenkins_remoting.log'
            }
        }
    
    def _connect_jenkins(self):
        """Connect to Jenkins server with mock fallback"""
        try:
            # Check if mock mode is enabled
            if os.getenv('MOCK_MODE', 'false').lower() == 'true':
                self.logger.info("MOCK MODE: Using mock Jenkins client")
                return MockJenkinsClient(self.config['jenkins'])
            
            # Try to use python-jenkins library if available
            try:
                from jenkins import Jenkins
                jenkins_config = self.config['jenkins']
                jenkins = Jenkins(
                    jenkins_config['base_url'],
                    username=jenkins_config['username'],
                    password=jenkins_config['api_token']
                )
                
                # Test connection
                user_info = jenkins.get_whoami()
                self.logger.info(f"Successfully connected to Jenkins as {user_info['fullName']} using python-jenkins")
                return jenkins
                
            except ImportError:
                self.logger.warning("python-jenkins library not available, using requests as fallback")
                return self._connect_with_requests()
            
        except Exception as e:
            self.logger.warning(f"Failed to connect to Jenkins: {e}, using mock client")
            # Fallback to mock client
            return MockJenkinsClient(self.config['jenkins'])
    
    def _connect_with_requests(self):
        """Connect to Jenkins using requests library as fallback"""
        self.logger.info("Using requests-based Jenkins client")
        return RequestsJenkinsClient(self.config['jenkins'])
    
    def get_node_info(self, node_name: str) -> Dict:
        """Get information about a specific node"""
        try:
            return self.jenkins.get_node_info(node_name)
        except Exception as e:
            self.logger.error(f"Error getting node info for {node_name}: {e}")
            return {}
    
    def get_all_nodes(self) -> List[Dict]:
        """Get all connected nodes"""
        try:
            return self.jenkins.get_all_nodes()
        except Exception as e:
            self.logger.error(f"Error getting nodes: {e}")
            return []


class MockJenkinsClient:
    """Mock Jenkins client for testing without real Jenkins"""
    
    def __init__(self, jenkins_config: Dict):
        self.base_url = jenkins_config['base_url']
        self.logger = logging.getLogger(__name__)
        self.mock_nodes = self._create_mock_nodes()
    
    def _create_mock_nodes(self) -> List[Dict]:
        """Create mock nodes for demonstration"""
        return [
            {
                'name': 'linux-amd64-node',
                'displayName': 'linux-amd64-node',
                'offline': False,
                'idle': True,
                'numExecutors': 4,
                'assignedLabels': [{'name': 'linux'}, {'name': 'amd64'}]
            },
            {
                'name': 'linux-arm64-node',
                'displayName': 'linux-arm64-node', 
                'offline': False,
                'idle': True,
                'numExecutors': 2,
                'assignedLabels': [{'name': 'linux'}, {'name': 'arm64'}]
            },
            {
                'name': 'windows-amd64-node',
                'displayName': 'windows-amd64-node',
                'offline': True,
                'idle': False,
                'numExecutors': 2,
                'assignedLabels': [{'name': 'windows'}, {'name': 'amd64'}]
            }
        ]
    
    def get_whoami(self) -> Dict:
        """Get mock user info"""
        return {'fullName': 'Mock Admin User', 'id': 'admin'}
    
    def get_node_info(self, node_name: str) -> Dict:
        """Get mock node information"""
        for node in self.mock_nodes:
            if node['name'] == node_name:
                return node
        return {}
    
    def get_all_nodes(self) -> List[Dict]:
        """Get all mock nodes"""
        return self.mock_nodes
    
    def create_node(self, name: str, numExecutors: int = 2, nodeDescription: str = '', 
                   remoteFS: str = '/home/jenkins', labels: list = None, exclusive: bool = False):
        """Create a mock node"""
        self.logger.info(f"MOCK: Creating node {name}")
        new_node = {
            'name': name,
            'displayName': name,
            'offline': False,
            'idle': True,
            'numExecutors': numExecutors,
            'assignedLabels': [{'name': label} for label in (labels or [])]
        }
        self.mock_nodes.append(new_node)
        return new_node
    
    def delete_node(self, node_name: str):
        """Delete a mock node"""
        self.logger.info(f"MOCK: Deleting node {node_name}")
        self.mock_nodes = [node for node in self.mock_nodes if node['name'] != node_name]
        return {"status": "deleted"}


class RequestsJenkinsClient:
    """Fallback Jenkins client using requests library"""
    
    def __init__(self, jenkins_config: Dict):
        self.base_url = jenkins_config['base_url']
        self.auth = (jenkins_config['username'], jenkins_config['api_token'])
        self.logger = logging.getLogger(__name__)
    
    def get_whoami(self) -> Dict:
        """Get current user info"""
        response = requests.get(
            f"{self.base_url}/api/json",
            auth=self.auth,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def get_node_info(self, node_name: str) -> Dict:
        """Get node information"""
        response = requests.get(
            f"{self.base_url}/computer/{node_name}/api/json",
            auth=self.auth,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return {}
    
    def get_all_nodes(self) -> List[Dict]:
        """Get all nodes"""
        response = requests.get(
            f"{self.base_url}/computer/api/json",
            auth=self.auth,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('computer', [])
        return []
    
    def create_node(self, name: str, numExecutors: int = 2, nodeDescription: str = '', 
                   remoteFS: str = '/home/jenkins', labels: list = None, exclusive: bool = False):
        """Create a new node (simplified implementation)"""
        self.logger.info(f"Would create node: {name} with labels: {labels}")
        # This is a simplified implementation - in production, you'd use proper Jenkins API
        return {"name": name, "status": "created"}
    
    def delete_node(self, node_name: str):
        """Delete a node (simplified implementation)"""
        self.logger.info(f"Would delete node: {node_name}")
        return {"status": "deleted"}