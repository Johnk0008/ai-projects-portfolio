# working_rbi_chatbot.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RBIChatbot:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key or self.api_key == "your_actual_gemini_api_key_here":
            print("❌ GOOGLE_API_KEY not found or not set properly")
            print("💡 Please edit the .env file and add your real Gemini API key")
            print("💡 Get a free key from: https://aistudio.google.com/app/apikey")
            return
        
        try:
            # Configure the API - this should work with available versions
            genai.configure(api_key=self.api_key)
            
            # Get available models
            models = genai.list_models()
            gemini_models = [model.name for model in models if 'gemini' in model.name]
            print(f"✅ Available Gemini models: {gemini_models}")
            
            # Use the first available Gemini model
            if gemini_models:
                model_name = gemini_models[0]
                self.model = genai.GenerativeModel(model_name)
                print(f"✅ Using model: {model_name}")
            else:
                print("❌ No Gemini models available")
                return
                
            print("✅ RBI Chatbot initialized successfully!")
            
        except Exception as e:
            print(f"❌ Failed to initialize chatbot: {e}")
    
    def ask_question(self, question):
        """Ask a question about RBI NBFC regulations"""
        if not hasattr(self, 'model'):
            return "Chatbot not initialized. Please check your API key."
        
        prompt = f"""
        You are an expert AI assistant specialized in RBI's Master Directions on 
        Non-Banking Financial Company - Scale Based Regulation (NBFC-SBR).
        
        Please provide a comprehensive answer to this question based on RBI regulations:
        
        QUESTION: {question}
        
        Focus on these key areas:
        - Capital adequacy requirements (CRAR)
        - Tier I and Tier II capital requirements  
        - Minimum Net Owned Funds (NOF)
        - Leverage ratio limits
        - Classification into Base Layer, Middle Layer, Upper Layer
        - Regulatory compliance requirements
        
        Provide specific percentages, amounts, and regulatory references.
        Structure your answer clearly with bullet points.
        Be accurate and professional.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"❌ Error: {str(e)}"

def main():
    print("🏦 RBI NBFC Regulations Chatbot")
    print("=" * 60)
    print("This chatbot answers questions about RBI's Scale Based Regulation")
    print("for Non-Banking Financial Companies (NBFCs)")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = RBIChatbot()
    
    if not chatbot.api_key:
        return
    
    if not hasattr(chatbot, 'model'):
        return
    
    # Comprehensive test questions
    questions = [
        "What are the capital requirements for NBFCs in Scale Based Regulation?",
        "What is the minimum Capital to Risk-weighted Assets Ratio (CRAR) for Base Layer NBFCs?",
        "What are the different regulatory layers for NBFCs and how are they classified?",
        "What is the minimum Net Owned Funds requirement for non-deposit taking NBFCs?",
        "What are the Tier I and Tier II capital requirements for NBFCs?",
        "What is the leverage ratio limit for NBFCs?",
        "What are the key differences between Base Layer, Middle Layer and Upper Layer NBFCs?"
    ]
    
    print(f"\n📚 Testing RBI NBFC Regulations Knowledge")
    print(f"🎯 Number of questions: {len(questions)}")
    print("=" * 60)
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*70}")
        print(f"❓ QUESTION {i}: {question}")
        print(f"{'='*70}")
        
        print("🔄 Generating answer...")
        answer = chatbot.ask_question(question)
        
        print(f"\n📝 ANSWER:")
        print(answer)
        
        # Progress indicator
        if i < len(questions):
            print(f"\n📊 Progress: {i}/{len(questions)} questions completed")
            print("─" * 70)

    print(f"\n✅ All {len(questions)} questions completed!")
    print("🏦 Thank you for using the RBI NBFC Regulations Chatbot!")

if __name__ == "__main__":
    main()