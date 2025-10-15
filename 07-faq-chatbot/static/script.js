class Chatbot {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.suggestedQuestions = document.getElementById('suggestedQuestions');
        
        this.init();
    }
    
    init() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Load suggested questions
        this.loadSuggestedQuestions();
        
        // Add welcome message
        this.addBotMessage('Hello! I\'m your FAQ assistant. How can I help you today? You can ask me about shipping, returns, payments, or any other questions you might have.');
    }
    
    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;
        
        // Add user message
        this.addUserMessage(message);
        this.userInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            this.hideTypingIndicator();
            
            if (data.success) {
                if (data.results && data.results.length > 0) {
                    data.results.forEach((result, index) => {
                        setTimeout(() => {
                            this.addBotMessage(result.answer, result);
                        }, index * 300);
                    });
                } else {
                    this.addBotMessage('I\'m sorry, I couldn\'t find a good match for your question. Could you please rephrase or try asking something else?');
                }
            } else {
                this.addBotMessage('Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addBotMessage('Sorry, there was a network error. Please check your connection and try again.');
            console.error('Error:', error);
        }
    }
    
    addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.textContent = message;
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    addBotMessage(message, result = null) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        
        let messageHTML = message;
        
        if (result) {
            const confidenceClass = `confidence-${result.confidence}`;
            messageHTML += `
                <div class="similarity-score">
                    <span class="confidence-badge ${confidenceClass}">
                        ${result.confidence.toUpperCase()} CONFIDENCE
                    </span>
                    Similarity: ${(result.similarity_score * 100).toFixed(1)}%
                </div>
            `;
        }
        
        messageElement.innerHTML = messageHTML;
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.className = 'message bot-message typing-indicator';
        typingElement.id = 'typingIndicator';
        typingElement.innerHTML = `
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        this.chatMessages.appendChild(typingElement);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    loadSuggestedQuestions() {
        const questions = [
            "What is your return policy?",
            "How long does shipping take?",
            "What payment methods do you accept?",
            "How can I track my order?",
            "Do you offer international shipping?"
        ];
        
        this.suggestedQuestions.innerHTML = '';
        questions.forEach(question => {
            const questionElement = document.createElement('button');
            questionElement.className = 'suggested-question';
            questionElement.textContent = question;
            questionElement.addEventListener('click', () => {
                this.userInput.value = question;
                this.sendMessage();
            });
            this.suggestedQuestions.appendChild(questionElement);
        });
    }
    
    loadCategoryFAQs(category) {
        // Remove active class from all buttons
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Add active class to clicked button
        event.target.classList.add('active');
        
        // In a real implementation, you might want to filter FAQs by category
        this.addBotMessage(`Showing FAQs for ${category}. Ask me anything about ${category.toLowerCase()}!`);
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
    new Chatbot();
});