import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class DataVisualizer:
    def __init__(self, style='seaborn'):
        plt.style.use(style)
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        sns.set_palette(self.colors)
    
    def create_time_series_plot(self, data, date_col, value_col, title="Time Series Analysis"):
        """Create interactive time series plot"""
        fig = px.line(data, x=date_col, y=value_col, 
                     title=title, template='plotly_white')
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=value_col.replace('_', ' ').title(),
            hovermode='x unified'
        )
        return fig
    
    def create_correlation_heatmap(self, data, title="Correlation Matrix"):
        """Create correlation heatmap"""
        corr_matrix = data.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu_r',
            zmin=-1,
            zmax=1,
            hoverongaps=False,
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Features",
            yaxis_title="Features",
            template='plotly_white'
        )
        return fig
    
    def create_distribution_plot(self, data, column, title="Distribution Plot"):
        """Create distribution plot with multiple visualizations"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Histogram', 'Box Plot', 'Violin Plot', 'ECDF'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Histogram
        fig.add_trace(go.Histogram(x=data[column], name='Histogram', nbinsx=30), row=1, col=1)
        
        # Box plot
        fig.add_trace(go.Box(y=data[column], name='Box Plot'), row=1, col=2)
        
        # Violin plot
        fig.add_trace(go.Violin(y=data[column], name='Violin Plot'), row=2, col=1)
        
        # ECDF
        x_ecdf = np.sort(data[column])
        y_ecdf = np.arange(1, len(x_ecdf)+1) / len(x_ecdf)
        fig.add_trace(go.Scatter(x=x_ecdf, y=y_ecdf, mode='lines', name='ECDF'), row=2, col=2)
        
        fig.update_layout(height=600, title=title, template='plotly_white')
        return fig
    
    def create_scatter_matrix(self, data, columns, color_col=None, title="Scatter Matrix"):
        """Create scatter plot matrix"""
        fig = px.scatter_matrix(data, dimensions=columns, color=color_col,
                               title=title, template='plotly_white')
        fig.update_traces(diagonal_visible=False)
        return fig
    
    def create_bar_plot(self, data, x_col, y_col, title="Bar Plot", orientation='v'):
        """Create bar plot with different orientations"""
        if orientation == 'v':
            fig = px.bar(data, x=x_col, y=y_col, title=title, template='plotly_white')
        else:
            fig = px.bar(data, x=y_col, y=x_col, title=title, template='plotly_white', orientation='h')
        
        fig.update_layout(
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title()
        )
        return fig
    
    def create_pie_chart(self, data, names_col, values_col, title="Pie Chart"):
        """Create interactive pie chart"""
        fig = px.pie(data, names=names_col, values=values_col, title=title,
                    template='plotly_white', hole=0.3)
        return fig
    
    def create_advanced_dashboard(self, sales_data, customer_data):
        """Create an advanced dashboard with multiple plots"""
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=[
                'Sales Trend Over Time', 'Revenue by Product Category',
                'Customer Distribution by Age', 'Correlation Heatmap',
                'Purchase Frequency vs Income', 'Churn Rate by Satisfaction',
                'Regional Sales Performance', 'Browsing Time Distribution',
                'Customer Segmentation'
            ],
            specs=[
                [{"type": "scatter"}, {"type": "bar"}, {"type": "histogram"}],
                [{"type": "heatmap"}, {"type": "scatter"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "violin"}, {"type": "scatter"}]
            ]
        )
        
        # Sales trend
        sales_data['date'] = pd.to_datetime(sales_data['date'])
        monthly_sales = sales_data.groupby(sales_data['date'].dt.to_period('M'))['sales'].sum().reset_index()
        monthly_sales['date'] = monthly_sales['date'].astype(str)
        
        fig.add_trace(
            go.Scatter(x=monthly_sales['date'], y=monthly_sales['sales'], mode='lines+markers'),
            row=1, col=1
        )
        
        # Revenue by category
        category_revenue = sales_data.groupby('product_category')['revenue'].sum().reset_index()
        fig.add_trace(
            go.Bar(x=category_revenue['product_category'], y=category_revenue['revenue']),
            row=1, col=2
        )
        
        # Age distribution
        fig.add_trace(
            go.Histogram(x=customer_data['age'] * 50 + 20),  # Scale to realistic ages
            row=1, col=3
        )
        
        # Correlation heatmap (simplified)
        corr = customer_data[['age', 'income', 'browsing_time', 'pages_visited']].corr()
        fig.add_trace(
            go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns),
            row=2, col=1
        )
        
        # Purchase frequency vs income
        fig.add_trace(
            go.Scatter(x=customer_data['income'], y=customer_data['purchase_frequency'], mode='markers'),
            row=2, col=2
        )
        
        # Churn by satisfaction
        churn_by_satisfaction = customer_data.groupby('satisfaction_score')['churn'].mean().reset_index()
        fig.add_trace(
            go.Bar(x=churn_by_satisfaction['satisfaction_score'], y=churn_by_satisfaction['churn']),
            row=2, col=3
        )
        
        # Regional sales
        regional_sales = sales_data.groupby('region')['sales'].sum().reset_index()
        fig.add_trace(
            go.Bar(x=regional_sales['region'], y=regional_sales['sales']),
            row=3, col=1
        )
        
        # Browsing time distribution
        fig.add_trace(
            go.Violin(y=customer_data['browsing_time']),
            row=3, col=2
        )
        
        # Customer segmentation
        fig.add_trace(
            go.Scatter(x=customer_data['income'], y=customer_data['pages_visited'], 
                      mode='markers', marker=dict(color=customer_data['churn'])),
            row=3, col=3
        )
        
        fig.update_layout(height=900, title_text="Comprehensive Business Analytics Dashboard", showlegend=False)
        return fig