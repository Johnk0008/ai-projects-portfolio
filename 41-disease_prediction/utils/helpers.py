import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc

class Visualization:
    def __init__(self):
        plt.style.use('default')
    
    def plot_confusion_matrix(self, y_true, y_pred, model_name):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        plt.show()
    
    def plot_roc_curve(self, y_true, y_pred_proba, model_name):
        """Plot ROC curve"""
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba[:, 1])
        roc_auc = auc(fpr, tpr)
        
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
    
    def plot_feature_importance(self, model, feature_names, model_name):
        """Plot feature importance for tree-based models"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 6))
            plt.title(f'Feature Importance - {model_name}')
            plt.bar(range(len(importances)), importances[indices])
            plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
            plt.tight_layout()
            plt.show()

def evaluate_model(results, X_test, y_test, feature_names=None):
    """Comprehensive model evaluation"""
    viz = Visualization()
    
    for model_name, result in results.items():
        print(f"\n{'-'*50}")
        print(f"Evaluation for {model_name}:")
        print(f"{'-'*50}")
        
        print(f"Accuracy: {result['accuracy']:.4f}")
        print(f"Cross-validation: {result['cv_mean']:.4f} ± {result['cv_std']:.4f}")
        
        # Confusion Matrix
        viz.plot_confusion_matrix(y_test, result['predictions'], model_name)
        
        # ROC Curve
        if result['probabilities'] is not None:
            viz.plot_roc_curve(y_test, result['probabilities'], model_name)
        
        # Feature Importance
        if feature_names is not None and hasattr(result['model'], 'feature_importances_'):
            viz.plot_feature_importance(result['model'], feature_names, model_name)