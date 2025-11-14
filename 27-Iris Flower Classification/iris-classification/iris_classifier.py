import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

class IrisClassifier:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.accuracy = 0
        self.label_encoder = LabelEncoder()
        self.model_name = ""
        
    def load_data(self, file_path='Iris.csv'):
        """Load and preprocess the Iris dataset"""
        try:
            df = pd.read_csv(file_path)
            print("✅ Dataset loaded successfully!")
            print(f"Dataset shape: {df.shape}")
            return df
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return None
    
    def preprocess_data(self, df):
        """Preprocess the data for training"""
        # Create model directory if it doesn't exist
        if not os.path.exists('model'):
            os.makedirs('model')
            
        # Drop ID column if exists
        if 'Id' in df.columns:
            df = df.drop('Id', axis=1)
        
        # Check for missing values
        print("\nMissing values:")
        print(df.isnull().sum())
        
        # Separate features and target
        X = df.drop('Species', axis=1)
        y = df['Species']
        
        # Encode target labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f"\nFeatures shape: {X.shape}")
        print(f"Target shape: {y_encoded.shape}")
        print(f"Classes: {self.label_encoder.classes_}")
        
        return X, y_encoded
    
    def explore_data(self, df):
        """Explore the dataset with visualizations"""
        print("\n=== Dataset Exploration ===")
        print(f"Dataset Info:")
        print(df.info())
        print(f"\nDataset Description:")
        print(df.describe())
        print(f"\nSpecies Distribution:")
        print(df['Species'].value_counts())
        
        # Create visualizations
        plt.figure(figsize=(15, 10))
        
        # Subplot 1: Species distribution
        plt.subplot(2, 3, 1)
        df['Species'].value_counts().plot(kind='bar')
        plt.title('Species Distribution')
        plt.xticks(rotation=45)
        
        # Subplot 2: Sepal length vs width
        plt.subplot(2, 3, 2)
        colors = {'Iris-setosa': 'red', 'Iris-versicolor': 'blue', 'Iris-virginica': 'green'}
        for species in df['Species'].unique():
            species_data = df[df['Species'] == species]
            plt.scatter(species_data['SepalLengthCm'], species_data['SepalWidthCm'], 
                       label=species, alpha=0.7)
        plt.xlabel('Sepal Length (cm)')
        plt.ylabel('Sepal Width (cm)')
        plt.legend()
        plt.title('Sepal Length vs Width')
        
        # Subplot 3: Petal length vs width
        plt.subplot(2, 3, 3)
        for species in df['Species'].unique():
            species_data = df[df['Species'] == species]
            plt.scatter(species_data['PetalLengthCm'], species_data['PetalWidthCm'], 
                       label=species, alpha=0.7)
        plt.xlabel('Petal Length (cm)')
        plt.ylabel('Petal Width (cm)')
        plt.legend()
        plt.title('Petal Length vs Width')
        
        plt.tight_layout()
        plt.savefig('iris_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def train_models(self, X, y):
        """Train multiple models and select the best one"""
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models to try (all with probability support)
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(kernel='rbf', random_state=42, probability=True),
            'Logistic Regression': LogisticRegression(random_state=42)
        }
        
        best_model = None
        best_accuracy = 0
        best_model_name = ""
        
        print("\n=== Model Training Results ===")
        for name, model in models.items():
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Calculate accuracy
            accuracy = accuracy_score(y_test, y_pred)
            print(f"{name} Accuracy: {accuracy:.4f}")
            
            # Update best model
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model
                best_model_name = name
        
        self.model = best_model
        self.accuracy = best_accuracy
        self.model_name = best_model_name
        
        print(f"\n✅ Best Model: {best_model_name} with accuracy: {best_accuracy:.4f}")
        
        return X_test_scaled, y_test
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the best model"""
        if self.model is None:
            print("❌ No model trained yet!")
            return
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        
        print("\n=== Model Evaluation ===")
        print(f"Final Model Accuracy: {accuracy:.4f}")
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=self.label_encoder.classes_))
        
        # Confusion matrix
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
    
    def save_model(self, file_path='model/iris_model.pkl'):
        """Save the trained model and scaler"""
        if self.model is None:
            print("❌ No model to save!")
            return
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'accuracy': self.accuracy,
            'label_encoder': self.label_encoder,
            'model_name': self.model_name
        }
        
        joblib.dump(model_data, file_path)
        print(f"✅ Model saved to {file_path}")
    
    def test_prediction(self):
        """Test the model with sample data"""
        if self.model is None:
            print("❌ No model loaded!")
            return
        
        print("\n=== Testing Predictions ===")
        test_samples = [
            ([5.1, 3.5, 1.4, 0.2], "Iris-setosa"),
            ([6.0, 2.7, 5.1, 1.6], "Iris-versicolor"),
            ([6.3, 3.3, 6.0, 2.5], "Iris-virginica")
        ]
        
        for features, expected in test_samples:
            species, probabilities = self.predict_single(features)
            print(f"Features: {features}")
            print(f"Expected: {expected}, Predicted: {species}")
            print(f"Probabilities: {dict(zip(self.label_encoder.classes_, probabilities))}")
            print()
    
    def predict_single(self, features):
        """Predict species for a single sample"""
        if self.model is None:
            print("❌ No model loaded!")
            return None, None
        
        # Convert to numpy array and scale
        features_array = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features_array)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        
        # Get probabilities
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Convert prediction back to species name
        predicted_species = self.label_encoder.inverse_transform([prediction])[0]
        
        return predicted_species, probabilities

def main():
    """Main function to run the complete pipeline"""
    print("🚀 Starting Iris Flower Classification Pipeline...")
    
    # Initialize classifier
    classifier = IrisClassifier()
    
    # Load data
    df = classifier.load_data('Iris.csv')
    if df is None:
        print("❌ Failed to load data. Exiting.")
        return
    
    # Explore data
    classifier.explore_data(df)
    
    # Preprocess data
    X, y = classifier.preprocess_data(df)
    
    # Train models and select best one
    X_test, y_test = classifier.train_models(X, y)
    
    # Evaluate model
    classifier.evaluate_model(X_test, y_test)
    
    # Save model
    classifier.save_model()
    
    # Test predictions
    classifier.test_prediction()
    
    print("\n🎉 Model Training Complete!")
    print(f"Best model: {classifier.model_name}")
    print(f"Accuracy: {classifier.accuracy:.4f}")

if __name__ == "__main__":
    main()