# cli_version.py
import os
import sys
from ai_engine import AIQABot
from config import Config

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print application banner"""
    banner = """
    🤖 AI Q&A BOT - COMMAND LINE VERSION
    ===================================
    Welcome! Ask me anything. Type 'help' for commands, 'quit' to exit.
    """
    print(banner)

def print_help():
    """Display help information"""
    help_text = """
    Available Commands:
    - Type your question to get an AI-powered answer
    - 'stats' - Show conversation statistics
    - 'history' - Show conversation history
    - 'clear' - Clear conversation history
    - 'export' - Export conversation to JSON
    - 'help' - Show this help message
    - 'quit' - Exit the application
    """
    print(help_text)

def main():
    """Main CLI application"""
    try:
        Config.validate_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set your OPENAI_API_KEY in the .env file")
        return
    
    bot = AIQABot()
    clear_screen()
    print_banner()
    
    while True:
        try:
            user_input = input("\n🎯 Your question: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                stats = bot.get_stats()
                print(f"\nThanks for using AI Q&A Bot! You asked {stats['total_questions']} questions.")
                break
                
            elif user_input.lower() == 'help':
                print_help()
                
            elif user_input.lower() == 'stats':
                stats = bot.get_stats()
                print(f"\n📊 Conversation Statistics:")
                print(f"   Total Questions: {stats['total_questions']}")
                print(f"   Session Duration: {stats['session_duration']}")
                print(f"   History Size: {stats['current_history_size']}")
                
            elif user_input.lower() == 'history':
                if not bot.conversation_history:
                    print("\nNo conversation history yet.")
                else:
                    print(f"\n📝 Conversation History (last {len(bot.conversation_history)} exchanges):")
                    for i, (q, a) in enumerate(bot.conversation_history[-5:], 1):
                        print(f"\n{i}. Q: {q}")
                        print(f"   A: {a[:100]}..." if len(a) > 100 else f"   A: {a}")
                        
            elif user_input.lower() == 'clear':
                bot.clear_history()
                print("\n🗑️  Conversation history cleared!")
                
            elif user_input.lower() == 'export':
                filename = bot.export_conversation()
                print(f"\n💾 Conversation exported to: {filename}")
                
            else:
                # Process the question
                print("\n🤔 Thinking...")
                answer = bot.query_openai(user_input)
                print(f"\n🤖 Answer: {answer}")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()