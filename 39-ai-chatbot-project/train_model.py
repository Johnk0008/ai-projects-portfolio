import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot.chatbot_core import ChatbotCore
import json

def main():
    print("🤖 Training AI Chatbot Model...")
    
    # Initialize chatbot
    chatbot = ChatbotCore('data/intents.json')
    
    # Load rules
    chatbot.rule_engine.load_rules('data/faq_dataset.json')
    
    # Train ML model
    print("Training machine learning model...")
    results = chatbot.train_model(model_type='random_forest')
    
    print(f"Training completed!")
    print(f"Training Accuracy: {results['train_accuracy']:.2%}")
    print(f"Test Accuracy: {results['test_accuracy']:.2%}")
    print(f"Classes: {', '.join(results['classes'])}")
    
    # Save model
    os.makedirs('models/saved_models', exist_ok=True)
    chatbot.save_model('models/saved_models/chatbot_model.joblib')
    print("Model saved to models/saved_models/chatbot_model.joblib")
    
    # Test the chatbot
    print("\n🧪 Testing chatbot...")
    test_messages = [
        "hello",
        "what are your hours?",
        "thank you",
        "goodbye",
        "what can you do?"
    ]
    
    for message in test_messages:
        response = chatbot.get_response(message)
        print(f"\nYou: {message}")
        print(f"Bot: {response['response']}")
        print(f"Method: {response['method']}, Confidence: {response['confidence']:.2f}")

if __name__ == '__main__':
    main()