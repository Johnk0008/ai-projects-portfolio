from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from config import Config
from models import db, URLMapping, URLClick
from forms import URLShortenForm, URLAnalyticsForm
from utils import validate_url, get_client_info, generate_qr_code_url
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

@app.route('/')
def index():
    form = URLShortenForm()
    return render_template('index.html', form=form)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    form = URLShortenForm()
    
    if form.validate_on_submit():
        long_url = form.long_url.data
        custom_alias = form.custom_alias.data
        title = form.title.data
        description = form.description.data
        expires_in_days = int(form.expires_in_days.data) if form.expires_in_days.data else None
        
        # Validate URL
        is_valid, validated_url = validate_url(long_url)
        if not is_valid:
            return jsonify({'success': False, 'error': validated_url})
        
        # Check if custom alias is available
        if custom_alias:
            existing = URLMapping.query.filter_by(short_code=custom_alias).first()
            if existing:
                return jsonify({'success': False, 'error': 'Custom alias already taken'})
        
        # Check if URL already exists (without custom alias)
        if not custom_alias:
            existing = URLMapping.query.filter_by(long_url=validated_url).first()
            if existing:
                return jsonify({
                    'success': True, 
                    'existing': True,
                    **existing.to_dict()
                })
        
        # Create new URL mapping
        try:
            new_url = URLMapping(
                long_url=validated_url,
                custom_alias=custom_alias,
                title=title,
                description=description,
                expires_in_days=expires_in_days
            )
            
            db.session.add(new_url)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'existing': False,
                **new_url.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Database error: ' + str(e)})
    
    # Form validation failed
    errors = {field.name: field.errors for field in form if field.errors}
    return jsonify({'success': False, 'error': 'Form validation failed', 'errors': errors})

@app.route('/r/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL with analytics tracking"""
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()
    
    if not url_mapping:
        flash('Short URL not found', 'error')
        return redirect(url_for('index'))
    
    if not url_mapping.is_active:
        flash('This short URL has been deactivated', 'error')
        return redirect(url_for('index'))
    
    if url_mapping.is_expired():
        flash('This short URL has expired', 'error')
        return redirect(url_for('index'))
    
    # Track the click
    client_info = get_client_info()
    
    click = URLClick(
        url_id=url_mapping.id,
        ip_address=client_info['ip_address'],
        user_agent=client_info['user_agent'],
        referrer=client_info['referrer'],
        browser=client_info['browser'],
        platform=client_info['platform']
    )
    
    # Update URL mapping stats
    url_mapping.total_clicks += 1
    url_mapping.last_accessed = datetime.utcnow()
    
    db.session.add(click)
    db.session.commit()
    
    return redirect(url_mapping.long_url)

@app.route('/dashboard')
def dashboard():
    """Dashboard showing all URLs and stats"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    urls = URLMapping.query.order_by(URLMapping.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    total_urls = URLMapping.query.count()
    total_clicks = db.session.query(db.func.sum(URLMapping.total_clicks)).scalar() or 0
    
    # Recent activity
    recent_clicks = URLClick.query.order_by(URLClick.clicked_at.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                         urls=urls,
                         total_urls=total_urls,
                         total_clicks=total_clicks,
                         recent_clicks=recent_clicks)

@app.route('/analytics/<short_code>')
def url_analytics(short_code):
    """Detailed analytics for a specific URL"""
    form = URLAnalyticsForm()
    days = int(request.args.get('days', 30))
    
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()
    if not url_mapping:
        flash('URL not found', 'error')
        return redirect(url_for('dashboard'))
    
    # Get analytics data
    analytics_data = url_mapping.get_analytics(days=days)
    
    # Get recent clicks
    recent_clicks = URLClick.query.filter_by(url_id=url_mapping.id)\
        .order_by(URLClick.clicked_at.desc())\
        .limit(50)\
        .all()
    
    # Generate QR code
    qr_code_url = generate_qr_code_url(request.host_url + 'r/' + short_code)
    
    return render_template('analytics.html',
                         url=url_mapping,
                         analytics=analytics_data,
                         recent_clicks=recent_clicks,
                         qr_code_url=qr_code_url,
                         form=form,
                         days=days)

@app.route('/api/url/<short_code>/deactivate', methods=['POST'])
def deactivate_url(short_code):
    """Deactivate a URL"""
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()
    
    if not url_mapping:
        return jsonify({'success': False, 'error': 'URL not found'})
    
    url_mapping.is_active = False
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'URL deactivated'})

@app.route('/api/url/<short_code>/reactivate', methods=['POST'])
def reactivate_url(short_code):
    """Reactivate a URL"""
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()
    
    if not url_mapping:
        return jsonify({'success': False, 'error': 'URL not found'})
    
    url_mapping.is_active = True
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'URL reactivated'})

@app.route('/api/url/<short_code>/delete', methods=['DELETE'])
def delete_url(short_code):
    """Delete a URL and its analytics"""
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()
    
    if not url_mapping:
        return jsonify({'success': False, 'error': 'URL not found'})
    
    db.session.delete(url_mapping)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'URL deleted'})

# API Endpoints
@app.route('/api/v1/urls', methods=['GET'])
def api_list_urls():
    """API endpoint to list all URLs"""
    urls = URLMapping.query.all()
    return jsonify([url.to_dict() for url in urls])

@app.route('/api/v1/shorten', methods=['POST'])
def api_shorten_url():
    """API endpoint to shorten URL"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    # Use the same logic as web form
    form_data = {
        'long_url': data['url'],
        'custom_alias': data.get('custom_alias'),
        'title': data.get('title'),
        'description': data.get('description')
    }
    
    # Create a mock form for validation
    class MockForm:
        def __init__(self, data):
            self.long_url = type('Field', (), {'data': data.get('long_url')})()
            self.custom_alias = type('Field', (), {'data': data.get('custom_alias')})()
            self.title = type('Field', (), {'data': data.get('title')})()
            self.description = type('Field', (), {'data': data.get('description')})()
            self.expires_in_days = type('Field', (), {'data': data.get('expires_in_days')})()
    
    mock_form = MockForm(form_data)
    
    # Reuse the existing shorten logic
    response = shorten_url()
    return response

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("🚀 Advanced URL Shortener Starting...")
    print("📍 Access the application at: http://localhost:5001")
    print("📊 Dashboard: http://localhost:5001/dashboard")
    app.run(debug=True, host='0.0.0.0', port=5001)