import pandas as pd
import numpy as np
import os
from src.data_processing import DataProcessor
from src.feature_engineering import FeatureEngineer
from src.model_training import ModelTrainer
from src.evaluation import ModelEvaluator
from config import *

def main():
    print("=== Credit Scoring Model Implementation ===\n")
    
    # Step 1: Data Processing
    print("Step 1: Data Processing...")
    processor = DataProcessor()
    df = processor.load_data()  # Generate sample data
    
    print(f"Dataset shape: {df.shape}")
    print(f"Target distribution:\n{df['credit_score'].value_counts()}")
    
    # Handle missing values
    df = processor.handle_missing_values(df)
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = processor.split_data(df)
    
    print(f"Training set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Step 2: Feature Engineering
    print("\nStep 2: Feature Engineering...")
    feature_engineer = FeatureEngineer()
    
    # Create new features
    X_train_fe = feature_engineer.create_features(X_train)
    X_val_fe = feature_engineer.create_features(X_val)
    X_test_fe = feature_engineer.create_features(X_test)
    
    print(f"Original features: {X_train.shape[1]}")
    print(f"After feature engineering: {X_train_fe.shape[1]}")
    
    # Fit preprocessor on training data
    feature_engineer.fit_preprocessor(X_train_fe)
    
    # Transform all datasets
    X_train_processed = feature_engineer.transform_features(X_train_fe)
    X_val_processed = feature_engineer.transform_features(X_val_fe)
    X_test_processed = feature_engineer.transform_features(X_test_fe)
    
    print(f"After preprocessing: {X_train_processed.shape[1]} features")
    
    # Save preprocessor
    feature_engineer.save_preprocessor(MODELS_DIR / "preprocessor.joblib")
    
    # Step 3: Model Training
    print("\nStep 3: Model Training...")
    model_trainer = ModelTrainer()
    
    # Train models
    results = model_trainer.train_models(X_train_processed, y_train)
    
    # Step 4: Model Evaluation
    print("\nStep 4: Model Evaluation...")
    evaluator = ModelEvaluator()
    
    # Evaluate on validation set
    print("\n=== Validation Set Performance ===")
    val_results = {}
    for model_name in results.keys():
        y_pred = model_trainer.predict(model_name, X_val_processed)
        y_pred_proba = model_trainer.predict_proba(model_name, X_val_processed)
        
        print(f"\n--- {model_name.upper()} ---")
        metrics = evaluator.generate_report(y_val, y_pred, y_pred_proba, model_name)
        val_results[model_name] = metrics
    
    # Final evaluation on test set with best model
    print("\n=== Final Test Set Performance (Best Model) ===")
    best_model_name = max(val_results, key=lambda x: val_results[x]['f1'])
    print(f"Best model: {best_model_name}")
    
    y_test_pred = model_trainer.predict(best_model_name, X_test_processed)
    y_test_pred_proba = model_trainer.predict_proba(best_model_name, X_test_processed)
    
    test_metrics = evaluator.generate_report(
        y_test, y_test_pred, y_test_pred_proba, f"Best Model ({best_model_name})"
    )
    
    # Feature importance
    best_model = results[best_model_name]['model']
    if hasattr(best_model, 'feature_importances_'):
        print("\nFeature Importance Analysis:")
        evaluator.feature_importance_plot(best_model, X_train_processed.columns.tolist())
    
    # Save best model
    model_trainer.save_best_model(MODELS_DIR / "best_model.joblib")
    print(f"\nBest model saved to: {MODELS_DIR / 'best_model.joblib'}")
    
    # Print summary
    print("\n=== PROJECT SUMMARY ===")
    print(f"Dataset size: {df.shape}")
    print(f"Target distribution: {df['credit_score'].value_counts().to_dict()}")
    print(f"Best model: {best_model_name}")
    print(f"Test F1-Score: {test_metrics['f1']:.4f}")
    print(f"Test ROC-AUC: {test_metrics.get('roc_auc', 'N/A')}")
    print(f"Test Precision: {test_metrics['precision']:.4f}")
    print(f"Test Recall: {test_metrics['recall']:.4f}")
    
    return {
        'processor': processor,
        'feature_engineer': feature_engineer,
        'model_trainer': model_trainer,
        'evaluator': evaluator,
        'test_metrics': test_metrics
    }

if __name__ == "__main__":
    results = main()