import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import io
import base64

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_matplotlib_dashboard():
    # Load data
    daily_steps = pd.read_csv('cleaned_daily_steps.csv')
    sleep_data = pd.read_csv('cleaned_sleep_data.csv')
    
    # Convert date columns
    daily_steps['ActivityDay'] = pd.to_datetime(daily_steps['ActivityDay'])
    sleep_data['SleepDay'] = pd.to_datetime(sleep_data['SleepDay'])
    
    # Create the dashboard figure
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Bellabeat Fitness Analytics Dashboard', fontsize=16, fontweight='bold')
    
    # Plot 1: Weekly Activity Pattern
    daily_steps['DayOfWeek'] = daily_steps['ActivityDay'].dt.day_name()
    weekly_avg = daily_steps.groupby('DayOfWeek')['StepTotal'].mean().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    
    axes[0,0].bar(weekly_avg.index, weekly_avg.values, color='skyblue', edgecolor='black', alpha=0.7)
    axes[0,0].axhline(10000, color='red', linestyle='--', label='10K Steps Goal')
    axes[0,0].set_title('Average Steps by Day of Week')
    axes[0,0].set_ylabel('Average Steps')
    axes[0,0].tick_params(axis='x', rotation=45)
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # Plot 2: Sleep Distribution
    sleep_hours = sleep_data['TotalMinutesAsleep'] / 60
    axes[0,1].hist(sleep_hours, bins=15, color='lightgreen', edgecolor='black', alpha=0.7)
    axes[0,1].axvline(7, color='red', linestyle='--', label='Recommended 7 hrs')
    axes[0,1].set_title('Sleep Duration Distribution')
    axes[0,1].set_xlabel('Sleep Hours')
    axes[0,1].set_ylabel('Frequency')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # Plot 3: Activity Levels
    activity_levels = pd.cut(daily_steps['StepTotal'], 
                           bins=[0, 5000, 7500, 10000, float('inf')],
                           labels=['Sedentary', 'Lightly Active', 'Active', 'Very Active'])
    level_counts = activity_levels.value_counts()
    
    colors = ['lightcoral', 'lightyellow', 'lightgreen', 'lightblue']
    axes[1,0].pie(level_counts.values, labels=level_counts.index, autopct='%1.1f%%', 
                 colors=colors, startangle=90)
    axes[1,0].set_title('User Activity Levels Distribution')
    
    # Plot 4: Sleep Efficiency
    sleep_data['SleepEfficiency'] = (sleep_data['TotalMinutesAsleep'] / sleep_data['TotalTimeInBed']) * 100
    axes[1,1].scatter(sleep_data['TotalTimeInBed'], sleep_data['TotalMinutesAsleep'], 
                     alpha=0.6, color='purple')
    axes[1,1].plot([0, 1000], [0, 1000], 'r--', alpha=0.8, label='Perfect Efficiency')
    axes[1,1].set_xlabel('Time in Bed (minutes)')
    axes[1,1].set_ylabel('Time Asleep (minutes)')
    axes[1,1].set_title('Sleep Efficiency: Time in Bed vs Time Asleep')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def generate_insights_report():
    # Load data
    daily_steps = pd.read_csv('cleaned_daily_steps.csv')
    sleep_data = pd.read_csv('cleaned_sleep_data.csv')
    
    # Calculate key metrics
    avg_steps = daily_steps['StepTotal'].mean()
    goal_achievement = (daily_steps['StepTotal'] >= 10000).mean() * 100
    avg_sleep = sleep_data['TotalMinutesAsleep'].mean() / 60
    sleep_efficiency = (sleep_data['TotalMinutesAsleep'] / sleep_data['TotalTimeInBed']).mean() * 100
    
    insights = f"""
    BELLABEAT FITNESS ANALYTICS - KEY INSIGHTS
    ==========================================
    
    KEY METRICS:
    • Average Daily Steps: {avg_steps:,.0f}
    • Users Meeting 10K Steps Goal: {goal_achievement:.1f}%
    • Average Sleep Duration: {avg_sleep:.1f} hours
    • Average Sleep Efficiency: {sleep_efficiency:.1f}%
    
    CRITICAL INSIGHTS:
    1. ACTIVITY LEVELS:
       - Only {goal_achievement:.1f}% of users meet recommended 10,000 daily steps
       - Average activity ({avg_steps:.0f} steps) is below optimal health levels
    
    2. SLEEP PATTERNS:
       - Users average {avg_sleep:.1f} hours of sleep (below 7-9 hour recommendation)
       - Sleep efficiency of {sleep_efficiency:.1f}% indicates room for improvement
    
    STRATEGIC RECOMMENDATIONS:
    1. Implement smart notifications for sedentary behavior detection
    2. Develop personalized step goals based on user history
    3. Add sleep quality scoring and improvement suggestions
    4. Create educational content on sleep optimization
    """
    
    return insights

# Generate and save dashboard
if __name__ == "__main__":
    print("Generating Bellabeat Fitness Dashboard...")
    
    # Create visualization
    dashboard_fig = create_matplotlib_dashboard()
    plt.savefig('bellabeat_dashboard.png', dpi=300, bbox_inches='tight')
    print("✅ Dashboard visualization saved as 'bellabeat_dashboard.png'")
    
    # Generate insights report
    insights = generate_insights_report()
    with open('bellabeat_insights_report.txt', 'w') as f:
        f.write(insights)
    print("✅ Insights report saved as 'bellabeat_insights_report.txt'")
    
    # Print insights to console
    print("\n" + "="*50)
    print(insights)
    print("="*50)
    
    print("\n🎯 Dashboard generation complete!")
    print("📊 Check the generated files:")
    print("   - bellabeat_dashboard.png")
    print("   - bellabeat_insights_report.txt")