from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import os

from data.sample_data import generate_sample_financial_data, save_sample_data
from models.financial_analysis import FinancialAnalyzer
from models.forecasting import FinancialForecaster

app = Flask(__name__)

# Load or generate sample data
try:
    financial_data = pd.read_csv('data/financial_data.csv')
except FileNotFoundError:
    financial_data = generate_sample_financial_data()
    os.makedirs('data', exist_ok=True)
    financial_data.to_csv('data/financial_data.csv', index=False)

# Initialize analyzers
analyzer = FinancialAnalyzer(financial_data)
forecaster = FinancialForecaster(financial_data)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/financial-summary')
def financial_summary():
    summary, full_data = analyzer.get_financial_summary()
    return jsonify(summary)

@app.route('/api/income-statement')
def income_statement():
    df = analyzer.calculate_profitability_metrics()
    
    # Create income statement trend chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['revenue'], 
        name='Revenue', 
        line=dict(color='#1f77b4')
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['gross_profit'], 
        name='Gross Profit', 
        line=dict(color='#ff7f0e')
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['net_income'], 
        name='Net Income', 
        line=dict(color='#2ca02c')
    ))
    
    fig.update_layout(
        title='Income Statement Trends',
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        template='plotly_white'
    )
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'chart': chart_json,
        'data': df.tail(12).to_dict('records')
    })

@app.route('/api/profitability-metrics')
def profitability_metrics():
    df = analyzer.calculate_profitability_metrics()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['gross_margin'], 
        name='Gross Margin', 
        line=dict(color='#1f77b4')
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['operating_margin'], 
        name='Operating Margin', 
        line=dict(color='#ff7f0e')
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['net_margin'], 
        name='Net Margin', 
        line=dict(color='#2ca02c')
    ))
    
    fig.update_layout(
        title='Profitability Margins Over Time',
        xaxis_title='Date',
        yaxis_title='Margin (%)',
        template='plotly_white'
    )
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'chart': chart_json,
        'current_margins': {
            'gross_margin': df['gross_margin'].iloc[-1],
            'operating_margin': df['operating_margin'].iloc[-1],
            'net_margin': df['net_margin'].iloc[-1]
        }
    })

@app.route('/api/balance-sheet')
def balance_sheet():
    df = analyzer.calculate_liquidity_ratios()
    
    # Assets breakdown
    latest = df.iloc[-1]
    assets_data = {
        'Cash': latest['cash'],
        'Accounts Receivable': latest['accounts_receivable'],
        'Inventory': latest['inventory'],
        'Other Assets': latest['total_assets'] - (latest['cash'] + latest['accounts_receivable'] + latest['inventory'])
    }
    
    # Liabilities and Equity
    liabilities_equity = {
        'Accounts Payable': latest['accounts_payable'],
        'Short-term Debt': latest['short_term_debt'],
        'Long-term Debt': latest['long_term_debt'],
        'Equity': latest['equity']
    }
    
    # Liquidity ratios trend
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['current_ratio'], 
        name='Current Ratio', 
        line=dict(color='#1f77b4')
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['quick_ratio'], 
        name='Quick Ratio', 
        line=dict(color='#ff7f0e')
    ))
    
    fig.update_layout(
        title='Liquidity Ratios Trend',
        xaxis_title='Date',
        yaxis_title='Ratio',
        template='plotly_white'
    )
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'assets': assets_data,
        'liabilities_equity': liabilities_equity,
        'liquidity_chart': chart_json,
        'current_ratio': latest['current_ratio'],
        'quick_ratio': latest['quick_ratio']
    })

@app.route('/api/cash-flow')
def cash_flow():
    df = financial_data.copy()
    
    # Cash flow trends
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['operating_cash_flow'], 
        name='Operating Cash Flow', 
        line=dict(color='#1f77b4')
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['investing_cash_flow'], 
        name='Investing Cash Flow', 
        line=dict(color='#ff7f0e')
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['financing_cash_flow'], 
        name='Financing Cash Flow', 
        line=dict(color='#2ca02c')
    ))
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['net_cash_flow'], 
        name='Net Cash Flow', 
        line=dict(color='#d62728', dash='dash')
    ))
    
    fig.update_layout(
        title='Cash Flow Statement Trends',
        xaxis_title='Date',
        yaxis_title='Cash Flow ($)',
        template='plotly_white'
    )
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'chart': chart_json,
        'cash_flow_data': df.tail(12).to_dict('records')
    })

@app.route('/api/forecast')
def get_forecast():
    periods = request.args.get('periods', 12, type=int)
    forecast_df = forecaster.forecast_income_statement(periods)
    
    # Combine historical and forecast data
    historical = financial_data[['date', 'revenue', 'net_income']].copy()
    historical['type'] = 'Historical'
    
    forecast_plot = forecast_df[['date', 'revenue', 'net_income']].copy()
    forecast_plot['type'] = 'Forecast'
    
    combined = pd.concat([historical, forecast_plot])
    
    # Create forecast chart
    fig = go.Figure()
    
    # Historical data
    hist_data = combined[combined['type'] == 'Historical']
    fig.add_trace(go.Scatter(
        x=hist_data['date'], 
        y=hist_data['revenue'],
        name='Revenue (Historical)', 
        line=dict(color='#1f77b4')
    ))
    fig.add_trace(go.Scatter(
        x=hist_data['date'], 
        y=hist_data['net_income'],
        name='Net Income (Historical)', 
        line=dict(color='#2ca02c')
    ))
    
    # Forecast data
    forecast_data = combined[combined['type'] == 'Forecast']
    fig.add_trace(go.Scatter(
        x=forecast_data['date'], 
        y=forecast_data['revenue'],
        name='Revenue (Forecast)', 
        line=dict(color='#1f77b4', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=forecast_data['date'], 
        y=forecast_data['net_income'],
        name='Net Income (Forecast)', 
        line=dict(color='#2ca02c', dash='dash')
    ))
    
    fig.update_layout(
        title=f'Financial Forecast - Next {periods} Months',
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        template='plotly_white'
    )
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'forecast_chart': chart_json,
        'forecast_data': forecast_df.to_dict('records')
    })

@app.route('/api/trends')
def get_trends():
    trends = analyzer.get_income_statement_trends()
    
    # Expense breakdown pie chart
    expense_data = trends['expense_breakdown']
    fig = px.pie(
        values=list(expense_data.values()),
        names=list(expense_data.keys()),
        title='Expense Breakdown (% of Revenue)'
    )
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'expense_breakdown_chart': chart_json,
        'trends': trends
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)