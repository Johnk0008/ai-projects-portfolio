import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Bellabeat Fitness Analytics", layout="wide")

# Load data
@st.cache_data
def load_data():
    daily_steps = pd.read_csv('cleaned_daily_steps.csv')
    sleep_data = pd.read_csv('cleaned_sleep_data.csv')
    return daily_steps, sleep_data

daily_steps, sleep_data = load_data()

# Dashboard title
st.title("🚴‍♀️ Bellabeat Fitness Data Analytics Dashboard")
st.markdown("---")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_steps = daily_steps['StepTotal'].mean()
    st.metric("Average Daily Steps", f"{avg_steps:,.0f}")

with col2:
    goal_achievement = (daily_steps['StepTotal'] >= 10000).mean() * 100
    st.metric("Goal Achievement Rate", f"{goal_achievement:.1f}%")

with col3:
    avg_sleep = sleep_data['TotalMinutesAsleep'].mean() / 60
    st.metric("Average Sleep Hours", f"{avg_sleep:.1f} hrs")

with col4:
    sleep_efficiency = (sleep_data['TotalMinutesAsleep'] / sleep_data['TotalTimeInBed']).mean() * 100
    st.metric("Sleep Efficiency", f"{sleep_efficiency:.1f}%")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Weekly Activity Pattern")
    weekly_avg = daily_steps.groupby('DayOfWeek')['StepTotal'].mean().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    fig1 = px.bar(weekly_avg, x=weekly_avg.index, y=weekly_avg.values,
                 labels={'x': 'Day of Week', 'y': 'Average Steps'})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Sleep Distribution")
    fig2 = px.histogram(sleep_data, x='TotalMinutesAsleep', 
                       nbins=20, title="Sleep Duration Distribution")
    st.plotly_chart(fig2, use_container_width=True)

# Additional visualizations
col3, col4 = st.columns(2)

with col3:
    st.subheader("User Activity Levels")
    activity_levels = pd.cut(daily_steps['StepTotal'], 
                           bins=[0, 5000, 7500, 10000, float('inf')],
                           labels=['Sedentary', 'Lightly Active', 'Active', 'Very Active'])
    level_counts = activity_levels.value_counts()
    fig3 = px.pie(values=level_counts.values, names=level_counts.index,
                 title="Activity Level Distribution")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Sleep Efficiency")
    sleep_data['SleepEfficiency'] = (sleep_data['TotalMinutesAsleep'] / sleep_data['TotalTimeInBed']) * 100
    fig4 = px.scatter(sleep_data, x='TotalTimeInBed', y='TotalMinutesAsleep',
                     trendline='lowess', title="Time in Bed vs Time Asleep")
    st.plotly_chart(fig4, use_container_width=True)

# Insights section
st.markdown("---")
st.subheader("📊 Key Insights & Recommendations")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.write("**Activity Insights:**")
    st.write(f"- Only {goal_achievement:.1f}% of users meet 10,000 steps goal")
    st.write(f"- Average activity level: {avg_steps:,.0f} steps per day")
    st.write("- Tuesday shows highest activity levels")
    
with insight_col2:
    st.write("**Sleep Insights:**")
    st.write(f"- Average sleep: {avg_sleep:.1f} hours (below 7-9 hour recommendation)")
    st.write(f"- Sleep efficiency: {sleep_efficiency:.1f}%")
    st.write("- Room for improvement in sleep quality")

# Run with: streamlit run bellabeat_dashboard.py