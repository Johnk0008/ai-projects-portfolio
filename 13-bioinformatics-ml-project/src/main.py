import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from data_processing import SequenceProcessor
from ml_models import MLModels
from visualization import DataVisualizer

def main():
    print("=== Bioinformatics ML Application ===")
    
    # Initialize processor
    processor = SequenceProcessor()
    
    # Generate sample biological data
    print("Generating sample biological data...")
    sequences, labels = processor.generate_sample_data()
    
    # Extract features
    print("Extracting sequence features...")
    features = processor.extract_sequence_features(sequences)
    
    # Create DataFrame
    df = pd.DataFrame(features)
    df['label'] = labels
    
    print(f"Dataset shape: {df.shape}")
    print(f"Feature columns: {df.columns.tolist()}")
    
    # Initialize ML models
    ml_engine = MLModels()
    
    # Prepare features and labels
    X = df.drop('label', axis=1)
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Train and evaluate models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'predictions': y_pred
        }
        print(f"{name} Accuracy: {accuracy:.4f}")
        print(classification_report(y_test, y_pred))
    
    # Visualize results
    visualizer = DataVisualizer()
    visualizer.plot_model_comparison(results)
    visualizer.plot_feature_importance(models['Random Forest'], X.columns)
    
    # Demonstrate deep learning approach
    print("\n=== Deep Learning Demonstration ===")
    ml_engine.demo_neural_network(X.values, y)
    
    print("\n=== Application Completed ===")

if __name__ == "__main__":
    main()