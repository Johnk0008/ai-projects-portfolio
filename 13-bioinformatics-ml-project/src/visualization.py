import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class DataVisualizer:
    def __init__(self):
        plt.style.use('default')
        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    def plot_model_comparison(self, results):
        """Create model comparison visualization"""
        models = list(results.keys())
        accuracies = [results[model]['accuracy'] for model in models]
        
        plt.figure(figsize=(10, 6))
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Model accuracy comparison
        bars = ax1.bar(models, accuracies, color=self.colors[:len(models)], alpha=0.8)
        ax1.set_ylabel('Accuracy')
        ax1.set_title('Model Performance Comparison')
        ax1.set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, accuracy in zip(bars, accuracies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{accuracy:.3f}', ha='center', va='bottom')
        
        # Feature importance (for Random Forest if available)
        if 'Random Forest' in results:
            rf_model = results['Random Forest']['model']
            if hasattr(rf_model, 'feature_importances_'):
                feature_importance = pd.DataFrame({
                    'feature': range(len(rf_model.feature_importances_)),
                    'importance': rf_model.feature_importances_
                })
                top_features = feature_importance.nlargest(10, 'importance')
                
                ax2.barh(range(len(top_features)), 
                        top_features['importance'], 
                        color=self.colors[0])
                ax2.set_yticks(range(len(top_features)))
                ax2.set_yticklabels([f'Feature {i}' for i in top_features['feature']])
                ax2.set_xlabel('Importance')
                ax2.set_title('Top 10 Feature Importances (Random Forest)')
        
        plt.tight_layout()
        plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_feature_importance(self, model, feature_names):
        """Plot feature importance for tree-based models"""
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=True)
            
            plt.figure(figsize=(10, 8))
            plt.barh(importance_df['feature'][-15:], 
                    importance_df['importance'][-15:], 
                    color=self.colors[0])
            plt.xlabel('Feature Importance')
            plt.title('Top 15 Most Important Features')
            plt.tight_layout()
            plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def plot_sequence_features(self, df):
        """Visualize sequence feature distributions"""
        numeric_features = df.select_dtypes(include=[np.number]).columns
        
        plt.figure(figsize=(15, 10))
        
        # Plot distributions for first 6 features
        for i, feature in enumerate(numeric_features[:6]):
            plt.subplot(2, 3, i + 1)
            sns.histplot(data=df, x=feature, hue='label', alpha=0.7)
            plt.title(f'Distribution of {feature}')
        
        plt.tight_layout()
        plt.savefig('feature_distributions.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_correlation_matrix(self, df):
        """Plot correlation matrix of features"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        plt.figure(figsize=(12, 10))
        correlation_matrix = numeric_df.corr()
        
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, cmap='coolwarm', 
                   center=0, annot=False, square=True)
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()