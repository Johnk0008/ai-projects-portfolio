import json
import os

class FlashcardManager:
    def __init__(self, filename="flashcards.json"):
        self.filename = filename
        self.flashcards = []
        self.current_index = 0
        self.load_flashcards()
    
    def load_flashcards(self):
        """Load flashcards from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.flashcards = data.get('flashcards', [])
                    self.current_index = min(data.get('current_index', 0), max(0, len(self.flashcards) - 1))
            except (json.JSONDecodeError, KeyError, Exception) as e:
                print(f"Error loading flashcards: {e}")
                self.flashcards = []
                self.current_index = 0
    
    def save_flashcards(self):
        """Save flashcards to JSON file"""
        try:
            data = {
                'flashcards': self.flashcards,
                'current_index': self.current_index
            }
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving flashcards: {e}")
    
    def add_flashcard(self, question, answer):
        """Add a new flashcard"""
        self.flashcards.append({
            'question': question,
            'answer': answer
        })
        self.save_flashcards()
    
    def edit_flashcard(self, index, question, answer):
        """Edit an existing flashcard"""
        if 0 <= index < len(self.flashcards):
            self.flashcards[index] = {
                'question': question,
                'answer': answer
            }
            self.save_flashcards()
            return True
        return False
    
    def delete_flashcard(self, index):
        """Delete a flashcard"""
        if 0 <= index < len(self.flashcards):
            self.flashcards.pop(index)
            # Adjust current index if needed
            if self.current_index >= len(self.flashcards):
                self.current_index = max(0, len(self.flashcards) - 1)
            self.save_flashcards()
            return True
        return False
    
    def get_current_flashcard(self):
        """Get current flashcard"""
        if self.flashcards and 0 <= self.current_index < len(self.flashcards):
            return self.flashcards[self.current_index]
        return None
    
    def next_card(self):
        """Move to next card"""
        if self.flashcards:
            self.current_index = (self.current_index + 1) % len(self.flashcards)
            self.save_flashcards()
    
    def previous_card(self):
        """Move to previous card"""
        if self.flashcards:
            self.current_index = (self.current_index - 1) % len(self.flashcards)
            self.save_flashcards()
    
    def get_card_count(self):
        """Get total number of flashcards"""
        return len(self.flashcards)