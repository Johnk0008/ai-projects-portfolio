from auth_system import AuthenticationSystem
import os

class LoginRegistrationApp:
    def __init__(self):
        self.auth_system = AuthenticationSystem()
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("🔐 LOGIN & REGISTRATION SYSTEM")
        print("="*50)
        
        if self.auth_system.current_user:
            print(f"👤 Currently logged in as: {self.auth_system.current_user}")
            print("1. Logout")
            print("2. Show Registered Users")
            print("3. Exit")
        else:
            print("1. Register")
            print("2. Login")
            print("3. Show Registered Users")
            print("4. Exit")
        
        print("="*50)
    
    def run(self):
        """Run the main application loop"""
        print("🚀 Welcome to the Secure Login & Registration System!")
        
        while True:
            self.display_menu()
            
            try:
                if self.auth_system.current_user:
                    choice = input("Enter your choice (1-3): ").strip()
                else:
                    choice = input("Enter your choice (1-4): ").strip()
                
                if self.auth_system.current_user:
                    # User is logged in
                    if choice == '1':
                        self.auth_system.logout()
                    elif choice == '2':
                        self.auth_system.show_users()
                    elif choice == '3':
                        print("👋 Thank you for using our system!")
                        break
                    else:
                        print("❌ Invalid choice! Please try again.")
                
                else:
                    # User is not logged in
                    if choice == '1':
                        self.auth_system.register()
                    elif choice == '2':
                        if self.auth_system.login():
                            # Login successful
                            pass
                    elif choice == '3':
                        self.auth_system.show_users()
                    elif choice == '4':
                        print("👋 Thank you for using our system!")
                        break
                    else:
                        print("❌ Invalid choice! Please try again.")
                        
            except KeyboardInterrupt:
                print("\n\n👋 Program interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")

def main():
    app = LoginRegistrationApp()
    app.run()

if __name__ == "__main__":
    main()