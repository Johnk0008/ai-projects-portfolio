# src/vector_store.py
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import FakeEmbeddings
from src.config import Config

class VectorStoreManager:
    def __init__(self):
        self.config = Config()
        self.embeddings = FakeEmbeddings(size=384)  # Simple fake embeddings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    
    def create_documents_from_text(self, text: str):
        """Create documents from text"""
        print("Splitting text into chunks...")
        chunks = self.text_splitter.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]
        print(f"Created {len(documents)} documents")
        return documents
    
    def create_vector_store(self, documents):
        """Create and persist vector store"""
        print("Creating vector store...")
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.config.VECTOR_STORE_PATH,
            collection_name=self.config.CHROMA_COLLECTION_NAME
        )
        print("Vector store created successfully!")
        return vector_store
    
    def load_vector_store(self):
        """Load existing vector store"""
        print("Loading vector store...")
        vector_store = Chroma(
            persist_directory=self.config.VECTOR_STORE_PATH,
            embedding_function=self.embeddings,
            collection_name=self.config.CHROMA_COLLECTION_NAME
        )
        return vector_store
    
    def search_similar_documents(self, query: str, k: int = 4):
        """Search for similar documents"""
        vector_store = self.load_vector_store()
        results = vector_store.similarity_search(query, k=k)
        return results