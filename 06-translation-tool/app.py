from flask import Flask, render_template, request, jsonify, flash
from googletrans import Translator, LANGUAGES
import logging
from utils import copy_to_clipboard, text_to_speech

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize translator
translator = Translator()

# Extended language list
SUPPORTED_LANGUAGES = {
    'auto': 'Auto Detect',
    'en': 'English',
    'es': 'Spanish', 
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'el': 'Greek',
    'he': 'Hebrew',
    'th': 'Thai',
    'vi': 'Vietnamese'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = None
    source_lang = 'auto'
    target_lang = 'es'
    source_text = ''
    
    if request.method == 'POST':
        try:
            source_text = request.form.get('source_text', '').strip()
            source_lang = request.form.get('source_lang', 'auto')
            target_lang = request.form.get('target_lang', 'es')
            
            if not source_text:
                flash('Please enter text to translate', 'error')
                return render_template('index.html', 
                                    languages=SUPPORTED_LANGUAGES,
                                    source_text=source_text,
                                    source_lang=source_lang,
                                    target_lang=target_lang)
            
            # Perform translation
            if source_lang == 'auto':
                # Auto-detect source language
                detected = translator.detect(source_text)
                source_lang = detected.lang
                logger.info(f"Auto-detected language: {source_lang}")
            
            translation = translator.translate(
                source_text, 
                src=source_lang, 
                dest=target_lang
            )
            
            translated_text = translation.text
            logger.info(f"Translated from {source_lang} to {target_lang}")
            
            flash('Translation completed successfully!', 'success')
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            flash(f'Translation failed: {str(e)}', 'error')
    
    return render_template('index.html',
                         languages=SUPPORTED_LANGUAGES,
                         translated_text=translated_text,
                         source_text=source_text,
                         source_lang=source_lang,
                         target_lang=target_lang)

@app.route('/copy-to-clipboard', methods=['POST'])
def copy_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if copy_to_clipboard(text):
            return jsonify({'success': True, 'message': 'Text copied to clipboard'})
        else:
            return jsonify({'success': False, 'error': 'Failed to copy text'})
            
    except Exception as e:
        logger.error(f"Clipboard error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/text-to-speech', methods=['POST'])
def speak_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        lang = data.get('lang', 'en')
        
        if text_to_speech(text, lang):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Text-to-speech failed'})
            
    except Exception as e:
        logger.error(f"Text-to-speech error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/languages', methods=['GET'])
def get_languages():
    return jsonify(SUPPORTED_LANGUAGES)

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', 
                         languages=SUPPORTED_LANGUAGES,
                         error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html',
                         languages=SUPPORTED_LANGUAGES,
                         error="Internal server error"), 500

if __name__ == '__main__':
    print("Starting Translation Tool...")
    print("Supported languages:", list(SUPPORTED_LANGUAGES.keys()))
    app.run(debug=True, host='0.0.0.0', port=5000)