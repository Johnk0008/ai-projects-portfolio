from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import string
import random
import hashlib

db = SQLAlchemy()

class URLMapping(db.Model):
    __tablename__ = 'url_mappings'
    
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2000), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    custom_alias = db.Column(db.String(50), unique=True, nullable=True)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    total_clicks = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    clicks = db.relationship('URLClick', backref='url_mapping', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, long_url, custom_alias=None, title=None, description=None, expires_in_days=None):
        self.long_url = long_url
        self.custom_alias = custom_alias
        self.title = title
        self.description = description
        
        if custom_alias:
            self.short_code = custom_alias
        else:
            self.short_code = self.generate_short_code()
            
        if expires_in_days:
            self.expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    def generate_short_code(self, length=6):
        """Generate a unique short code"""
        characters = string.ascii_letters + string.digits
        attempts = 0
        while attempts < 10:  # Prevent infinite loop
            code = ''.join(random.choices(characters, k=length))
            if not URLMapping.query.filter_by(short_code=code).first():
                return code
            attempts += 1
        # Fallback: use hash-based approach
        hash_input = f"{self.long_url}{datetime.utcnow().timestamp()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:length]
    
    def is_expired(self):
        return self.expires_at and datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'long_url': self.long_url,
            'short_code': self.short_code,
            'custom_alias': self.custom_alias,
            'title': self.title,
            'description': self.description,
            'short_url': f'/r/{self.short_code}',
            'full_short_url': f'http://localhost:5000/r/{self.short_code}',
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'total_clicks': self.total_clicks,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'is_expired': self.is_expired()
        }
    
    def get_analytics(self, days=30):
        """Get analytics data for this URL"""
        from datetime import datetime, timedelta
        start_date = datetime.utcnow() - timedelta(days=days)
        
        clicks = URLClick.query.filter(
            URLClick.url_id == self.id,
            URLClick.clicked_at >= start_date
        ).all()
        
        # Group by date
        daily_clicks = {}
        for click in clicks:
            date_str = click.clicked_at.strftime('%Y-%m-%d')
            daily_clicks[date_str] = daily_clicks.get(date_str, 0) + 1
        
        return {
            'total_clicks': len(clicks),
            'daily_clicks': daily_clicks,
            'referrers': {},
            'browsers': {},
            'platforms': {}
        }

class URLClick(db.Model):
    __tablename__ = 'url_clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('url_mappings.id'), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    referrer = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(100), nullable=True)
    browser = db.Column(db.String(100), nullable=True)
    platform = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'clicked_at': self.clicked_at.isoformat(),
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'country': self.country,
            'browser': self.browser,
            'platform': self.platform
        }