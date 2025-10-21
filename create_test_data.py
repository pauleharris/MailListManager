import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

# Simple script to create test subscription entries

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscriptions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from datetime import datetime


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    is_subscribed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def create_test_subscription(email):
    """Create a test subscription entry"""
    with app.app_context():
        db.create_all()
        
        # Generate a secure random token
        token = secrets.token_urlsafe(32)
        
        # Create subscription
        subscription = Subscription(
            email=email,
            token=token,
            is_subscribed=True
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        print(f"Created subscription for {email}")
        print(f"Management URL: http://localhost:5000/manage/{token}")
        return token

if __name__ == '__main__':
    # Create a test subscription
    test_email = "test@example.com"
    create_test_subscription(test_email)