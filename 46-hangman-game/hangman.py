import random

class HangmanGame:
    def __init__(self):
        # Predefined list of words
        self.words = ['python', 'hangman', 'computer', 'programming', 'algorithm']
        self.word = ''
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.max_attempts = 6
        self.game_over = False
        self.won = False
        
    def select_random_word(self):
        """Select a random word from the predefined list"""
        self.word = random.choice(self.words).lower()
        self.guessed_letters = ['_' for _ in self.word]
        
    def display_game_state(self):
        """Display current game state"""
        print("\n" + "="*40)
        print(f"Word: {' '.join(self.guessed_letters)}")
        print(f"Incorrect guesses: {self.incorrect_guesses}/{self.max_attempts}")
        print(f"Guessed letters: {', '.join(sorted(set([l for l in self.guessed_letters if l != '_']))) if any(l != '_' for l in self.guessed_letters) else 'None'}")
        
        # Display hangman progress
        self.display_hangman()
        
    def display_hangman(self):
        """Simple ASCII art for hangman progress"""
        stages = [
            """
               -----
               |   |
                   |
                   |
                   |
                   |
            =========
            """,
            """
               -----
               |   |
               O   |
                   |
                   |
                   |
            =========
            """,
            """
               -----
               |   |
               O   |
               |   |
                   |
                   |
            =========
            """,
            """
               -----
               |   |
               O   |
              /|   |
                   |
                   |
            =========
            """,
            """
               -----
               |   |
               O   |
              /|\\  |
                   |
                   |
            =========
            """,
            """
               -----
               |   |
               O   |
              /|\\  |
              /    |
                   |
            =========
            """,
            """
               -----
               |   |
               O   |
              /|\\  |
              / \\  |
                   |
            =========
            """
        ]
        print(stages[self.incorrect_guesses])
        
    def get_player_guess(self):
        """Get and validate player's guess"""
        while True:
            guess = input("Enter a letter: ").lower().strip()
            
            if len(guess) != 1:
                print("Please enter exactly one letter!")
                continue
                
            if not guess.isalpha():
                print("Please enter a valid letter!")
                continue
                
            if guess in self.guessed_letters:
                print(f"You already guessed '{guess}'!")
                continue
                
            return guess
            
    def process_guess(self, guess):
        """Process the player's guess"""
        if guess in self.word:
            # Update guessed letters with correct guess
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.guessed_letters[i] = guess
            print(f"Good guess! '{guess}' is in the word.")
        else:
            self.incorrect_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.")
            
    def check_game_status(self):
        """Check if game is won or lost"""
        # Check if won
        if '_' not in self.guessed_letters:
            self.game_over = True
            self.won = True
            return
            
        # Check if lost
        if self.incorrect_guesses >= self.max_attempts:
            self.game_over = True
            self.won = False
            
    def display_result(self):
        """Display game result"""
        print("\n" + "="*40)
        if self.won:
            print("🎉 Congratulations! You won! 🎉")
            print(f"The word was: {self.word}")
        else:
            print("💀 Game Over! You lost! 💀")
            print(f"The word was: {self.word}")
        print("="*40)
        
    def play_again(self):
        """Ask player if they want to play again"""
        while True:
            choice = input("\nDo you want to play again? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                
    def play(self):
        """Main game loop"""
        print("🎮 Welcome to Hangman Game! 🎮")
        print("Guess the word one letter at a time.")
        print(f"You have {self.max_attempts} incorrect guesses allowed.")
        
        while True:
            # Reset game state
            self.select_random_word()
            self.incorrect_guesses = 0
            self.game_over = False
            self.won = False
            
            print(f"\nNew game started! The word has {len(self.word)} letters.")
            
            # Game loop
            while not self.game_over:
                self.display_game_state()
                guess = self.get_player_guess()
                self.process_guess(guess)
                self.check_game_status()
                
            # Display final result
            self.display_game_state()
            self.display_result()
            
            # Ask to play again
            if not self.play_again():
                print("\nThanks for playing! Goodbye! 👋")
                break

def main():
    """Main function to start the game"""
    game = HangmanGame()
    game.play()

if __name__ == "__main__":
    main()