import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    precision_recall_curve, roc_curve
)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import joblib

class ModelEvaluator:
    def __init__(self):
        self.metrics = {}
        
    def calculate_metrics(self, y_true, y_pred, y_pred_proba=None, model_name='model'):
        """Calculate comprehensive evaluation metrics"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred)
        }
        
        if y_pred_proba is not None:
            metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba[:, 1])
        
        self.metrics[model_name] = metrics
        return metrics
    
    def plot_confusion_matrix(self, y_true, y_pred, model_name='Model'):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Good Credit', 'Bad Credit'],
                   yticklabels=['Good Credit', 'Bad Credit'])
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        plt.show()
        
        return cm
    
    def plot_roc_curve(self, y_true, y_pred_proba, model_name='Model'):
        """Plot ROC curve"""
        fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba[:, 1])
        roc_auc = roc_auc_score(y_true, y_pred_proba[:, 1])
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name}')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.show()
        
        return fpr, tpr, roc_auc
    
    def plot_precision_recall_curve(self, y_true, y_pred_proba, model_name='Model'):
        """Plot Precision-Recall curve"""
        precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba[:, 1])
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Precision-Recall Curve - {model_name}')
        plt.grid(True)
        plt.show()
        
        return precision, recall
    
    def feature_importance_plot(self, model, feature_names, top_n=15):
        """Plot feature importance for tree-based models"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 8))
            plt.title("Feature Importances")
            plt.bar(range(min(top_n, len(importances))), 
                   importances[indices[:top_n]])
            plt.xticks(range(min(top_n, len(importances))), 
                      [feature_names[i] for i in indices[:top_n]], rotation=45)
            plt.tight_layout()
            plt.show()
            
            return importances
        else:
            print("Model doesn't have feature_importances_ attribute")
            return None
    
    def generate_report(self, y_true, y_pred, y_pred_proba=None, model_name='Model'):
        """Generate comprehensive evaluation report"""
        print(f"=== {model_name} Evaluation Report ===")
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred))
        
        metrics = self.calculate_metrics(y_true, y_pred, y_pred_proba, model_name)
        print("\nPerformance Metrics:")
        for metric, value in metrics.items():
            print(f"{metric.capitalize()}: {value:.4f}")
        
        # Plot metrics
        self.plot_confusion_matrix(y_true, y_pred, model_name)
        
        if y_pred_proba is not None:
            self.plot_roc_curve(y_true, y_pred_proba, model_name)
            self.plot_precision_recall_curve(y_true, y_pred_proba, model_name)
        
        return metrics