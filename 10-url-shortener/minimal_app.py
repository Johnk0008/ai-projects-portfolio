from flask import Flask, request, jsonify, redirect
import sqlite3
import string
import random
import os
from urllib.parse import urlparse

app = Flask(__name__)

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('urls.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS url_mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            clicks INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def generate_short_code():
    """Generate random 6-character code"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=6))

def is_valid_url(url):
    """Simple URL validation"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('urls.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    """Simple HTML interface"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔗 URL Shortener</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; 
                display: flex; 
                align-items: center; 
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 500px;
                width: 100%;
            }
            h1 { 
                text-align: center; 
                margin-bottom: 30px; 
                color: #333;
                font-size: 2em;
            }
            .input-group {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            input[type="text"] {
                flex: 1;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                padding: 15px 25px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                transition: background 0.3s;
            }
            button:hover {
                background: #5a6fd8;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                display: none;
            }
            .success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .short-url {
                margin: 10px 0;
                font-weight: bold;
                word-break: break-all;
            }
            .copy-btn {
                background: #28a745;
                margin-left: 10px;
            }
            .copy-btn:hover {
                background: #218838;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔗 URL Shortener</h1>
            <div class="input-group">
                <input type="text" id="longUrl" placeholder="https://example.com/very/long/url..." />
                <button onclick="shortenUrl()">Shorten</button>
            </div>
            <div id="result" class="result"></div>
        </div>

        <script>
            async function shortenUrl() {
                const longUrl = document.getElementById('longUrl').value.trim();
                const resultDiv = document.getElementById('result');
                
                if (!longUrl) {
                    showResult('Please enter a URL', 'error');
                    return;
                }
                
                try {
                    const response = await fetch('/shorten', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ url: longUrl })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        const shortUrl = `${window.location.origin}/${data.short_code}`;
                        showResult(`
                            <div>✅ URL shortened successfully!</div>
                            <div class="short-url">
                                Short URL: <a href="${shortUrl}" target="_blank">${shortUrl}</a>
                                <button class="copy-btn" onclick="copyToClipboard('${shortUrl}')">Copy</button>
                            </div>
                            <div><small>Clicks: ${data.clicks}</small></div>
                        `, 'success');
                    } else {
                        showResult('Error: ' + data.error, 'error');
                    }
                } catch (error) {
                    showResult('Network error: ' + error.message, 'error');
                }
            }
            
            function showResult(message, type) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = message;
                resultDiv.className = 'result ' + type;
                resultDiv.style.display = 'block';
            }
            
            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(() => {
                    alert('✅ URL copied to clipboard!');
                });
            }
            
            // Enter key support
            document.getElementById('longUrl').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    shortenUrl();
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Shorten URL endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'success': False, 'error': 'No URL provided'})
        
        long_url = data['url'].strip()
        
        # Validate URL
        if not is_valid_url(long_url):
            return jsonify({'success': False, 'error': 'Invalid URL. Include http:// or https://'})
        
        conn = get_db_connection()
        
        # Check if URL already exists
        existing = conn.execute(
            'SELECT * FROM url_mappings WHERE long_url = ?', 
            (long_url,)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({
                'success': True,
                'short_code': existing['short_code'],
                'clicks': existing['clicks']
            })
        
        # Generate unique short code
        while True:
            short_code = generate_short_code()
            # Check if code is unique
            if not conn.execute('SELECT * FROM url_mappings WHERE short_code = ?', (short_code,)).fetchone():
                break
        
        # Insert new mapping
        conn.execute(
            'INSERT INTO url_mappings (long_url, short_code) VALUES (?, ?)',
            (long_url, short_code)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'short_code': short_code,
            'clicks': 0
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Server error'})

@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect to original URL"""
    try:
        conn = get_db_connection()
        mapping = conn.execute(
            'SELECT * FROM url_mappings WHERE short_code = ?', 
            (short_code,)
        ).fetchone()
        
        if not mapping:
            conn.close()
            return jsonify({'error': 'Short URL not found'}), 404
        
        # Update click count
        conn.execute(
            'UPDATE url_mappings SET clicks = clicks + 1 WHERE short_code = ?',
            (short_code,)
        )
        conn.commit()
        conn.close()
        
        return redirect(mapping['long_url'])
        
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

@app.route('/stats')
def get_stats():
    """Get statistics for all URLs"""
    try:
        conn = get_db_connection()
        urls = conn.execute(
            'SELECT * FROM url_mappings ORDER BY created_at DESC'
        ).fetchall()
        conn.close()
        
        stats = []
        for url in urls:
            stats.append({
                'long_url': url['long_url'],
                'short_code': url['short_code'],
                'short_url': f"{request.host_url}{url['short_code']}",
                'clicks': url['clicks'],
                'created_at': url['created_at']
            })
        
        return jsonify({'urls': stats})
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    print("🚀 Starting URL Shortener...")
    print("📊 Access the application at: http://localhost:5000")
    print("📈 View stats at: http://localhost:5000/stats")
    app.run(debug=True, host='0.0.0.0', port=5000)