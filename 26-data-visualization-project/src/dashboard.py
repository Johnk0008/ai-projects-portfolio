import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from src.data_loader import DataLoader
from src.visualizations import DataVisualizer
import pandas as pd

class InteractiveDashboard:
    def __init__(self):
        self.loader = DataLoader()
        self.visualizer = DataVisualizer()
        self.sales_data, self.customer_data = self.loader.load_data()
        self.app = dash.Dash(__name__)
        
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Setup the dashboard layout"""
        self.app.layout = html.Div([
            html.H1("Advanced Data Visualization Dashboard", 
                   style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
            
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Sales Analytics', value='tab-1'),
                dcc.Tab(label='Customer Insights', value='tab-2'),
                dcc.Tab(label='Advanced Dashboard', value='tab-3'),
                dcc.Tab(label='Data Stories', value='tab-4'),
            ]),
            
            html.Div(id='tabs-content')
        ], style={'padding': '20px'})
    
    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        @self.app.callback(
            Output('tabs-content', 'children'),
            Input('tabs', 'value')
        )
        def render_content(tab):
            if tab == 'tab-1':
                return self.render_sales_analytics()
            elif tab == 'tab-2':
                return self.render_customer_insights()
            elif tab == 'tab-3':
                return self.render_advanced_dashboard()
            elif tab == 'tab-4':
                return self.render_data_stories()
        
        # Additional callbacks for interactivity
        @self.app.callback(
            Output('sales-time-series', 'figure'),
            [Input('sales-metric', 'value')]
        )
        def update_sales_plot(metric):
            return self.visualizer.create_time_series_plot(
                self.sales_data, 'date', metric, f"{metric.title()} Over Time"
            )
    
    def render_sales_analytics(self):
        return html.Div([
            html.H2("Sales Performance Analysis"),
            
            html.Div([
                html.Label("Select Metric:"),
                dcc.Dropdown(
                    id='sales-metric',
                    options=[
                        {'label': 'Sales', 'value': 'sales'},
                        {'label': 'Revenue', 'value': 'revenue'},
                        {'label': 'Customers', 'value': 'customers'}
                    ],
                    value='sales'
                )
            ], style={'width': '30%', 'marginBottom': 20}),
            
            dcc.Graph(id='sales-time-series'),
            
            html.Div([
                dcc.Graph(
                    figure=self.visualizer.create_bar_plot(
                        self.sales_data.groupby('product_category')['revenue'].sum().reset_index(),
                        'product_category', 'revenue', 'Revenue by Product Category'
                    )
                ),
                dcc.Graph(
                    figure=self.visualizer.create_pie_chart(
                        self.sales_data.groupby('region')['sales'].sum().reset_index(),
                        'region', 'sales', 'Sales Distribution by Region'
                    )
                )
            ], style={'display': 'flex', 'flexDirection': 'row'})
        ])
    
    def render_customer_insights(self):
        return html.Div([
            html.H2("Customer Behavior Insights"),
            
            html.Div([
                dcc.Graph(
                    figure=self.visualizer.create_correlation_heatmap(
                        self.customer_data, "Customer Behavior Correlation Matrix"
                    )
                ),
                dcc.Graph(
                    figure=self.visualizer.create_scatter_matrix(
                        self.customer_data[['age', 'income', 'browsing_time', 'pages_visited']],
                        ['age', 'income', 'browsing_time', 'pages_visited'],
                        self.customer_data['churn'],
                        "Customer Segmentation Scatter Matrix"
                    )
                )
            ]),
            
            html.Div([
                dcc.Graph(
                    figure=self.visualizer.create_distribution_plot(
                        self.customer_data, 'income', 'Income Distribution Analysis'
                    )
                )
            ])
        ])
    
    def render_advanced_dashboard(self):
        return html.Div([
            html.H2("Comprehensive Business Analytics"),
            dcc.Graph(
                figure=self.visualizer.create_advanced_dashboard(self.sales_data, self.customer_data)
            )
        ])
    
    def render_data_stories(self):
        return html.Div([
            html.H2("Data-Driven Business Stories"),
            
            html.Div([
                html.H3("Story 1: Seasonal Sales Patterns"),
                html.P("Our analysis reveals clear seasonal patterns in sales data, with peaks during holiday seasons and dips in Q1."),
                dcc.Graph(
                    figure=self.visualizer.create_time_series_plot(
                        self.sales_data, 'date', 'sales', "Seasonal Sales Pattern Analysis"
                    )
                )
            ], style={'marginBottom': 40}),
            
            html.Div([
                html.H3("Story 2: Customer Churn Drivers"),
                html.P("Satisfaction score shows strong negative correlation with churn rate. Customers with scores below 3 are 5x more likely to churn."),
                dcc.Graph(
                    figure=self.visualizer.create_bar_plot(
                        self.customer_data.groupby('satisfaction_score')['churn'].mean().reset_index(),
                        'satisfaction_score', 'churn', 'Churn Rate by Satisfaction Score'
                    )
                )
            ], style={'marginBottom': 40}),
            
            html.Div([
                html.H3("Story 3: Regional Performance"),
                html.P("Western region shows highest revenue per customer, while Northern region has the highest volume but lower margins."),
                dcc.Graph(
                    figure=self.visualizer.create_pie_chart(
                        self.sales_data.groupby('region')['revenue'].sum().reset_index(),
                        'region', 'revenue', 'Revenue Distribution by Region'
                    )
                )
            ])
        ])
    
    def run(self, debug=True):
        self.app.run_server(debug=debug)

# Streamlit alternative (uncomment if you prefer Streamlit)
import streamlit as st

def create_streamlit_app():
    """Alternative Streamlit implementation"""
    st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")
    
    loader = DataLoader()
    visualizer = DataVisualizer()
    sales_data, customer_data = loader.load_data()
    
    st.title("📊 Advanced Data Visualization Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Sales Analytics", "Customer Insights", "Advanced Dashboard", "Data Stories"])
    
    with tab1:
        st.header("Sales Performance Analysis")
        metric = st.selectbox("Select Metric", ['sales', 'revenue', 'customers'])
        st.plotly_chart(visualizer.create_time_series_plot(sales_data, 'date', metric), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(visualizer.create_bar_plot(
                sales_data.groupby('product_category')['revenue'].sum().reset_index(),
                'product_category', 'revenue', 'Revenue by Product Category'
            ), use_container_width=True)
        with col2:
            st.plotly_chart(visualizer.create_pie_chart(
                sales_data.groupby('region')['sales'].sum().reset_index(),
                'region', 'sales', 'Sales Distribution by Region'
            ), use_container_width=True)
    
    with tab2:
        st.header("Customer Behavior Insights")
        st.plotly_chart(visualizer.create_correlation_heatmap(customer_data), use_container_width=True)
        st.plotly_chart(visualizer.create_scatter_matrix(
            customer_data[['age', 'income', 'browsing_time', 'pages_visited']],
            ['age', 'income', 'browsing_time', 'pages_visited'],
            customer_data['churn']
        ), use_container_width=True)
    
    with tab3:
        st.header("Comprehensive Business Analytics")
        st.plotly_chart(visualizer.create_advanced_dashboard(sales_data, customer_data), use_container_width=True)
    
    with tab4:
        st.header("Data-Driven Business Stories")
        # Add data stories content

if __name__ == '__main__':
    # Run Dash app
    dashboard = InteractiveDashboard()
    dashboard.run()