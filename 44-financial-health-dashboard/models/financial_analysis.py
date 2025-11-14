import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class FinancialAnalyzer:
    def __init__(self, data):
        self.data = data
        self.data['date'] = pd.to_datetime(self.data['date'])
    
    def calculate_profitability_metrics(self):
        """Calculate key profitability ratios"""
        df = self.data.copy()
        
        # Profitability ratios
        df['gross_margin'] = (df['gross_profit'] / df['revenue']) * 100
        df['operating_margin'] = (df['operating_income'] / df['revenue']) * 100
        df['net_margin'] = (df['net_income'] / df['revenue']) * 100
        df['roa'] = (df['net_income'] / df['total_assets']) * 100  # Return on Assets
        df['roe'] = (df['net_income'] / df['equity']) * 100  # Return on Equity
        
        # Efficiency ratios
        df['asset_turnover'] = df['revenue'] / df['total_assets']
        
        return df
    
    def calculate_liquidity_ratios(self):
        """Calculate liquidity ratios"""
        df = self.data.copy()
        
        df['current_ratio'] = (df['cash'] + df['accounts_receivable'] + df['inventory']) / df['accounts_payable']
        df['quick_ratio'] = (df['cash'] + df['accounts_receivable']) / df['accounts_payable']
        df['cash_ratio'] = df['cash'] / df['accounts_payable']
        
        return df
    
    def calculate_leverage_ratios(self):
        """Calculate leverage/solvency ratios"""
        df = self.data.copy()
        
        df['debt_to_equity'] = df['total_liabilities'] / df['equity']
        df['debt_to_assets'] = df['total_liabilities'] / df['total_assets']
        df['interest_coverage'] = df['operating_income'] / (df['total_liabilities'] * 0.05)  # Assuming 5% interest
        
        return df
    
    def get_financial_summary(self):
        """Generate comprehensive financial summary"""
        df = self.calculate_profitability_metrics()
        df = self.calculate_liquidity_ratios()
        df = self.calculate_leverage_ratios()
        
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else latest
        
        summary = {
            'revenue': {
                'current': latest['revenue'],
                'growth': ((latest['revenue'] - previous['revenue']) / previous['revenue']) * 100
            },
            'net_income': {
                'current': latest['net_income'],
                'growth': ((latest['net_income'] - previous['net_income']) / previous['net_income']) * 100
            },
            'gross_margin': {
                'current': latest['gross_margin'],
                'change': latest['gross_margin'] - previous['gross_margin']
            },
            'current_ratio': {
                'current': latest['current_ratio'],
                'change': latest['current_ratio'] - previous['current_ratio']
            },
            'debt_to_equity': {
                'current': latest['debt_to_equity'],
                'change': latest['debt_to_equity'] - previous['debt_to_equity']
            }
        }
        
        return summary, df
    
    def get_income_statement_trends(self):
        """Analyze income statement trends"""
        df = self.calculate_profitability_metrics()
        
        trends = {
            'revenue_growth': df['revenue'].pct_change().mean() * 100,
            'profit_margin_trend': df['net_margin'].diff().mean(),
            'expense_breakdown': {
                'cogs_percentage': (df['cogs'].mean() / df['revenue'].mean()) * 100,
                'operating_expenses_percentage': (df['operating_expenses'].mean() / df['revenue'].mean()) * 100,
                'salaries_percentage': (df['salaries'].mean() / df['revenue'].mean()) * 100
            }
        }
        
        return trends