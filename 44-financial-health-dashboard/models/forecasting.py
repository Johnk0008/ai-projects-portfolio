import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class FinancialForecaster:
    def __init__(self, data):
        self.data = data
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data = self.data.sort_values('date')
    
    def prepare_features(self):
        """Prepare features for forecasting"""
        df = self.data.copy()
        
        # Create time-based features
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['year'] = df['date'].dt.year
        df['time_index'] = range(len(df))
        
        # Create lag features only if we have enough data
        if len(df) > 1:
            df['revenue_lag_1'] = df['revenue'].shift(1)
        if len(df) > 3:
            df['revenue_lag_3'] = df['revenue'].shift(3)
        if len(df) > 6:
            df['revenue_lag_6'] = df['revenue'].shift(6)
        
        # Rolling statistics
        if len(df) >= 3:
            df['revenue_rolling_mean_3'] = df['revenue'].rolling(window=3, min_periods=1).mean()
            df['revenue_rolling_std_3'] = df['revenue'].rolling(window=3, min_periods=1).std()
        else:
            df['revenue_rolling_mean_3'] = df['revenue'].expanding().mean()
            df['revenue_rolling_std_3'] = df['revenue'].expanding().std()
        
        # Growth rates
        df['revenue_growth'] = df['revenue'].pct_change().fillna(0)
        
        return df
    
    def forecast_revenue(self, periods=12):
        """Forecast revenue using multiple models"""
        df = self.prepare_features()
        
        # Use simpler forecasting for small datasets
        if len(df) < 4:
            return self._simple_forecast(df, 'revenue', periods)
        
        # Select available features
        available_features = ['time_index', 'month', 'quarter', 'year']
        
        # Add available lag features
        for lag in [1, 3, 6]:
            if f'revenue_lag_{lag}' in df.columns:
                available_features.append(f'revenue_lag_{lag}')
        
        # Add rolling features if available
        if 'revenue_rolling_mean_3' in df.columns:
            available_features.extend(['revenue_rolling_mean_3', 'revenue_rolling_std_3'])
        
        if 'revenue_growth' in df.columns:
            available_features.append('revenue_growth')
        
        # Remove any columns with all NaN values
        available_features = [f for f in available_features if f in df.columns and not df[f].isna().all()]
        
        # Prepare training data
        train_data = df.dropna(subset=available_features + ['revenue'])
        
        if len(train_data) < 3:
            return self._simple_forecast(df, 'revenue', periods)
        
        X = train_data[available_features]
        y = train_data['revenue']
        
        # Train models
        lr_model = LinearRegression()
        rf_model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=5)
        
        try:
            lr_model.fit(X, y)
            rf_model.fit(X, y)
        except Exception as e:
            print(f"Model training failed: {e}")
            return self._simple_forecast(df, 'revenue', periods)
        
        # Generate future dates
        last_date = df['date'].iloc[-1]
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=periods,
            freq='M'
        )
        
        # Create future features
        future_data = []
        current_values = df.iloc[-1].copy()
        
        for i, date in enumerate(future_dates):
            future_row = {
                'date': date,
                'time_index': len(df) + i,
                'month': date.month,
                'quarter': date.quarter,
                'year': date.year
            }
            
            # Initialize with current values
            for feature in available_features:
                if feature not in future_row:
                    future_row[feature] = current_values.get(feature, 0)
            
            future_data.append(future_row)
            
            # Update current values for next iteration (simplified)
            if i == 0:
                # For the first forecast, use the last known values
                current_values = future_row.copy()
        
        future_df = pd.DataFrame(future_data)
        
        # Ensure all required features are present
        for feature in available_features:
            if feature not in future_df.columns:
                future_df[feature] = 0
        
        # Make predictions
        try:
            future_X = future_df[available_features]
            future_df['revenue_forecast_lr'] = lr_model.predict(future_X)
            future_df['revenue_forecast_rf'] = rf_model.predict(future_X)
            future_df['revenue_forecast'] = (future_df['revenue_forecast_lr'] + future_df['revenue_forecast_rf']) / 2
        except Exception as e:
            print(f"Prediction failed: {e}")
            # Fallback to simple forecast
            simple_forecast = self._simple_forecast(df, 'revenue', periods)
            return simple_forecast
        
        return future_df[['date', 'revenue_forecast', 'revenue_forecast_lr', 'revenue_forecast_rf']]
    
    def _simple_forecast(self, df, column, periods):
        """Simple forecasting method for small datasets or when complex models fail"""
        last_value = df[column].iloc[-1]
        
        # Calculate growth rate from available data
        if len(df) > 1:
            growth_rate = df[column].pct_change().mean()
            if pd.isna(growth_rate) or abs(growth_rate) > 1:  # Sanity check
                growth_rate = 0.02  # Default 2% growth
        else:
            growth_rate = 0.02  # Default 2% growth
        
        future_dates = pd.date_range(
            start=df['date'].iloc[-1] + pd.DateOffset(months=1),
            periods=periods,
            freq='M'
        )
        
        forecasts = []
        current_value = last_value
        
        for date in future_dates:
            current_value = current_value * (1 + growth_rate)
            forecasts.append({
                'date': date,
                f'{column}_forecast': current_value,
                f'{column}_forecast_lr': current_value,
                f'{column}_forecast_rf': current_value
            })
        
        return pd.DataFrame(forecasts)
    
    def forecast_income_statement(self, periods=12):
        """Forecast complete income statement"""
        revenue_forecast = self.forecast_revenue(periods)
        
        # Use historical ratios to forecast other items
        historical_data = self.data
        
        # Calculate average ratios from historical data
        revenue_mean = historical_data['revenue'].mean()
        
        if revenue_mean > 0:
            historical_ratios = {
                'cogs_ratio': historical_data['cogs'].mean() / revenue_mean,
                'operating_expenses_ratio': historical_data['operating_expenses'].mean() / revenue_mean,
                'salaries_ratio': historical_data['salaries'].mean() / revenue_mean,
                'marketing_ratio': historical_data['marketing'].mean() / revenue_mean,
                'other_expenses_ratio': historical_data['other_expenses'].mean() / revenue_mean
            }
        else:
            # Default ratios if no historical data
            historical_ratios = {
                'cogs_ratio': 0.4,
                'operating_expenses_ratio': 0.25,
                'salaries_ratio': 0.15,
                'marketing_ratio': 0.05,
                'other_expenses_ratio': 0.03
            }
        
        forecast_df = revenue_forecast.copy()
        
        # Rename revenue column for consistency
        if 'revenue_forecast' in forecast_df.columns:
            forecast_df['revenue'] = forecast_df['revenue_forecast']
        elif 'revenue_forecast_lr' in forecast_df.columns:
            forecast_df['revenue'] = forecast_df['revenue_forecast_lr']
        else:
            # Fallback if no revenue forecast available
            last_revenue = historical_data['revenue'].iloc[-1] if len(historical_data) > 0 else 50000
            forecast_df['revenue'] = [last_revenue * (1.02 ** i) for i in range(1, periods + 1)]
        
        # Calculate other financial statement items
        forecast_df['cogs'] = forecast_df['revenue'] * historical_ratios['cogs_ratio']
        forecast_df['gross_profit'] = forecast_df['revenue'] - forecast_df['cogs']
        forecast_df['operating_expenses'] = forecast_df['revenue'] * historical_ratios['operating_expenses_ratio']
        forecast_df['salaries'] = forecast_df['revenue'] * historical_ratios['salaries_ratio']
        forecast_df['marketing'] = forecast_df['revenue'] * historical_ratios['marketing_ratio']
        forecast_df['other_expenses'] = forecast_df['revenue'] * historical_ratios['other_expenses_ratio']
        
        forecast_df['operating_income'] = (
            forecast_df['gross_profit'] - 
            forecast_df['operating_expenses'] - 
            forecast_df['salaries'] - 
            forecast_df['marketing']
        )
        
        forecast_df['net_income'] = forecast_df['operating_income'] - forecast_df['other_expenses']
        
        return forecast_df