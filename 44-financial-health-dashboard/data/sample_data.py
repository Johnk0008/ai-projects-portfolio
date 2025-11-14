import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_financial_data():
    """Generate comprehensive sample financial data for SMEs"""
    
    # Generate dates for the last 3 years (36 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Ensure we have at least 12 months of data
    if len(dates) < 12:
        dates = pd.date_range(start=start_date, periods=36, freq='M')
    
    # Base values with realistic growth
    base_revenue = 50000
    growth_rate = 0.02  # 2% monthly growth
    
    financial_data = []
    
    for i, date in enumerate(dates):
        # Revenue with seasonality and growth
        seasonal_factor = 1 + 0.1 * np.sin(i * 2 * np.pi / 12)  # Seasonal variation
        revenue = base_revenue * (1 + growth_rate) ** i * seasonal_factor
        
        # Expenses (60-70% of revenue)
        cogs = revenue * 0.4  # Cost of Goods Sold
        operating_expenses = revenue * 0.25
        salaries = revenue * 0.15
        marketing = revenue * 0.05
        other_expenses = revenue * 0.03
        
        total_expenses = cogs + operating_expenses + salaries + marketing + other_expenses
        
        # Financial metrics
        gross_profit = revenue - cogs
        operating_income = gross_profit - operating_expenses - salaries - marketing
        net_income = operating_income - other_expenses
        
        # Balance sheet items
        cash = max(net_income * 0.3 + np.random.normal(5000, 1000), 1000)
        accounts_receivable = revenue * 0.2
        inventory = cogs * 0.5
        total_assets = cash + accounts_receivable + inventory + 100000  # Fixed assets
        
        accounts_payable = cogs * 0.3
        short_term_debt = 20000
        long_term_debt = 80000
        total_liabilities = accounts_payable + short_term_debt + long_term_debt
        
        equity = total_assets - total_liabilities
        
        # Cash flow
        operating_cash_flow = net_income * 0.8
        investing_cash_flow = -5000  # Regular capital expenditures
        financing_cash_flow = -2000  # Debt repayment
        
        net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
        
        financial_data.append({
            'date': date,
            'revenue': revenue,
            'cogs': cogs,
            'gross_profit': gross_profit,
            'operating_expenses': operating_expenses,
            'salaries': salaries,
            'marketing': marketing,
            'other_expenses': other_expenses,
            'total_expenses': total_expenses,
            'operating_income': operating_income,
            'net_income': net_income,
            'cash': cash,
            'accounts_receivable': accounts_receivable,
            'inventory': inventory,
            'total_assets': total_assets,
            'accounts_payable': accounts_payable,
            'short_term_debt': short_term_debt,
            'long_term_debt': long_term_debt,
            'total_liabilities': total_liabilities,
            'equity': equity,
            'operating_cash_flow': operating_cash_flow,
            'investing_cash_flow': investing_cash_flow,
            'financing_cash_flow': financing_cash_flow,
            'net_cash_flow': net_cash_flow
        })
    
    return pd.DataFrame(financial_data)

def save_sample_data():
    """Save sample data to CSV"""
    df = generate_sample_financial_data()
    df.to_csv('data/financial_data.csv', index=False)
    return df

if __name__ == "__main__":
    save_sample_data()
    print("Sample financial data generated successfully!")