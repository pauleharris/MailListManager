from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
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
    token = db.Column(db.String(255), unique=True, nullable=False)
    is_subscribed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

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

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))