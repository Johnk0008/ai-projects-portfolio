# app.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class UnemploymentAnalysis:
    def __init__(self, file1, file2):
        """
        Initialize the analysis with two datasets
        """
        try:
            # Try reading with different encodings
            self.df1 = pd.read_csv(file1, encoding='utf-8')
        except:
            try:
                self.df1 = pd.read_csv(file1, encoding='latin-1')
            except:
                self.df1 = pd.read_csv(file1, encoding='cp1252')
        
        try:
            self.df2 = pd.read_csv(file2, encoding='utf-8')
        except:
            try:
                self.df2 = pd.read_csv(file2, encoding='latin-1')
            except:
                self.df2 = pd.read_csv(file2, encoding='cp1252')
                
        self.combined_df = None
        
    def data_cleaning(self):
        """
        Clean and preprocess the data with robust error handling
        """
        print("Step 1: Data Cleaning and Preprocessing")
        print("=" * 50)
        
        # Display initial data info
        print("Initial Dataset 1 Info:")
        print(f"Shape: {self.df1.shape}")
        print(f"Columns: {list(self.df1.columns)}")
        print(f"First few Date values: {self.df1.iloc[:, 1].head().tolist() if len(self.df1.columns) > 1 else 'No Date column'}")
        
        print("\nInitial Dataset 2 Info:")
        print(f"Shape: {self.df2.shape}")
        print(f"Columns: {list(self.df2.columns)}")
        print(f"First few Date values: {self.df2['Date'].head().tolist() if 'Date' in self.df2.columns else 'No Date column'}")
        
        # Clean first dataset - handle spaces in column names
        self.df1 = self.df1.dropna(how='all')
        
        # Standardize column names - strip whitespace and handle specific column names
        self.df1.columns = self.df1.columns.str.strip()
        self.df2.columns = self.df2.columns.str.strip()
        
        # For df1, check if columns have spaces and rename them properly
        print("\nRenaming columns for Dataset 1...")
        column_mapping = {}
        for col in self.df1.columns:
            cleaned_col = col.strip()
            if 'Date' in cleaned_col:
                column_mapping[col] = 'Date'
            elif 'Region' in cleaned_col:
                column_mapping[col] = 'Region'
            elif 'Estimated Unemployment Rate' in cleaned_col:
                column_mapping[col] = 'Estimated Unemployment Rate (%)'
            elif 'Estimated Employed' in cleaned_col:
                column_mapping[col] = 'Estimated Employed'
            elif 'Estimated Labour Participation Rate' in cleaned_col:
                column_mapping[col] = 'Estimated Labour Participation Rate (%)'
            elif 'Frequency' in cleaned_col:
                column_mapping[col] = 'Frequency'
            elif 'Area' in cleaned_col:
                column_mapping[col] = 'Area'
        
        # Apply the mapping
        self.df1 = self.df1.rename(columns=column_mapping)
        print(f"Renamed columns in Dataset 1: {list(self.df1.columns)}")
        
        # Remove rows where Region is NaN
        if 'Region' in self.df1.columns:
            self.df1 = self.df1[self.df1['Region'].notna()]
        
        # Clean second dataset
        self.df2 = self.df2.dropna(how='all')
        
        # Clean date columns - handle leading/trailing spaces
        print("\nCleaning date columns...")
        
        # Function to clean and convert dates
        def clean_date_column(df, date_col='Date'):
            if date_col not in df.columns:
                print(f"Warning: {date_col} column not found in dataframe")
                return df
                
            # Strip whitespace from date strings
            df[date_col] = df[date_col].astype(str).str.strip()
            
            # Try multiple date formats
            for fmt in ['%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y']:
                try:
                    converted_dates = pd.to_datetime(df[date_col], format=fmt, errors='coerce')
                    if not converted_dates.isna().all():
                        df[date_col] = converted_dates
                        print(f"Successfully converted dates using format: {fmt}")
                        break
                except Exception as e:
                    continue
            else:
                # If no format works, use pandas automatic detection
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                print("Used automatic date conversion with coerce")
            
            return df
        
        # Apply date cleaning to both datasets
        if 'Date' in self.df1.columns:
            self.df1 = clean_date_column(self.df1, 'Date')
        if 'Date' in self.df2.columns:
            self.df2 = clean_date_column(self.df2, 'Date')
        
        # Handle numeric columns with robust conversion
        numeric_cols = ['Estimated Unemployment Rate (%)', 'Estimated Employed', 
                       'Estimated Labour Participation Rate (%)']
        
        for col in numeric_cols:
            if col in self.df1.columns:
                # Clean numeric strings - remove commas, spaces, etc.
                self.df1[col] = self.df1[col].astype(str).str.replace(',', '').str.strip()
                self.df1[col] = pd.to_numeric(self.df1[col], errors='coerce')
            
            if col in self.df2.columns:
                self.df2[col] = self.df2[col].astype(str).str.replace(',', '').str.strip()
                self.df2[col] = pd.to_numeric(self.df2[col], errors='coerce')
        
        # Clean region names
        if 'Region' in self.df1.columns:
            self.df1['Region'] = self.df1['Region'].astype(str).str.strip()
        if 'Region' in self.df2.columns:
            self.df2['Region'] = self.df2['Region'].astype(str).str.strip()
        
        # Remove duplicates
        self.df1 = self.df1.drop_duplicates()
        self.df2 = self.df2.drop_duplicates()
        
        print(f"\nAfter cleaning:")
        print(f"Dataset 1 shape: {self.df1.shape}")
        print(f"Dataset 2 shape: {self.df2.shape}")
        
        if 'Date' in self.df1.columns:
            print(f"Dataset 1 date range: {self.df1['Date'].min()} to {self.df1['Date'].max()}")
        if 'Date' in self.df2.columns:
            print(f"Dataset 2 date range: {self.df2['Date'].min()} to {self.df2['Date'].max()}")
        
        print("\nMissing values in Dataset 1:")
        print(self.df1.isnull().sum())
        print("\nMissing values in Dataset 2:")
        print(self.df2.isnull().sum())
        
    def explore_data(self):
        """
        Explore the datasets and combine them
        """
        print("\nStep 2: Data Exploration")
        print("=" * 50)
        
        # Basic statistics
        print("Basic Statistics - Dataset 1:")
        numeric_cols_df1 = ['Estimated Unemployment Rate (%)', 'Estimated Employed', 
                           'Estimated Labour Participation Rate (%)']
        numeric_cols_df1 = [col for col in numeric_cols_df1 if col in self.df1.columns]
        if numeric_cols_df1:
            print(self.df1[numeric_cols_df1].describe())
        else:
            print("No numeric columns found in Dataset 1")
        
        print("\nBasic Statistics - Dataset 2:")
        numeric_cols_df2 = ['Estimated Unemployment Rate (%)', 'Estimated Employed', 
                           'Estimated Labour Participation Rate (%)']
        numeric_cols_df2 = [col for col in numeric_cols_df2 if col in self.df2.columns]
        if numeric_cols_df2:
            print(self.df2[numeric_cols_df2].describe())
        else:
            print("No numeric columns found in Dataset 2")
        
        # Find common columns for combination
        common_cols = []
        for col in ['Region', 'Date', 'Estimated Unemployment Rate (%)',
                   'Estimated Employed', 'Estimated Labour Participation Rate (%)']:
            if col in self.df1.columns and col in self.df2.columns:
                common_cols.append(col)
        
        print(f"\nCommon columns for combination: {common_cols}")
        
        if common_cols:
            df1_common = self.df1[common_cols].copy()
            df2_common = self.df2[common_cols].copy()
            
            self.combined_df = pd.concat([df1_common, df2_common], ignore_index=True)
            self.combined_df = self.combined_df.drop_duplicates()
            
            # Add month and year columns for time series analysis
            self.combined_df['Month'] = self.combined_df['Date'].dt.month
            self.combined_df['Year'] = self.combined_df['Date'].dt.year
            self.combined_df['Month_Year'] = self.combined_df['Date'].dt.to_period('M')
            
            print(f"\nCombined dataset shape: {self.combined_df.shape}")
            print(f"Date range: {self.combined_df['Date'].min()} to {self.combined_df['Date'].max()}")
        else:
            print("No common columns found for combination. Using Dataset 2 as primary.")
            self.combined_df = self.df2.copy()
            if 'Date' in self.combined_df.columns:
                self.combined_df['Month'] = self.combined_df['Date'].dt.month
                self.combined_df['Year'] = self.combined_df['Date'].dt.year
                self.combined_df['Month_Year'] = self.combined_df['Date'].dt.to_period('M')
        
    def analyze_covid_impact(self):
        """
        Analyze the impact of COVID-19 on unemployment
        """
        print("\nStep 3: COVID-19 Impact Analysis")
        print("=" * 50)
        
        if self.combined_df is None or self.combined_df.empty:
            print("No data available for analysis")
            return None, None, None
        
        # Define pre-COVID and COVID periods
        pre_covid = self.combined_df[self.combined_df['Date'] < '2020-03-01']
        covid_period = self.combined_df[self.combined_df['Date'] >= '2020-03-01']
        
        print(f"Pre-COVID records: {len(pre_covid)}")
        print(f"COVID period records: {len(covid_period)}")
        
        if len(pre_covid) == 0 or len(covid_period) == 0:
            print("Insufficient data for COVID impact analysis")
            return pre_covid, covid_period, None
        
        # Calculate average unemployment rates
        pre_covid_avg = pre_covid['Estimated Unemployment Rate (%)'].mean()
        covid_avg = covid_period['Estimated Unemployment Rate (%)'].mean()
        
        print(f"\nAverage Unemployment Rate:")
        print(f"Pre-COVID (Before Mar 2020): {pre_covid_avg:.2f}%")
        print(f"During COVID (Mar 2020 onwards): {covid_avg:.2f}%")
        print(f"Change: {((covid_avg - pre_covid_avg) / pre_covid_avg * 100):.2f}%")
        
        # Analyze by region
        try:
            # Create period labels
            conditions = [
                self.combined_df['Date'] < pd.Timestamp('2020-03-01'),
                self.combined_df['Date'] >= pd.Timestamp('2020-03-01')
            ]
            choices = ['Pre-COVID', 'COVID']
            
            self.combined_df['Period'] = np.select(conditions, choices, default='Unknown')
            
            region_impact = self.combined_df.groupby(['Region', 'Period'])['Estimated Unemployment Rate (%)'].mean().unstack()
            
            if 'COVID' in region_impact.columns and 'Pre-COVID' in region_impact.columns:
                region_impact['Change'] = region_impact['COVID'] - region_impact['Pre-COVID']
                region_impact['Change_Percent'] = (region_impact['Change'] / region_impact['Pre-COVID']) * 100
                
                print("\nTop 10 regions most affected by COVID-19:")
                print(region_impact.nlargest(10, 'Change_Percent')[['Pre-COVID', 'COVID', 'Change_Percent']])
            else:
                print("Insufficient data for regional COVID impact analysis")
                region_impact = None
                
        except Exception as e:
            print(f"Error in regional COVID analysis: {e}")
            region_impact = None
        
        return pre_covid, covid_period, region_impact
    
    def seasonal_trends_analysis(self):
        """
        Identify seasonal patterns and trends
        """
        print("\nStep 4: Seasonal Trends Analysis")
        print("=" * 50)
        
        if self.combined_df is None or self.combined_df.empty:
            print("No data available for seasonal analysis")
            return None, None, None
        
        # Monthly trends
        monthly_trends = self.combined_df.groupby('Month_Year')['Estimated Unemployment Rate (%)'].mean().reset_index()
        monthly_trends['Month_Year'] = monthly_trends['Month_Year'].astype(str)
        
        # Seasonal patterns by month
        seasonal_pattern = self.combined_df.groupby('Month')['Estimated Unemployment Rate (%)'].mean()
        
        print("Seasonal Pattern by Month:")
        for month, rate in seasonal_pattern.items():
            print(f"Month {month}: {rate:.2f}%")
        
        # Year-over-year comparison
        yearly_comparison = self.combined_df.groupby('Year')['Estimated Unemployment Rate (%)'].mean()
        print(f"\nYearly Average Unemployment Rates:")
        for year, rate in yearly_comparison.items():
            print(f"{year}: {rate:.2f}%")
            
        return monthly_trends, seasonal_pattern, yearly_comparison
    
    def regional_analysis(self):
        """
        Analyze regional variations in unemployment
        """
        print("\nStep 5: Regional Analysis")
        print("=" * 50)
        
        if self.combined_df is None or self.combined_df.empty:
            print("No data available for regional analysis")
            return None
        
        regional_stats = self.combined_df.groupby('Region').agg({
            'Estimated Unemployment Rate (%)': ['mean', 'std', 'max', 'min'],
            'Estimated Employed': 'mean',
            'Estimated Labour Participation Rate (%)': 'mean'
        }).round(2)
        
        regional_stats.columns = ['_'.join(col).strip() for col in regional_stats.columns.values]
        regional_stats = regional_stats.sort_values('Estimated Unemployment Rate (%)_mean', ascending=False)
        
        print("Top 10 regions with highest average unemployment:")
        print(regional_stats.head(10)[['Estimated Unemployment Rate (%)_mean', 
                                    'Estimated Unemployment Rate (%)_std']])
        
        print("\nTop 10 regions with lowest average unemployment:")
        print(regional_stats.tail(10)[['Estimated Unemployment Rate (%)_mean', 
                                    'Estimated Unemployment Rate (%)_std']])
        
        return regional_stats
    
    def create_visualizations(self, pre_covid, covid_period, monthly_trends, regional_stats):
        """
        Create comprehensive visualizations
        """
        print("\nStep 6: Creating Visualizations")
        print("=" * 50)
        
        if self.combined_df is None or self.combined_df.empty:
            print("No data available for visualizations")
            return
        
        # Set up the plotting style
        plt.rcParams['figure.figsize'] = (15, 12)
        
        # Create subplots
        fig, axes = plt.subplots(3, 2, figsize=(20, 18))
        fig.suptitle('Unemployment Analysis in India: Comprehensive Overview', 
                    fontsize=16, fontweight='bold', y=0.95)
        
        # 1. Time series of unemployment rate
        try:
            monthly_avg = self.combined_df.groupby('Month_Year')['Estimated Unemployment Rate (%)'].mean()
            axes[0,0].plot(monthly_avg.index.astype(str), monthly_avg.values, 
                          marker='o', linewidth=2, markersize=4)
            axes[0,0].axvline(x='2020-03', color='red', linestyle='--', alpha=0.7, 
                             label='COVID-19 Start')
            axes[0,0].set_title('Monthly Average Unemployment Rate Over Time', fontweight='bold')
            axes[0,0].set_xlabel('Month-Year')
            axes[0,0].set_ylabel('Unemployment Rate (%)')
            axes[0,0].tick_params(axis='x', rotation=45)
            axes[0,0].legend()
            axes[0,0].grid(True, alpha=0.3)
        except Exception as e:
            axes[0,0].text(0.5, 0.5, 'Time series data\nnot available', 
                          ha='center', va='center', transform=axes[0,0].transAxes)
            axes[0,0].set_title('Monthly Average Unemployment Rate Over Time', fontweight='bold')
        
        # 2. Pre-COVID vs COVID comparison
        try:
            if pre_covid is not None and covid_period is not None:
                periods = ['Pre-COVID', 'COVID Period']
                rates = [pre_covid['Estimated Unemployment Rate (%)'].mean(), 
                        covid_period['Estimated Unemployment Rate (%)'].mean()]
                
                bars = axes[0,1].bar(periods, rates, color=['skyblue', 'lightcoral'], alpha=0.8)
                axes[0,1].set_title('Average Unemployment Rate: Pre-COVID vs COVID Period', 
                                   fontweight='bold')
                axes[0,1].set_ylabel('Unemployment Rate (%)')
                
                # Add value labels on bars
                for bar, rate in zip(bars, rates):
                    height = bar.get_height()
                    axes[0,1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                                  f'{rate:.2f}%', ha='center', va='bottom', fontweight='bold')
            else:
                axes[0,1].text(0.5, 0.5, 'COVID comparison data\nnot available', 
                              ha='center', va='center', transform=axes[0,1].transAxes)
                axes[0,1].set_title('Average Unemployment Rate: Pre-COVID vs COVID Period', 
                                   fontweight='bold')
        except:
            axes[0,1].text(0.5, 0.5, 'COVID comparison data\nnot available', 
                          ha='center', va='center', transform=axes[0,1].transAxes)
            axes[0,1].set_title('Average Unemployment Rate: Pre-COVID vs COVID Period', 
                               fontweight='bold')
        
        # 3. Top regions with highest unemployment
        try:
            if regional_stats is not None:
                top_regions = regional_stats.head(10)
                axes[1,0].barh(range(len(top_regions)), 
                              top_regions['Estimated Unemployment Rate (%)_mean'],
                              color='lightcoral', alpha=0.8)
                axes[1,0].set_yticks(range(len(top_regions)))
                axes[1,0].set_yticklabels(top_regions.index)
                axes[1,0].set_title('Top 10 Regions with Highest Average Unemployment Rate', 
                                   fontweight='bold')
                axes[1,0].set_xlabel('Average Unemployment Rate (%)')
            else:
                axes[1,0].text(0.5, 0.5, 'Regional data\nnot available', 
                              ha='center', va='center', transform=axes[1,0].transAxes)
                axes[1,0].set_title('Top 10 Regions with Highest Average Unemployment Rate', 
                                   fontweight='bold')
        except:
            axes[1,0].text(0.5, 0.5, 'Regional data\nnot available', 
                          ha='center', va='center', transform=axes[1,0].transAxes)
            axes[1,0].set_title('Top 10 Regions with Highest Average Unemployment Rate', 
                               fontweight='bold')
        
        # 4. Seasonal pattern by month
        try:
            seasonal_pattern = self.combined_df.groupby('Month')['Estimated Unemployment Rate (%)'].mean()
            axes[1,1].plot(seasonal_pattern.index, seasonal_pattern.values, 
                          marker='o', linewidth=2, markersize=6, color='green')
            axes[1,1].set_title('Seasonal Pattern of Unemployment (Monthly Average)', 
                               fontweight='bold')
            axes[1,1].set_xlabel('Month')
            axes[1,1].set_ylabel('Unemployment Rate (%)')
            axes[1,1].set_xticks(range(1, 13))
            axes[1,1].grid(True, alpha=0.3)
        except:
            axes[1,1].text(0.5, 0.5, 'Seasonal data\nnot available', 
                          ha='center', va='center', transform=axes[1,1].transAxes)
            axes[1,1].set_title('Seasonal Pattern of Unemployment (Monthly Average)', 
                               fontweight='bold')
        
        # 5. Distribution of unemployment rates
        try:
            axes[2,0].hist(self.combined_df['Estimated Unemployment Rate (%)'], 
                          bins=30, alpha=0.7, color='lightblue', edgecolor='black')
            axes[2,0].axvline(self.combined_df['Estimated Unemployment Rate (%)'].mean(), 
                             color='red', linestyle='--', 
                             label=f'Mean: {self.combined_df["Estimated Unemployment Rate (%)"].mean():.2f}%')
            axes[2,0].set_title('Distribution of Unemployment Rates', fontweight='bold')
            axes[2,0].set_xlabel('Unemployment Rate (%)')
            axes[2,0].set_ylabel('Frequency')
            axes[2,0].legend()
        except:
            axes[2,0].text(0.5, 0.5, 'Distribution data\nnot available', 
                          ha='center', va='center', transform=axes[2,0].transAxes)
            axes[2,0].set_title('Distribution of Unemployment Rates', fontweight='bold')
        
        # 6. Employment vs Unemployment correlation
        try:
            if 'Estimated Employed' in self.combined_df.columns:
                axes[2,1].scatter(self.combined_df['Estimated Employed'] / 1000000, 
                                 self.combined_df['Estimated Unemployment Rate (%)'],
                                 alpha=0.6, color='purple')
                axes[2,1].set_title('Employment vs Unemployment Rate', fontweight='bold')
                axes[2,1].set_xlabel('Estimated Employed (Millions)')
                axes[2,1].set_ylabel('Unemployment Rate (%)')
                axes[2,1].grid(True, alpha=0.3)
            else:
                axes[2,1].text(0.5, 0.5, 'Employment data\nnot available', 
                              ha='center', va='center', transform=axes[2,1].transAxes)
                axes[2,1].set_title('Employment vs Unemployment Rate', fontweight='bold')
        except:
            axes[2,1].text(0.5, 0.5, 'Employment data\nnot available', 
                          ha='center', va='center', transform=axes[2,1].transAxes)
            axes[2,1].set_title('Employment vs Unemployment Rate', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('unemployment_analysis_comprehensive.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Create interactive plot with Plotly
        try:
            self.create_interactive_visualizations(monthly_trends, regional_stats)
        except Exception as e:
            print(f"Interactive visualizations failed: {e}")
    
    def create_interactive_visualizations(self, monthly_trends, regional_stats):
        """
        Create interactive visualizations using Plotly
        """
        if monthly_trends is not None and not monthly_trends.empty:
            # Interactive time series
            fig1 = px.line(monthly_trends, x='Month_Year', y='Estimated Unemployment Rate (%)',
                          title='Interactive: Monthly Unemployment Rate Trend',
                          markers=True)
            fig1.add_vline(x='2020-03', line_dash="dash", line_color="red",
                          annotation_text="COVID-19 Start")
            fig1.show()
        
        if regional_stats is not None and not regional_stats.empty:
            # Regional heatmap (top 20 regions)
            top_20_regions = regional_stats.head(20)
            fig2 = px.bar(top_20_regions.reset_index(), 
                         x='Estimated Unemployment Rate (%)_mean', 
                         y='Region',
                         orientation='h',
                         title='Top 20 Regions with Highest Unemployment Rates',
                         color='Estimated Unemployment Rate (%)_mean',
                         color_continuous_scale='Reds')
            fig2.show()
    
    def generate_policy_insights(self, region_impact, regional_stats):
        """
        Generate insights for economic and social policies
        """
        print("\nStep 7: Policy Insights and Recommendations")
        print("=" * 50)
        
        if self.combined_df is None or self.combined_df.empty:
            print("No data available for policy insights")
            return
        
        # Key findings
        avg_unemployment = self.combined_df['Estimated Unemployment Rate (%)'].mean()
        max_unemployment = self.combined_df['Estimated Unemployment Rate (%)'].max()
        
        if regional_stats is not None and not regional_stats.empty:
            most_affected_region = regional_stats.index[0]
        else:
            most_affected_region = "Unknown"
        
        print("KEY FINDINGS:")
        print(f"• National average unemployment rate: {avg_unemployment:.2f}%")
        print(f"• Peak unemployment rate observed: {max_unemployment:.2f}%")
        print(f"• Most affected region: {most_affected_region}")
        
        # COVID-19 impact insights
        if region_impact is not None and not region_impact.empty:
            covid_impact_regions = region_impact.nlargest(5, 'Change_Percent')
            print(f"\nTOP 5 REGIONS MOST IMPACTED BY COVID-19:")
            for region in covid_impact_regions.index:
                change = covid_impact_regions.loc[region, 'Change_Percent']
                print(f"• {region}: {change:.1f}% increase")
        else:
            print(f"\nCOVID-19 impact analysis not available")
        
        # Policy recommendations
        print("\nPOLICY RECOMMENDATIONS:")
        print("1. TARGETED REGIONAL SUPPORT:")
        print("   • Focus on regions with highest unemployment rates and COVID impact")
        print("   • Implement region-specific employment generation programs")
        
        print("\n2. SKILL DEVELOPMENT INITIATIVES:")
        print("   • Enhance vocational training in high-unemployment regions")
        print("   • Promote digital skills for post-COVID economy")
        
        print("\n3. ECONOMIC STIMULUS MEASURES:")
        print("   • Support MSMEs in most affected regions")
        print("   • Create public works programs in high-unemployment areas")
        
        print("\n4. SOCIAL SAFETY NETS:")
        print("   • Strengthen unemployment benefits system")
        print("   • Expand healthcare coverage for informal workers")
        
        print("\n5. LONG-TERM STRATEGIES:")
        print("   • Diversify economic activities across regions")
        print("   • Invest in infrastructure development")
        print("   • Promote entrepreneurship and innovation")
    
    def run_complete_analysis(self):
        """
        Run the complete unemployment analysis pipeline
        """
        print("UNEMPLOYMENT ANALYSIS IN INDIA")
        print("=" * 60)
        
        try:
            # Execute all analysis steps
            self.data_cleaning()
            self.explore_data()
            pre_covid, covid_period, region_impact = self.analyze_covid_impact()
            monthly_trends, seasonal_pattern, yearly_comparison = self.seasonal_trends_analysis()
            regional_stats = self.regional_analysis()
            self.create_visualizations(pre_covid, covid_period, monthly_trends, regional_stats)
            self.generate_policy_insights(region_impact, regional_stats)
            
            print("\n" + "=" * 60)
            print("ANALYSIS COMPLETED SUCCESSFULLY!")
            print("Check generated visualizations and insights above.")
            
        except Exception as e:
            print(f"\nError during analysis: {e}")
            print("Attempting to continue with available data...")
            
            # Try to run basic analysis even if some parts fail
            try:
                if self.combined_df is not None:
                    print(f"\nBasic analysis on available data:")
                    print(f"Total records: {len(self.combined_df)}")
                    print(f"Average unemployment rate: {self.combined_df['Estimated Unemployment Rate (%)'].mean():.2f}%")
                    print(f"Date range: {self.combined_df['Date'].min()} to {self.combined_df['Date'].max()}")
            except:
                print("Limited analysis completed with errors.")

# Main execution
if __name__ == "__main__":
    try:
        # Initialize the analysis
        analyzer = UnemploymentAnalysis('data/Unemployment_in_India.csv', 'data/Unemployment_Rate_upto_11_2020.csv')
        
        # Run complete analysis
        analyzer.run_complete_analysis()
        
    except Exception as e:
        print(f"Main analysis failed: {e}")