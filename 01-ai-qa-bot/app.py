# app.py
import streamlit as st
import json
from datetime import datetime
from ai_engine import AIQABot
from config import Config

# Page configuration
st.set_page_config(
    page_title="AI Q&A Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'bot' not in st.session_state:
        st.session_state.bot = AIQABot()
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # API Configuration
        st.subheader("API Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", 
                               value=Config.OPENAI_API_KEY if Config.OPENAI_API_KEY != 'your-api-key-here' else "")
        
        if api_key and api_key != Config.OPENAI_API_KEY:
            Config.OPENAI_API_KEY = api_key
        
        # Model Settings
        st.subheader("Model Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1,
                               help="Higher values make output more random")
        
        # App Info
        st.subheader("App Information")
        st.info("""
        This AI Q&A Bot uses OpenAI's GPT models to answer your questions. 
        You can ask anything from technical topics to general knowledge!
        """)
        
        # Statistics
        stats = st.session_state.bot.get_stats()
        st.metric("Total Questions", stats['total_questions'])
        st.metric("Session Duration", stats['session_duration'])
        
        # Export functionality
        if st.button("📤 Export Conversation"):
            filename = f"conversation_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            st.session_state.bot.export_conversation(filename)
            st.success(f"Conversation exported to {filename}")
            
        if st.button("🗑️ Clear History"):
            st.session_state.bot.clear_history()
            st.session_state.conversation = []
            st.rerun()
    
    # Main content area
    st.title("🤖 AI Q&A Bot")
    st.markdown("Ask me anything and I'll do my best to answer!")
    
    # Conversation display
    st.subheader("💬 Conversation")
    
    # Display conversation history
    for i, (question, answer) in enumerate(st.session_state.conversation):
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(answer)
        st.markdown("---")
    
    # Question input
    st.subheader("🎯 Ask a Question")
    question = st.text_input("Type your question here:", placeholder="e.g., Explain quantum computing in simple terms...", key="question_input")
    
    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.button("Ask 🤖", type="primary", key="ask_button"):
            if question.strip():
                with st.spinner("Thinking..."):
                    try:
                        Config.validate_config()
                        answer = st.session_state.bot.query_openai(question, temperature=temperature)
                        
                        # Update conversation
                        st.session_state.conversation.append((question, answer))
                        
                        # Rerun to update display
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a question!")
    
    with col2:
        if st.button("Example Questions 🎲", key="example_button"):
            examples = [
                "Explain quantum computing in simple terms",
                "What are the benefits of renewable energy?",
                "How does machine learning work?",
                "Tell me about the history of artificial intelligence"
            ]
            import random
            example = random.choice(examples)
            st.session_state.question_input = example
            st.rerun()

if __name__ == "__main__":
    main()