import re
import json
from typing import Dict, List, Optional

class RuleEngine:
    def __init__(self, rules_file: str = None):
        self.rules = {}
        self.patterns = {}
        
        # Load default rules
        self.load_default_rules()
        
        if rules_file:
            self.load_rules(rules_file)
    
    def load_default_rules(self):
        """Load default rules for common greetings"""
        default_rules = {
            'greeting': {
                'patterns': [
                    r'\b(hello|hi|hey|howdy|greetings|good morning|good afternoon|good evening)\b',
                    r'\b(what\'s up|sup|yo)\b',
                    r'^hi$|^hello$|^hey$'
                ],
                'response': "Hello! How can I assist you today?"
            },
            'goodbye': {
                'patterns': [
                    r'\b(bye|goodbye|see you|farewell|take care|have a good day)\b',
                    r'\b(see ya|cya|later|gotta go|I\'m leaving)\b'
                ],
                'response': "Goodbye! Have a great day!"
            },
            'thanks': {
                'patterns': [
                    r'\b(thank you|thanks|thank you very much|appreciate it|thanks a lot|thx)\b'
                ],
                'response': "You're welcome! How else can I help you?"
            }
        }
        
        for intent, data in default_rules.items():
            self.rules[intent] = data['response']
            self.patterns[intent] = data['patterns']
    
    def load_rules(self, filepath: str):
        """Load rules from JSON file"""
        try:
            with open(filepath, 'r') as f:
                rules_data = json.load(f)
                
                # Load rules
                for intent, response in rules_data.get('rules', {}).items():
                    self.rules[intent] = response
                
                # Load patterns
                for intent, patterns in rules_data.get('patterns', {}).items():
                    if intent not in self.patterns:
                        self.patterns[intent] = []
                    self.patterns[intent].extend(patterns)
                    
        except FileNotFoundError:
            print(f"Rules file {filepath} not found. Using default rules.")
        except json.JSONDecodeError:
            print(f"Error decoding rules file {filepath}. Using default rules.")
    
    def add_rule(self, intent: str, patterns: List[str], response: str):
        """Add a new rule"""
        self.rules[intent] = response
        if intent not in self.patterns:
            self.patterns[intent] = []
        self.patterns[intent].extend(patterns)
    
    def match_rule(self, text: str) -> Optional[str]:
        """Match input text against rule patterns"""
        text = text.lower().strip()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                try:
                    # Use regex pattern matching
                    if re.search(pattern, text, re.IGNORECASE):
                        return self.rules.get(intent, "I'm not sure how to respond to that.")
                except re.error:
                    # Fallback to simple string matching for invalid regex
                    if pattern.lower() in text:
                        return self.rules.get(intent, "I'm not sure how to respond to that.")
        
        return None
    
    def get_rule_based_response(self, text: str) -> str:
        """Get response based on rule matching"""
        if not text.strip():
            return "Please type something so I can help you!"
            
        response = self.match_rule(text)
        return response if response else None