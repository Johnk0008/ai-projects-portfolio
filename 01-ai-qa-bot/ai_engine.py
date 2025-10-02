# ai_engine.py
import openai
import requests
import json
from datetime import datetime
from config import Config, logger

class AIQABot:
    """AI Q&A Bot with multiple AI backend support"""
    
    def __init__(self):
        self.conversation_history = []
        self.total_questions = 0
        self.start_time = datetime.now()
        
    def query_openai(self, question, model=Config.DEFAULT_MODEL, temperature=0.7):
        """Query OpenAI's API for answers"""
        try:
            client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            
            # Prepare messages with conversation history
            messages = [
                {"role": "system", "content": "You are a helpful and knowledgeable AI assistant. Provide accurate and concise answers."}
            ]
            
            # Add conversation history for context
            for q, a in self.conversation_history[-3:]:  # Last 3 exchanges for context
                messages.extend([
                    {"role": "user", "content": q},
                    {"role": "assistant", "content": a}
                ])
            
            messages.append({"role": "user", "content": question})
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append((question, answer))
            self.total_questions += 1
            
            # Limit history size
            if len(self.conversation_history) > Config.MAX_HISTORY:
                self.conversation_history.pop(0)
                
            logger.info(f"OpenAI query processed - Question: {question[:50]}...")
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def get_stats(self):
        """Get conversation statistics"""
        session_duration = datetime.now() - self.start_time
        return {
            "total_questions": self.total_questions,
            "session_duration": str(session_duration).split('.')[0],
            "current_history_size": len(self.conversation_history)
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def export_conversation(self, filename="conversation_export.json"):
        """Export conversation to JSON file"""
        export_data = {
            "export_time": datetime.now().isoformat(),
            "total_questions": self.total_questions,
            "conversation": [
                {"question": q, "answer": a, "timestamp": datetime.now().isoformat()}
                for q, a in self.conversation_history
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Conversation exported to {filename}")
        return filename