# src/chatbot.py - Uses live Google Gemini API
import google.generativeai as genai
from src.config import Config

class RBIChatbot:
    def __init__(self, document_store):
        self.config = Config()
        
        try:
            # Configure Google AI with live API
            genai.configure(api_key=self.config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(self.config.MODEL_NAME)
            self.document_store = document_store
            print("✅ Google Gemini API configured successfully")
        except Exception as e:
            print(f"❌ API configuration error: {e}")
            raise
    
    def ask_question(self, question: str):
        """Ask question using live Gemini API"""
        try:
            print(f"🔍 Searching documents for: {question}")
            
            # Get relevant context
            relevant_docs = self.document_store.search(question, k=3)
            context = "\n\n".join(relevant_docs) if relevant_docs else "No specific context found."
            
            print(f"📚 Found {len(relevant_docs)} relevant document sections")
            
            # Create optimized prompt
            prompt = f"""You are an expert AI assistant for RBI's NBFC Scale Based Regulation.

DOCUMENT CONTEXT:
{context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Answer based ONLY on the document context provided
2. If context doesn't contain answer, say: "Based on the available document, I cannot find specific information about this."
3. Be accurate, professional, and concise
4. Include relevant regulatory details when available

ANSWER:"""
            
            print("🤖 Generating response with Gemini API...")
            # Live API call to Google Gemini
            response = self.model.generate_content(prompt)
            
            return {
                "question": question,
                "answer": response.text,
                "source_documents": relevant_docs,
                "success": True
            }
            
        except Exception as e:
            error_msg = f"API Error: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "question": question,
                "answer": f"I encountered an error: {str(e)}. Please check your API key and connection.",
                "source_documents": [],
                "success": False
            }