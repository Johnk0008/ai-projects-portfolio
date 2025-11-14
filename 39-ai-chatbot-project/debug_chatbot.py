import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from chatbot.chatbot_core import ChatbotCore
from chatbot.rule_engine import RuleEngine

def test_rule_engine():
    """Test the rule engine separately"""
    print("🧪 Testing Rule Engine...")
    
    rule_engine = RuleEngine('data/faq_dataset.json')
    
    test_messages = [
        "hi",
        "hello",
        "hey there",
        "good morning",
        "what's up",
        "bye",
        "goodbye",
        "thank you",
        "thanks",
        "random message"
    ]
    
    for message in test_messages:
        response = rule_engine.get_rule_based_response(message)
        print(f"Input: '{message}' -> Response: '{response}'")

def test_chatbot():
    """Test the complete chatbot"""
    print("\n🤖 Testing Complete Chatbot...")
    
    chatbot = ChatbotCore('data/intents.json')
    
    # Load rules
    chatbot.rule_engine.load_rules('data/faq_dataset.json')
    
    # Test without training first
    print("Testing with rule-based only (no ML training):")
    test_messages = ["hi", "hello", "what are your hours?", "thank you", "goodbye"]
    
    for message in test_messages:
        response = chatbot.get_response(message)
        print(f"\nYou: {message}")
        print(f"Bot: {response['response']}")
        print(f"Method: {response['method']}, Confidence: {response['confidence']:.2f}")
    
    # Now train and test again
    print("\n" + "="*50)
    print("Training ML model...")
    results = chatbot.train_model(model_type='random_forest')
    
    print(f"Training Accuracy: {results['train_accuracy']:.2%}")
    print(f"Test Accuracy: {results['test_accuracy']:.2%}")
    
    print("\nTesting with ML model:")
    for message in test_messages:
        response = chatbot.get_response(message)
        print(f"\nYou: {message}")
        print(f"Bot: {response['response']}")
        print(f"Method: {response['method']}, Confidence: {response['confidence']:.2f}")

if __name__ == '__main__':
    test_rule_engine()
    test_chatbot()