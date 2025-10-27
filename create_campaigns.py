import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Script to create sample UnsubSite configurations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UnsubSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.String(100), unique=True, nullable=False)
    header_text = db.Column(db.Text, nullable=False)
    footer_text = db.Column(db.Text, nullable=False)
    yes_text = db.Column(db.String(100), nullable=False, default="YES")
    no_text = db.Column(db.String(100), nullable=False, default="NO")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_sample_campaigns():
    """Create sample campaign configurations"""
    with app.app_context():
        db.create_all()
        
        # Sample campaigns
        campaigns = [
            {
                'campaign_id': 'newsletter-2024',
                'header_text': 'Newsletter Subscription Preferences',
                'footer_text': 'Thank you for helping us improve our communications.',
                'yes_text': 'YES - Continue receiving our newsletter',
                'no_text': 'NO - Unsubscribe from newsletter'
            },
            {
                'campaign_id': 'promo-spring',
                'header_text': 'Spring Promotion Updates',
                'footer_text': 'We respect your privacy and preferences.',
                'yes_text': 'YES - Keep me updated on promotions',
                'no_text': 'NO - Remove me from promotional emails'
            },
            {
                'campaign_id': 'product-updates',
                'header_text': 'Product Update Notifications',
                'footer_text': 'You can modify these preferences anytime.',
                'yes_text': 'YES - Send me product updates',
                'no_text': 'NO - Stop product update emails'
            }
        ]
        
        for camp_data in campaigns:
            # Check if campaign already exists
            existing = UnsubSite.query.filter_by(campaign_id=camp_data['campaign_id']).first()
            if existing:
                print(f"Campaign {camp_data['campaign_id']} already exists, skipping...")
                continue
                
            campaign = UnsubSite(
                campaign_id=camp_data['campaign_id'],
                header_text=camp_data['header_text'],
                footer_text=camp_data['footer_text'],
                yes_text=camp_data['yes_text'],
                no_text=camp_data['no_text']
            )
            
            db.session.add(campaign)
            print(f"Created campaign: {camp_data['campaign_id']}")
        
        db.session.commit()
        print("Sample campaigns created successfully!")
        
        # Display sample URLs
        print("\nSample URLs to test:")
        for camp_data in campaigns:
            print(f"http://localhost:5000/subscribe?email=test@example.com&id={camp_data['campaign_id']}")

if __name__ == '__main__':
    create_sample_campaigns()