from portfolio_manager import PortfolioManager

def display_menu():
    """Display main menu options"""
    print("\n" + "="*40)
    print("STOCK PORTFOLIO TRACKER")
    print("="*40)
    print("1. Add Stock to Portfolio")
    print("2. Remove Stock from Portfolio")
    print("3. View Portfolio")
    print("4. Calculate Total Investment")
    print("5. Save Portfolio to Text File")
    print("6. Save Portfolio to CSV File")
    print("7. View Available Stocks")
    print("8. Exit")
    print("-"*40)

def get_user_choice():
    """Get and validate user menu choice"""
    try:
        choice = int(input("Enter your choice (1-8): "))
        return choice
    except ValueError:
        print("Please enter a valid number!")
        return None

def add_stock_interaction(portfolio_manager):
    """Handle add stock user interaction"""
    print("\n--- ADD STOCK TO PORTFOLIO ---")
    
    # Show available stocks
    available_stocks = portfolio_manager.get_available_stocks()
    print(f"Available stocks: {', '.join(available_stocks)}")
    
    stock_symbol = input("Enter stock symbol: ").strip()
    
    try:
        quantity = int(input("Enter quantity: "))
        if quantity <= 0:
            print("Quantity must be positive!")
            return
    except ValueError:
        print("Please enter a valid quantity!")
        return
    
    success, message = portfolio_manager.add_stock(stock_symbol, quantity)
    print(message)

def remove_stock_interaction(portfolio_manager):
    """Handle remove stock user interaction"""
    print("\n--- REMOVE STOCK FROM PORTFOLIO ---")
    
    if not portfolio_manager.portfolio:
        print("Portfolio is empty!")
        return
    
    portfolio_manager.display_portfolio()
    
    stock_symbol = input("Enter stock symbol to remove: ").strip()
    
    try:
        quantity = int(input("Enter quantity to remove: "))
        if quantity <= 0:
            print("Quantity must be positive!")
            return
    except ValueError:
        print("Please enter a valid quantity!")
        return
    
    success, message = portfolio_manager.remove_stock(stock_symbol, quantity)
    print(message)

def main():
    """Main application function"""
    portfolio_manager = PortfolioManager()
    
    print("Welcome to Stock Portfolio Tracker!")
    print("Track your investments with ease.")
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == 1:
            add_stock_interaction(portfolio_manager)
        
        elif choice == 2:
            remove_stock_interaction(portfolio_manager)
        
        elif choice == 3:
            portfolio_manager.display_portfolio()
        
        elif choice == 4:
            total_value, stock_details = portfolio_manager.calculate_total_investment()
            if stock_details:
                portfolio_manager.display_portfolio()
            else:
                print("Portfolio is empty!")
        
        elif choice == 5:
            if portfolio_manager.portfolio:
                filename = input("Enter filename (or press Enter for default): ").strip()
                if not filename:
                    portfolio_manager.save_to_file()
                else:
                    portfolio_manager.save_to_file(filename)
            else:
                print("Portfolio is empty! Nothing to save.")
        
        elif choice == 6:
            if portfolio_manager.portfolio:
                filename = input("Enter filename (or press Enter for default): ").strip()
                if not filename:
                    portfolio_manager.save_to_csv()
                else:
                    portfolio_manager.save_to_csv(filename)
            else:
                print("Portfolio is empty! Nothing to save.")
        
        elif choice == 7:
            available_stocks = portfolio_manager.get_available_stocks()
            print("\nAvailable Stocks:")
            print("-" * 20)
            for stock in available_stocks:
                price = portfolio_manager.stock_prices[stock]
                print(f"{stock}: ${price:.2f}")
        
        elif choice == 8:
            print("Thank you for using Stock Portfolio Tracker!")
            break
        
        else:
            print("Invalid choice! Please select 1-8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()