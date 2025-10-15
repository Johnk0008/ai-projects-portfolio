import json
import random
import requests
from typing import List, Dict, Optional

class QuoteManager:
    def __init__(self):
        self.quotes = self._load_default_quotes()
        self.current_quote_index = -1
    
    def _load_default_quotes(self) -> List[Dict[str, str]]:
        """Load default quotes library"""
        default_quotes = [
            {
                "text": "The only way to do great work is to love what you do.",
                "author": "Steve Jobs"
            },
            {
                "text": "Innovation distinguishes between a leader and a follower.",
                "author": "Steve Jobs"
            },
            {
                "text": "Your time is limited, so don't waste it living someone else's life.",
                "author": "Steve Jobs"
            },
            {
                "text": "Stay hungry, stay foolish.",
                "author": "Steve Jobs"
            },
            {
                "text": "The greatest glory in living lies not in never falling, but in rising every time we fall.",
                "author": "Nelson Mandela"
            },
            {
                "text": "The way to get started is to quit talking and begin doing.",
                "author": "Walt Disney"
            },
            {
                "text": "If life were predictable it would cease to be life, and be without flavor.",
                "author": "Eleanor Roosevelt"
            },
            {
                "text": "If you look at what you have in life, you'll always have more.",
                "author": "Oprah Winfrey"
            },
            {
                "text": "Life is what happens when you're busy making other plans.",
                "author": "John Lennon"
            },
            {
                "text": "Spread love everywhere you go. Let no one ever come to you without leaving happier.",
                "author": "Mother Teresa"
            },
            {
                "text": "When you reach the end of your rope, tie a knot in it and hang on.",
                "author": "Franklin D. Roosevelt"
            },
            {
                "text": "Always remember that you are absolutely unique. Just like everyone else.",
                "author": "Margaret Mead"
            },
            {
                "text": "Don't judge each day by the harvest you reap but by the seeds that you plant.",
                "author": "Robert Louis Stevenson"
            },
            {
                "text": "The future belongs to those who believe in the beauty of their dreams.",
                "author": "Eleanor Roosevelt"
            },
            {
                "text": "Tell me and I forget. Teach me and I remember. Involve me and I learn.",
                "author": "Benjamin Franklin"
            },
            {
                "text": "The best and most beautiful things in the world cannot be seen or even touched — they must be felt with the heart.",
                "author": "Helen Keller"
            },
            {
                "text": "It is during our darkest moments that we must focus to see the light.",
                "author": "Aristotle"
            },
            {
                "text": "Whoever is happy will make others happy too.",
                "author": "Anne Frank"
            },
            {
                "text": "Do not go where the path may lead, go instead where there is no path and leave a trail.",
                "author": "Ralph Waldo Emerson"
            },
            {
                "text": "You will face many defeats in life, but never let yourself be defeated.",
                "author": "Maya Angelou"
            },
            {
                "text": "Be yourself; everyone else is already taken.",
                "author": "Oscar Wilde"
            },
            {
                "text": "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.",
                "author": "Albert Einstein"
            },
            {
                "text": "So many books, so little time.",
                "author": "Frank Zappa"
            },
            {
                "text": "Be the change that you wish to see in the world.",
                "author": "Mahatma Gandhi"
            },
            {
                "text": "In three words I can sum up everything I've learned about life: it goes on.",
                "author": "Robert Frost"
            }
        ]
        return default_quotes
    
    def get_random_quote(self) -> Dict[str, str]:
        """Get a random quote that's different from the current one"""
        if not self.quotes:
            return {"text": "No quotes available", "author": "System"}
        
        # Ensure we get a different quote than the current one
        available_indices = list(range(len(self.quotes)))
        if self.current_quote_index in available_indices and len(available_indices) > 1:
            available_indices.remove(self.current_quote_index)
        
        new_index = random.choice(available_indices)
        self.current_quote_index = new_index
        return self.quotes[new_index]
    
    def get_quote_count(self) -> int:
        """Get total number of quotes"""
        return len(self.quotes)
    
    def fetch_online_quote(self) -> Optional[Dict[str, str]]:
        """Fetch a random quote from an online API (fallback)"""
        try:
            response = requests.get("https://api.quotable.io/random", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "text": data["content"],
                    "author": data["author"]
                }
        except Exception as e:
            print(f"Online quote fetch failed: {e}")
            # Fallback to local random quote
            return self.get_random_quote()
        return None
    
    def add_custom_quote(self, text: str, author: str):
        """Add a custom quote to the collection"""
        self.quotes.append({
            "text": text,
            "author": author
        })
    
    def export_quotes(self, filename: str = "my_quotes.json") -> bool:
        """Export quotes to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({"quotes": self.quotes}, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def import_quotes(self, filename: str = "my_quotes.json") -> bool:
        """Import quotes from a JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.quotes.extend(data.get("quotes", []))
            return True
        except Exception as e:
            print(f"Import failed: {e}")
            return False