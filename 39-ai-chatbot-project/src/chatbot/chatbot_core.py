import json
import numpy as np
from typing import Dict, Any
from .nlp_processor import NLPProcessor
from .ml_model import MLModel
from .rule_engine import RuleEngine

class ChatbotCore:
    def __init__(self, config_path: str = None):
        self.nlp_processor = NLPProcessor()
        self.ml_model = None
        self.rule_engine = RuleEngine()
        self.intents = {}
        self.confidence_threshold = 0.3  # Lowered from 0.7 to 0.3
        
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path: str):
        """Load chatbot configuration and intents"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.intents = config.get('intents', {})
                # Use lower confidence threshold
                self.confidence_threshold = config.get('confidence_threshold', 0.3)
                
                # Load rules if available
                rules_file = config.get('rules_file')
                if rules_file:
                    self.rule_engine.load_rules(rules_file)
                    
        except FileNotFoundError:
            print(f"Config file {config_path} not found. Using default rules.")
        except json.JSONDecodeError:
            print(f"Error decoding config file {config_path}. Using default rules.")
    
    def prepare_training_data(self):
        """Prepare training data from intents"""
        texts = []
        labels = []
        
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data.get('patterns', []):
                texts.append(pattern)
                labels.append(intent_name)
        
        return texts, labels
    
    def train_model(self, model_type: str = 'random_forest'):
        """Train the ML model"""
        texts, labels = self.prepare_training_data()
        
        if not texts:
            print("Warning: No training data available. Using rule-based only.")
            return {'train_accuracy': 0, 'test_accuracy': 0, 'classes': []}
        
        # Preprocess and vectorize texts
        self.nlp_processor.fit_vectorizer(texts)
        X = self.nlp_processor.vectorizer.transform(texts).toarray()
        y = np.array(labels)
        
        # Train ML model
        self.ml_model = MLModel(model_type)
        results = self.ml_model.train(X, y)
        
        return results
    
    def get_response(self, user_input: str) -> Dict[str, Any]:
        """Get chatbot response for user input"""
        if not user_input.strip():
            return {
                'response': "Please type a message so I can help you!",
                'confidence': 1.0,
                'method': 'fallback',
                'intent': 'empty_input'
            }
        
        # First, try rule-based matching
        rule_response = self.rule_engine.get_rule_based_response(user_input)
        if rule_response:
            return {
                'response': rule_response,
                'confidence': 1.0,
                'method': 'rule_based',
                'intent': 'rule_matched'
            }
        
        # If ML model is trained, use it
        if self.ml_model and hasattr(self.ml_model, 'model') and self.ml_model.model is not None:
            try:
                # Transform input
                X_input = self.nlp_processor.transform_text(user_input).toarray()
                
                # Get prediction
                probabilities = self.ml_model.predict_proba(X_input)[0]
                max_prob = np.max(probabilities)
                predicted_intent = self.ml_model.classes_[np.argmax(probabilities)]
                
                # Check confidence threshold (lowered)
                if max_prob >= self.confidence_threshold:
                    intent_responses = self.intents.get(predicted_intent, {}).get('responses', [])
                    response = np.random.choice(intent_responses) if intent_responses else "I understand, but I don't have a specific response for that."
                    
                    return {
                        'response': response,
                        'confidence': float(max_prob),
                        'method': 'ml_model',
                        'intent': predicted_intent
                    }
                else:
                    # Low confidence fallback
                    return {
                        'response': f"I think you're asking about '{predicted_intent}' but I'm not sure. Could you rephrase?",
                        'confidence': float(max_prob),
                        'method': 'ml_low_confidence',
                        'intent': predicted_intent
                    }
                
            except Exception as e:
                print(f"ML prediction error: {e}")
                # Fall through to fallback
        
        # Fallback response
        fallback_responses = [
            "I'm still learning. Could you try asking in a different way?",
            "I'm not sure I understand. Could you rephrase your question?",
            "That's an interesting question! I'm still learning how to respond to that.",
            "I'm here to help! Could you try asking that differently?"
        ]
        
        import random
        return {
            'response': random.choice(fallback_responses),
            'confidence': 0.0,
            'method': 'fallback',
            'intent': 'unknown'
        }
    
    def save_model(self, model_path: str):
        """Save trained model"""
        if self.ml_model and hasattr(self.ml_model, 'model') and self.ml_model.model is not None:
            self.ml_model.save_model(model_path)
        else:
            print("No trained model to save.")
    
    def load_model(self, model_path: str):
        """Load trained model"""
        try:
            self.ml_model = MLModel()
            self.ml_model.load_model(model_path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.ml_model = None