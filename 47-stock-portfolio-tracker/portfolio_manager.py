class PortfolioManager:
    def __init__(self):
        # Hardcoded stock prices dictionary
        self.stock_prices = {
            "AAPL": 180.50,
            "TSLA": 250.75,
            "GOOGL": 135.20,
            "MSFT": 330.80,
            "AMZN": 145.60,
            "NVDA": 450.25,
            "META": 310.40,
            "NFLX": 485.15
        }
        
        self.portfolio = {}
    
    def add_stock(self, stock_symbol, quantity):
        """Add stock to portfolio"""
        stock_symbol = stock_symbol.upper()
        
        if stock_symbol not in self.stock_prices:
            return False, f"Stock {stock_symbol} not found in our database"
        
        if stock_symbol in self.portfolio:
            self.portfolio[stock_symbol] += quantity
        else:
            self.portfolio[stock_symbol] = quantity
        
        return True, f"Added {quantity} shares of {stock_symbol}"
    
    def remove_stock(self, stock_symbol, quantity):
        """Remove stock from portfolio"""
        stock_symbol = stock_symbol.upper()
        
        if stock_symbol not in self.portfolio:
            return False, f"Stock {stock_symbol} not in portfolio"
        
        if self.portfolio[stock_symbol] < quantity:
            return False, f"Not enough shares of {stock_symbol} to remove"
        
        self.portfolio[stock_symbol] -= quantity
        
        if self.portfolio[stock_symbol] == 0:
            del self.portfolio[stock_symbol]
        
        return True, f"Removed {quantity} shares of {stock_symbol}"
    
    def calculate_total_investment(self):
        """Calculate total portfolio value"""
        total_value = 0
        stock_details = []
        
        for stock, quantity in self.portfolio.items():
            if stock in self.stock_prices:
                stock_value = self.stock_prices[stock] * quantity
                total_value += stock_value
                stock_details.append({
                    'symbol': stock,
                    'quantity': quantity,
                    'price': self.stock_prices[stock],
                    'value': stock_value
                })
        
        return total_value, stock_details
    
    def get_available_stocks(self):
        """Return list of available stocks"""
        return list(self.stock_prices.keys())
    
    def display_portfolio(self):
        """Display current portfolio"""
        if not self.portfolio:
            print("Portfolio is empty")
            return
        
        total_value, stock_details = self.calculate_total_investment()
        
        print("\n" + "="*50)
        print("PORTFOLIO SUMMARY")
        print("="*50)
        
        for detail in stock_details:
            print(f"{detail['symbol']}: {detail['quantity']} shares "
                  f"@ ${detail['price']:.2f} = ${detail['value']:.2f}")
        
        print("-"*50)
        print(f"TOTAL INVESTMENT: ${total_value:.2f}")
        print("="*50)
    
    def save_to_file(self, filename="portfolio_summary.txt"):
        """Save portfolio to text file"""
        total_value, stock_details = self.calculate_total_investment()
        
        with open(filename, 'w') as file:
            file.write("STOCK PORTFOLIO TRACKER - SUMMARY\n")
            file.write("="*40 + "\n")
            file.write(f"Generated on: {self._get_current_timestamp()}\n\n")
            
            for detail in stock_details:
                file.write(f"{detail['symbol']}: {detail['quantity']} shares "
                          f"@ ${detail['price']:.2f} = ${detail['value']:.2f}\n")
            
            file.write("-"*40 + "\n")
            file.write(f"TOTAL INVESTMENT: ${total_value:.2f}\n")
            file.write("="*40 + "\n")
        
        print(f"Portfolio saved to {filename}")
    
    def save_to_csv(self, filename="portfolio_data.csv"):
        """Save portfolio to CSV file"""
        import csv
        
        total_value, stock_details = self.calculate_total_investment()
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Stock Symbol', 'Quantity', 'Price', 'Total Value'])
            
            for detail in stock_details:
                writer.writerow([
                    detail['symbol'],
                    detail['quantity'],
                    f"${detail['price']:.2f}",
                    f"${detail['value']:.2f}"
                ])
            
            writer.writerow([])
            writer.writerow(['TOTAL INVESTMENT', '', '', f"${total_value:.2f}"])
        
        print(f"Portfolio data saved to {filename}")
    
    def _get_current_timestamp(self):
        """Get current timestamp for file saving"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")