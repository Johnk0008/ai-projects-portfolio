from flask import Flask, render_template, request, jsonify
import logging
from config import config
from faq_data import FAQData
from nlp_processor import NLPProcessor
from intent_matcher import IntentMatcher
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize components
faq_data = FAQData()
nlp_processor = NLPProcessor(use_spacy=app.config['USE_SPACY'])
intent_matcher = IntentMatcher(
    nlp_processor=nlp_processor,
    similarity_threshold=app.config['SIMILARITY_THRESHOLD']
)

# Load FAQs into intent matcher
intent_matcher.load_faqs(faq_data.get_all_faqs())

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return FAQ responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            })
        
        logger.info(f"Received message: {user_message}")
        
        # Find best matching FAQs
        matches = intent_matcher.find_best_match(
            user_message, 
            top_k=app.config['MAX_RESPONSES']
        )
        
        logger.info(f"Found {len(matches)} matches for user query")
        
        return jsonify({
            'success': True,
            'results': matches,
            'query': user_message
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/faqs', methods=['GET'])
def get_faqs():
    """Get all FAQs"""
    try:
        category = request.args.get('category')
        if category:
            faqs = intent_matcher.get_faqs_by_category(category)
        else:
            faqs = faq_data.get_all_faqs()
        
        return jsonify({
            'success': True,
            'faqs': faqs
        })
    except Exception as e:
        logger.error(f"Error getting FAQs: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get all FAQ categories"""
    try:
        categories = intent_matcher.get_faq_categories()
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/add-faq', methods=['POST'])
def add_faq():
    """Add new FAQ (admin functionality)"""
    try:
        data = request.get_json()
        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category', 'general')
        tags = data.get('tags', [])
        
        if not question or not answer:
            return jsonify({
                'success': False,
                'error': 'Question and answer are required'
            }), 400
        
        # Add to data storage
        new_faq = faq_data.add_faq(question, answer, category, tags)
        
        # Reload FAQs in intent matcher
        intent_matcher.load_faqs(faq_data.get_all_faqs())
        
        return jsonify({
            'success': True,
            'faq': new_faq
        })
        
    except Exception as e:
        logger.error(f"Error adding FAQ: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'faqs_loaded': len(faq_data.get_all_faqs()),
        'components': {
            'nlp_processor': 'active',
            'intent_matcher': 'active',
            'faq_data': 'active'
        }
    })

if __name__ == '__main__':
    logger.info("Starting FAQ Chatbot Application...")
    logger.info(f"Loaded {len(faq_data.get_all_faqs())} FAQs")
    logger.info(f"Similarity threshold: {app.config['SIMILARITY_THRESHOLD']}")
    logger.info(f"Using spaCy: {app.config['USE_SPACY']}")
    
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )