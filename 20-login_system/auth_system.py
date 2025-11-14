from user_manager import UserManager
import getpass

class AuthenticationSystem:
    def __init__(self):
        self.user_manager = UserManager()
        self.current_user = None
    
    def register(self):
        """Handle user registration"""
        print("\n=== REGISTRATION ===")
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        
        # Check if passwords match
        if password != confirm_password:
            print("❌ Error: Passwords do not match!")
            return False
        
        # Attempt to create user
        success, message = self.user_manager.create_user(username, password)
        
        if success:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            return False
    
    def login(self):
        """Handle user login"""
        print("\n=== LOGIN ===")
        username = input("Enter username: ").strip()
        password = getpass.getpass("Enter password: ")
        
        # Attempt to verify user
        success, message = self.user_manager.verify_user(username, password)
        
        if success:
            print(f"✅ {message}")
            self.current_user = username
            return True
        else:
            print(f"❌ {message}")
            return False
    
    def logout(self):
        """Handle user logout"""
        if self.current_user:
            print(f"👋 Goodbye, {self.current_user}!")
            self.current_user = None
        else:
            print("No user is currently logged in.")
    
    def show_users(self):
        """Display all registered users (for admin purposes)"""
        users = self.user_manager.get_all_users()
        if users:
            print(f"\n📊 Registered users ({len(users)}):")
            for user in users:
                print(f"  - {user}")
        else:
            print("\n📊 No users registered yet.")