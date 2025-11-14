import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from src.data_processing import HRDataProcessor
from src.analytics import HRAnalytics
from src.predictive_modeling import HRPredictiveModels

# Initialize data and models
processor = HRDataProcessor()
df = processor.generate_sample_data(1000)
analytics = HRAnalytics(df)
predictive_models = HRPredictiveModels(df)

# Calculate metrics
recruitment_metrics = processor.calculate_recruitment_metrics()
turnover_metrics = processor.calculate_turnover_metrics()
satisfaction_analysis = analytics.satisfaction_analysis()
performance_analysis = analytics.performance_analysis()
attrition_results = predictive_models.train_attrition_model()
hiring_forecast = predictive_models.forecast_hiring_needs()

# Save models
predictive_models.save_models()

# Fix negative salary values for visualization
df['salary_positive'] = df['salary'].apply(lambda x: max(x, 30000))  # Ensure minimum positive value

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("HR Analytics Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # Key Metrics Section
    html.Div([
        html.Div([
            html.H3("Overall Turnover Rate", style={'color': '#e74c3c'}),
            html.H2(f"{turnover_metrics['overall_turnover_rate']:.1f}%")
        ], className='four columns metric-box'),
        
        html.Div([
            html.H3("Avg Satisfaction Score", style={'color': '#27ae60'}),
            html.H2(f"{df['satisfaction_score'].mean():.1f}/5.0")
        ], className='four columns metric-box'),
        
        html.Div([
            html.H3("Hiring Forecast (12M)", style={'color': '#3498db'}),
            html.H2(f"{hiring_forecast['total_hiring_needs']}")
        ], className='four columns metric-box')
    ], className='row'),
    
    # Charts Section
    html.Div([
        # Turnover by Department
        html.Div([
            dcc.Graph(
                id='turnover-by-dept',
                figure=px.bar(
                    x=list(turnover_metrics['turnover_by_department'].keys()),
                    y=list(turnover_metrics['turnover_by_department'].values()),
                    title="Turnover Rate by Department",
                    labels={'x': 'Department', 'y': 'Turnover Rate (%)'},
                    color=list(turnover_metrics['turnover_by_department'].values()),
                    color_continuous_scale='Reds'
                )
            )
        ], className='six columns'),
        
        # Recruitment Source Effectiveness
        html.Div([
            dcc.Graph(
                id='recruitment-sources',
                figure=px.pie(
                    values=list(recruitment_metrics['source_effectiveness'].values()),
                    names=list(recruitment_metrics['source_effectiveness'].keys()),
                    title="Recruitment Sources"
                )
            )
        ], className='six columns')
    ], className='row'),
    
    # Performance and Satisfaction
    html.Div([
        html.Div([
            dcc.Graph(
                id='performance-satisfaction',
                figure=px.scatter(
                    df, x='satisfaction_score', y='performance_rating',
                    color='department', 
                    size='salary_positive',  # Use corrected salary values
                    title="Performance vs Satisfaction by Department",
                    size_max=15  # Limit maximum size
                )
            )
        ], className='six columns'),
        
        # Department Hiring Needs
        html.Div([
            dcc.Graph(
                id='hiring-needs',
                figure=px.bar(
                    x=list(hiring_forecast['department_hiring_needs'].keys()),
                    y=list(hiring_forecast['department_hiring_needs'].values()),
                    title="12-Month Hiring Forecast by Department",
                    color=list(hiring_forecast['department_hiring_needs'].values()),
                    color_continuous_scale='Blues'
                )
            )
        ], className='six columns')
    ], className='row'),
    
    # Feature Importance for Attrition
    html.Div([
        dcc.Graph(
            id='feature-importance',
            figure=px.bar(
                pd.DataFrame(attrition_results['feature_importance']),
                x='importance', y='feature',
                title="Feature Importance for Attrition Prediction",
                orientation='h',
                color='importance',
                color_continuous_scale='Viridis'
            )
        )
    ], className='row'),
    
    # Additional CSS Styling
    html.Div(style={'margin-top': '50px'})
])

# Add CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>HR Analytics Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            .metric-box {
                background: white;
                padding: 20px;
                margin: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            }
            .row {
                display: flex;
                flex-wrap: wrap;
                margin: 20px 0;
            }
            .six.columns {
                width: 48%;
                margin: 1%;
            }
            .four.columns {
                width: 31%;
                margin: 1%;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)