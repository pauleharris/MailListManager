from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///subscriptions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

db = SQLAlchemy(app)

# Database Model
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    campaign_id = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    is_subscribed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe')
def subscribe_with_params():
    """Handle subscription with email and campaign_id from URL parameters"""
    email = request.args.get('email')
    campaign_id = request.args.get('id')  # Using 'id' as the parameter name for campaign
    
    if not email:
        return render_template('error.html', message="Email address is required.")
    
    # Check if subscription already exists for this email and campaign
    existing_subscription = Subscription.query.filter_by(
        email=email, 
        campaign_id=campaign_id
    ).first()
    
    if existing_subscription:
        # Redirect to existing subscription management
        return redirect(url_for('manage_subscription', token=existing_subscription.token))
    
    # Create new subscription
    token = secrets.token_urlsafe(32)
    subscription = Subscription(
        email=email,
        campaign_id=campaign_id,
        token=token,
        is_subscribed=True
    )
    
    db.session.add(subscription)
    db.session.commit()
    
    # Redirect to management page
    return redirect(url_for('manage_subscription', token=token))

@app.route('/manage/<token>')
def manage_subscription(token):
    subscription = Subscription.query.filter_by(token=token).first()
    if not subscription:
        return render_template('error.html', message="Invalid subscription link.")
    
    return render_template('manage.html', 
                         subscription=subscription, 
                         token=token)

@app.route('/update/<token>', methods=['POST'])
def update_subscription(token):
    subscription = Subscription.query.filter_by(token=token).first()
    if not subscription:
        return render_template('error.html', message="Invalid subscription link.")
    
    action = request.form.get('action')
    
    if action == 'unsubscribe':
        subscription.is_subscribed = False
        message = "You have been successfully unsubscribed."
    elif action == 'resubscribe':
        subscription.is_subscribed = True
        message = "You have been successfully resubscribed."
    else:
        return render_template('error.html', message="Invalid action.")
    
    subscription.updated_at = datetime.utcnow()
    db.session.commit()
    
    return render_template('success.html', message=message)

# Initialize database on startup
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))