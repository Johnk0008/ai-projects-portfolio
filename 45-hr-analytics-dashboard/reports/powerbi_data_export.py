import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to Python path to import src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import the modules
from src.data_processing import HRDataProcessor
from src.analytics import HRAnalytics
from src.predictive_modeling import HRPredictiveModels

def export_data_for_powerbi():
    """Export processed data for Power BI"""
    print("Initializing HR Data Processor...")
    processor = HRDataProcessor()
    
    print("Generating sample data...")
    df = processor.generate_sample_data(1000)
    
    print("Performing analytics...")
    analytics = HRAnalytics(df)
    predictive_models = HRPredictiveModels(df)
    
    # Calculate all metrics
    print("Calculating recruitment metrics...")
    recruitment_metrics = processor.calculate_recruitment_metrics()
    
    print("Calculating turnover metrics...")
    turnover_metrics = processor.calculate_turnover_metrics()
    
    print("Analyzing satisfaction...")
    satisfaction_analysis = analytics.satisfaction_analysis()
    
    print("Analyzing performance...")
    performance_analysis = analytics.performance_analysis()
    
    print("Training predictive models...")
    attrition_results = predictive_models.train_attrition_model()
    
    print("Forecasting hiring needs...")
    hiring_forecast = predictive_models.forecast_hiring_needs()

    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)

    # Export main dataset to CSV for Power BI
    print("Exporting main dataset...")
    df.to_csv('reports/hr_analytics_data.csv', index=False)
    
    # Export metrics summary
    print("Exporting metrics...")
    metrics_df = pd.DataFrame({
        'metric': ['turnover_rate', 'avg_satisfaction', 'hiring_forecast'],
        'value': [turnover_metrics['overall_turnover_rate'], 
                 df['satisfaction_score'].mean(),
                 hiring_forecast['total_hiring_needs']]
    })
    metrics_df.to_csv('reports/hr_metrics.csv', index=False)
    
    # Export department-wise metrics
    print("Exporting department metrics...")
    dept_metrics = []
    for dept in df['department'].unique():
        dept_data = df[df['department'] == dept]
        dept_metrics.append({
            'department': dept,
            'employee_count': len(dept_data),
            'turnover_rate': turnover_metrics['turnover_by_department'].get(dept, 0),
            'avg_salary': dept_data['salary'].mean(),
            'avg_satisfaction': dept_data['satisfaction_score'].mean(),
            'avg_performance': dept_data['performance_rating'].mean(),
            'hiring_need': hiring_forecast['department_hiring_needs'].get(dept, 0)
        })
    
    dept_metrics_df = pd.DataFrame(dept_metrics)
    dept_metrics_df.to_csv('reports/department_metrics.csv', index=False)
    
    # Export turnover analysis
    print("Exporting turnover analysis...")
    turnover_df = pd.DataFrame({
        'category': list(turnover_metrics['turnover_by_department'].keys()),
        'turnover_rate': list(turnover_metrics['turnover_by_department'].values()),
        'type': 'department'
    })
    
    # Add position turnover
    position_turnover = pd.DataFrame({
        'category': list(turnover_metrics['turnover_by_position'].keys()),
        'turnover_rate': list(turnover_metrics['turnover_by_position'].values()),
        'type': 'position'
    })
    
    turnover_analysis_df = pd.concat([turnover_df, position_turnover], ignore_index=True)
    turnover_analysis_df.to_csv('reports/turnover_analysis.csv', index=False)
    
    # Export recruitment metrics
    print("Exporting recruitment metrics...")
    recruitment_df = pd.DataFrame({
        'source': list(recruitment_metrics['source_effectiveness'].keys()),
        'count': list(recruitment_metrics['source_effectiveness'].values())
    })
    recruitment_df.to_csv('reports/recruitment_sources.csv', index=False)
    
    # Export feature importance for Power BI
    print("Exporting feature importance...")
    feature_importance_df = pd.DataFrame(attrition_results['feature_importance'])
    feature_importance_df.to_csv('reports/feature_importance.csv', index=False)
    
    # Export satisfaction correlation
    print("Exporting satisfaction analysis...")
    satisfaction_corr_df = pd.DataFrame({
        'factor': list(satisfaction_analysis['satisfaction_correlation'].keys()),
        'correlation': list(satisfaction_analysis['satisfaction_correlation'].values())
    })
    satisfaction_corr_df.to_csv('reports/satisfaction_correlation.csv', index=False)
    
    # Export performance metrics
    print("Exporting performance metrics...")
    performance_dept_df = pd.DataFrame({
        'department': list(performance_analysis['performance_by_department'].keys()),
        'avg_performance': list(performance_analysis['performance_by_department'].values())
    })
    performance_dept_df.to_csv('reports/performance_by_department.csv', index=False)
    
    print("\n" + "="*50)
    print("DATA EXPORT COMPLETED SUCCESSFULLY!")
    print("="*50)
    print(f"Main dataset: {len(df)} employees exported")
    print(f"Departments analyzed: {len(df['department'].unique())}")
    print(f"Overall turnover rate: {turnover_metrics['overall_turnover_rate']:.1f}%")
    print(f"Total hiring forecast: {hiring_forecast['total_hiring_needs']} employees")
    print("\nFiles created in 'reports' folder:")
    print("- hr_analytics_data.csv (Main dataset)")
    print("- hr_metrics.csv (Key metrics)")
    print("- department_metrics.csv (Department analysis)")
    print("- turnover_analysis.csv (Turnover breakdown)")
    print("- recruitment_sources.csv (Recruitment channels)")
    print("- feature_importance.csv (Attrition factors)")
    print("- satisfaction_correlation.csv (Satisfaction drivers)")
    print("- performance_by_department.csv (Performance metrics)")
    print("\nThese files are ready for Power BI import!")

if __name__ == '__main__':
    export_data_for_powerbi()