from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL, Optional, Length, NumberRange
import validators

class URLShortenForm(FlaskForm):
    long_url = StringField('Long URL', validators=[
        DataRequired(message='URL is required'),
        URL(message='Please enter a valid URL (include http:// or https://)')
    ])
    custom_alias = StringField('Custom Alias (optional)', validators=[
        Optional(),
        Length(min=3, max=20, message='Custom alias must be between 3 and 20 characters'),
        # Regex validator for alphanumeric and hyphens
    ])
    title = StringField('Title (optional)', validators=[
        Optional(),
        Length(max=200, message='Title must be less than 200 characters')
    ])
    description = TextAreaField('Description (optional)', validators=[
        Optional(),
        Length(max=500, message='Description must be less than 500 characters')
    ])
    expires_in_days = SelectField('Expires After (optional)', choices=[
        ('', 'Never expire'),
        ('1', '1 day'),
        ('7', '7 days'),
        ('30', '30 days'),
        ('90', '90 days')
    ], validators=[Optional()])

class URLAnalyticsForm(FlaskForm):
    days = SelectField('Analytics Period', choices=[
        ('7', 'Last 7 days'),
        ('30', 'Last 30 days'),
        ('90', 'Last 90 days'),
        ('365', 'Last year')
    ], default='30')