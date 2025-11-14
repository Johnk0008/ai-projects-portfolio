import json
import os
from typing import Dict, Optional, Tuple
from security import SecurityManager

class UserManager:
    def __init__(self, users_dir: str = "users"):
        self.users_dir = users_dir
        self._ensure_users_directory()
    
    def _ensure_users_directory(self):
        """Create users directory if it doesn't exist"""
        if not os.path.exists(self.users_dir):
            os.makedirs(self.users_dir)
    
    def user_exists(self, username: str) -> bool:
        """Check if a user already exists"""
        user_file = os.path.join(self.users_dir, f"{username}.json")
        return os.path.exists(user_file)
    
    def create_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Create a new user with hashed password"""
        # Validate inputs
        valid_username, username_msg = SecurityManager.validate_username(username)
        if not valid_username:
            return False, username_msg
        
        valid_password, password_msg = SecurityManager.validate_password(password)
        if not valid_password:
            return False, password_msg
        
        # Check for duplicate username
        if self.user_exists(username):
            return False, "Username already exists"
        
        # Hash password and store user data
        salt, password_hash = SecurityManager.hash_password(password)
        user_data = {
            "username": username,
            "salt": salt,
            "password_hash": password_hash
        }
        
        # Save to file
        user_file = os.path.join(self.users_dir, f"{username}.json")
        try:
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2)
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Error saving user data: {str(e)}"
    
    def verify_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Verify user credentials"""
        if not self.user_exists(username):
            return False, "Username not found"
        
        # Load user data
        user_file = os.path.join(self.users_dir, f"{username}.json")
        try:
            with open(user_file, 'r') as f:
                user_data = json.load(f)
            
            # Verify password
            if SecurityManager.verify_password(
                password, 
                user_data["salt"], 
                user_data["password_hash"]
            ):
                return True, "Login successful"
            else:
                return False, "Invalid password"
                
        except Exception as e:
            return False, f"Error reading user data: {str(e)}"
    
    def get_all_users(self) -> list:
        """Get list of all registered usernames"""
        users = []
        try:
            for filename in os.listdir(self.users_dir):
                if filename.endswith('.json'):
                    username = filename[:-5]  # Remove .json extension
                    users.append(username)
        except Exception as e:
            print(f"Error reading users: {e}")
        return users