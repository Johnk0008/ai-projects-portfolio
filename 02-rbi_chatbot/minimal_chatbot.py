# minimal_chatbot.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class SimpleRBIChatbot:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GOOGLE_API_KEY in .env file")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def ask_question(self, question):
        prompt = f"""
        You are an expert on RBI's Master Directions on Non-Banking Financial Company - Scale Based Regulation.
        
        Answer the following question based on your knowledge of RBI NBFC regulations:
        
        Question: {question}
        
        Please provide a comprehensive answer covering:
        1. Capital requirements (CRAR, Tier I capital)
        2. Minimum Net Owned Funds
        3. Leverage ratios
        4. Any layer-specific requirements if applicable
        
        Structure your answer clearly with bullet points.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {e}"

# Test the chatbot
if __name__ == "__main__":
    chatbot = SimpleRBIChatbot()
    
    questions = [
        "What are the capital requirements for NBFCs?",
        "What is the minimum CRAR for Base Layer NBFCs?",
        "What are the different layers in Scale Based Regulation?",
        "What is the minimum Net Owned Funds requirement for NBFCs?"
    ]
    
    for question in questions:
        print(f"\n🤔 Question: {question}")
        print("📝 Answer:")
        answer = chatbot.ask_question(question)
        print(answer)
        print("\n" + "="*60)