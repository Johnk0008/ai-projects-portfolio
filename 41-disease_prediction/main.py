from data.data_loader import MedicalDataLoader
from models.model_trainer import DiseasePredictor
from utils.helpers import evaluate_model
import argparse

def main():
    parser = argparse.ArgumentParser(description='Disease Prediction System')
    parser.add_argument('--dataset', type=str, default='heart', 
                       choices=['heart', 'diabetes', 'breast_cancer'],
                       help='Dataset to use for training')
    parser.add_argument('--train', action='store_true', help='Train models')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate models')
    
    args = parser.parse_args()
    
    # Initialize components
    data_loader = MedicalDataLoader()
    predictor = DiseasePredictor()
    
    if args.train or args.evaluate:
        print(f"Loading {args.dataset} dataset...")
        X_train, X_test, y_train, y_test = data_loader.prepare_data(args.dataset)
        
        print(f"Dataset loaded: {X_train.shape[0]} training samples, {X_test.shape[0]} test samples")
        
        if args.train:
            print("Training models...")
            results = predictor.train_models(X_train, y_train, X_test, y_test, args.dataset)
            
            if args.evaluate:
                feature_names = data_loader.get_dataset(args.dataset).columns[:-1]
                evaluate_model(results, X_test, y_test, feature_names)
    
    else:
        print("Please specify --train to train models or run the Streamlit app for interactive use.")
        print("To run Streamlit app: streamlit run apps/streamlit_app.py")

if __name__ == "__main__":
    main()