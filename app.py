from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
from datetime import datetime

app = Flask(__name__)

# Database configuration
database_url = os.environ.get('DATABASE_URL')

# If DATABASE_URL is not set, build it from individual components
if not database_url:
    db_host = os.environ.get('DB_HOST')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_name_mailmaster = os.environ.get('DB_NAME_MAILMASTER')
    db_port = os.environ.get('DB_PORT', '3306')  # Default MySQL port
    # Use DB_NAME_MAILMASTER as the primary database
    if db_host and db_user and db_password and db_name_mailmaster:
        # mysql+mysqlconnector://<user>:<password>@<host>:<port>/<dbname>
        database_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name_mailmaster}"
    else:
        raise RuntimeError("Database configuration missing. Either set DATABASE_URL or provide DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME_MAILMASTER environment variables.")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

db = SQLAlchemy(app)

# Database Models
class UnsubSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.String(100), unique=True, nullable=False)
    header_text = db.Column(db.Text, nullable=False)
    footer_text = db.Column(db.Text, nullable=False)
    yes_text = db.Column(db.String(100), nullable=False, default="YES")
    no_text = db.Column(db.String(100), nullable=False, default="NO")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
    
    # Look up campaign configuration
    campaign_config = None
    if campaign_id:
        campaign_config = UnsubSite.query.filter_by(campaign_id=campaign_id).first()
    
    # Check if subscription already exists for this email and campaign
    existing_subscription = Subscription.query.filter_by(
        email=email, 
        campaign_id=campaign_id
    ).first()
    
    if existing_subscription:
        # Show management page with campaign-specific text
        return render_template('simple_manage.html', 
                             subscription=existing_subscription,
                             campaign_config=campaign_config,
                             token=existing_subscription.token)
    
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
    
    # Show management page with campaign-specific text
    return render_template('simple_manage.html', 
                         subscription=subscription,
                         campaign_config=campaign_config,
                         token=token)

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
    choice = request.form.get('choice')  # For radio button form
    
    # Handle radio button choice
    if choice:
        if choice == 'no':
            subscription.is_subscribed = False
            message = "You have been successfully unsubscribed."
        elif choice == 'yes':
            subscription.is_subscribed = True
            message = "You have been successfully resubscribed."
        else:
            return render_template('error.html', message="Invalid choice.")
    # Handle original button form
    elif action:
        if action == 'unsubscribe':
            subscription.is_subscribed = False
            message = "You have been successfully unsubscribed."
        elif action == 'resubscribe':
            subscription.is_subscribed = True
            message = "You have been successfully resubscribed."
        else:
            return render_template('error.html', message="Invalid action.")
    else:
        return render_template('error.html', message="No action specified.")
    
    subscription.updated_at = datetime.utcnow()
    db.session.commit()
    
    return render_template('success.html', message=message)

# Initialize database on startup
with app.app_context():
    db.create_all()
    
    # Create default campaign if none exists
    if not UnsubSite.query.first():
        default_campaign = UnsubSite(
            campaign_id='default',
            header_text='Manage Your Email Subscription',
            footer_text='You can change your preference at any time.',
            yes_text='YES - Keep me subscribed',
            no_text='NO - Unsubscribe me'
        )
        db.session.add(default_campaign)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))