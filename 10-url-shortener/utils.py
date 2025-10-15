import validators
from urllib.parse import urlparse
from flask import request
import user_agents

def validate_url(url):
    """Enhanced URL validation"""
    if not url:
        return False, "URL cannot be empty"
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Validate URL format
    if not validators.url(url):
        return False, "Please enter a valid URL"
    
    # Additional security checks
    parsed = urlparse(url)
    if not parsed.netloc:  # No domain
        return False, "Please enter a valid domain"
    
    # Block potentially malicious URLs (basic check)
    suspicious_keywords = ['javascript:', 'data:', 'vbscript:']
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        return False, "URL contains suspicious content"
    
    return True, url

def get_client_info():
    """Extract client information from request"""
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip_address:
        ip_address = ip_address.split(',')[0].strip()
    
    user_agent_str = request.headers.get('User-Agent', '')
    ua = user_agents.parse(user_agent_str)
    
    return {
        'ip_address': ip_address,
        'user_agent': user_agent_str,
        'browser': ua.browser.family,
        'platform': ua.os.family,
        'device': ua.device.family,
        'referrer': request.headers.get('Referer')
    }

def generate_qr_code_url(short_url):
    """Generate QR code URL using external service"""
    import urllib.parse
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(short_url)}"
    return qr_url