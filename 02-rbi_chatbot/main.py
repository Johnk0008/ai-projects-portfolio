# main.py - Main application
import os
import sys
import argparse

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from data_loader import DataLoader
    from simple_store import SimpleDocumentStore
    from chatbot import RBIChatbot
    from evaluator import Evaluator
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Please install required packages: pip install requests pypdf2 google-generativeai")
    sys.exit(1)

def main():
    print("🚀 RBI NBFC Chatbot - Live API Version")
    
    # Initialize components
    data_loader = DataLoader()
    document_store = SimpleDocumentStore()
    evaluator = Evaluator()
    
    parser = argparse.ArgumentParser(description="RBI NBFC Chatbot with Live APIs")
    parser.add_argument("--setup", action="store_true", help="Setup document store from RBI PDF")
    parser.add_argument("--question", type=str, help="Ask a specific question")
    parser.add_argument("--evaluate", action="store_true", help="Run evaluation tests")
    parser.add_argument("--interactive", action="store_true", help="Start interactive chat")
    
    args = parser.parse_args()
    
    if args.setup:
        print("📥 Setting up document store from RBI PDF...")
        pdf_text = data_loader.download_pdf()
        document_store.add_text(pdf_text)
        print("✅ Setup completed successfully!")
    
    if args.question:
        print(f"❓ Question: {args.question}")
        chatbot = RBIChatbot(document_store)
        response = chatbot.ask_question(args.question)
        print(f"\n🤖 Answer: {response['answer']}")
        if response['source_documents']:
            print(f"\n📚 Sources referenced: {len(response['source_documents'])}")
    
    if args.evaluate:
        print("🧪 Running comprehensive evaluation...")
        test_questions = data_loader.create_evaluation_questions()
        chatbot = RBIChatbot(document_store)
        results = evaluator.evaluate_chatbot(chatbot, test_questions)
        evaluator.print_summary(results)
        evaluator.save_results(results)
        print("✅ Evaluation completed!")
    
    if args.interactive:
        print("💬 Starting interactive chat session...")
        chatbot = RBIChatbot(document_store)
        
        print("🤖 RBI Chatbot ready! Ask about NBFC regulations.")
        print("   Type 'quit' to exit, 'eval' to run evaluation")
        
        while True:
            try:
                question = input("\n💭 Your question: ").strip()
                
                if question.lower() == 'quit':
                    print("👋 Thank you for using RBI Chatbot!")
                    break
                elif question.lower() == 'eval':
                    # Run quick evaluation
                    test_questions = data_loader.create_evaluation_questions()
                    results = evaluator.evaluate_chatbot(chatbot, test_questions[:2])
                    evaluator.print_summary(results)
                elif question:
                    response = chatbot.ask_question(question)
                    print(f"🤖 {response['answer']}")
                    if response['source_documents']:
                        print(f"   📖 {len(response['source_documents'])} sources referenced")
                else:
                    print("💡 Please enter a question")
                    
            except KeyboardInterrupt:
                print("\n👋 Session ended")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()