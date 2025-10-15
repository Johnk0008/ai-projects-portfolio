# src/simple_store.py - NO external dependencies
import re

class SimpleDocumentStore:
    def __init__(self):
        self.documents = []
        print("✅ Document store initialized")
    
    def add_text(self, text: str):
        """Split text into chunks and store"""
        print("Processing text into searchable chunks...")
        
        # Split by paragraphs or sentences
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50:  # Only keep substantial paragraphs
                self.documents.append(para)
        
        print(f"✅ Stored {len(self.documents)} document chunks")
    
    def search(self, query: str, k: int = 3):
        """Simple but effective keyword search"""
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.documents:
            doc_lower = doc.lower()
            # Count matching words
            score = sum(1 for word in query_words if word in doc_lower)
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by relevance and return top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:k]]