# Email Subscription Management Website

A very simple Python Flask web application for managing email subscriptions (unsubscribe/resubscribe functionality) designed for Azure hosting.

## Features

- Simple web interface with OK/NO buttons for subscription management
- Accepts string parameters via URL for user identification
- Database integration for storing subscription data
- Responsive HTML design
- Azure-ready deployment configuration

## Project Structure

```
MailListManager/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── manage.html       # Subscription management page
│   ├── success.html      # Success confirmation page
│   └── error.html        # Error page
└── .github/
    └── copilot-instructions.md  # Development guidelines
```

## How It Works

### Option 1: Direct Token Access (Original)
1. Users receive a subscription link with a unique token: `/manage/<token>`
2. The page displays their current subscription status
3. Users can click OK (to maintain/resubscribe) or NO (to unsubscribe)
4. Changes are saved to the database and confirmation is displayed

### Option 2: Email and Campaign ID Access (New)
1. **Call the subscription URL with email and campaign ID parameters:**
   ```
   https://yoursite.azurewebsites.net/subscribe?email=user@example.com&id=campaign123
   ```
2. The system automatically creates a subscription record (if it doesn't exist)
3. User is redirected to the management page where they can unsubscribe/resubscribe
4. If the subscription already exists, user is taken directly to the management page

### URL Format for External Forms

To call this from another form or website, use this URL format:

```
https://yoursite.azurewebsites.net/subscribe?email=EMAIL_ADDRESS&id=CAMPAIGN_ID
```

**Parameters:**
- `email` (required): The user's email address
- `id` (optional): Campaign identifier (e.g., "newsletter-2024", "promo-spring", etc.)

**Examples:**
```bash
# Basic subscription without campaign
https://yoursite.azurewebsites.net/subscribe?email=john@example.com

# Subscription with campaign ID
https://yoursite.azurewebsites.net/subscribe?email=john@example.com&id=newsletter-2024

# Subscription with campaign for promotional email
https://yoursite.azurewebsites.net/subscribe?email=jane@example.com&id=promo-spring-2024
```

### HTML Form Example

You can use this HTML form to redirect users to the subscription manager:

```html
<form action="https://yoursite.azurewebsites.net/subscribe" method="GET">
    <input type="email" name="email" placeholder="Enter your email" required>
    <input type="hidden" name="id" value="your-campaign-id">
    <button type="submit">Manage Subscription</button>
</form>
```

## Database Schema

The application uses a simple SQLite database (upgradeable to PostgreSQL for Azure) with a `Subscription` table:

- `id`: Primary key
- `email`: User's email address
- `campaign_id`: Campaign identifier (optional)
- `token`: Unique token for subscription management
- `is_subscribed`: Boolean subscription status
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Access the application at `http://localhost:5000`

## Azure Deployment

This application is designed to be easily deployed to Azure App Service. The configuration includes:

- Gunicorn as the production WSGI server
- Environment variable support for database connections
- Port configuration for Azure hosting

## Environment Variables

- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SECRET_KEY`: Flask secret key for session management
- `PORT`: Port number (defaults to 5000)

## Usage Example

### Method 1: Direct URL with Email and Campaign ID

Simply construct a URL with the email and campaign ID:

```
https://yoursite.azurewebsites.net/subscribe?email=user@example.com&id=campaign123
```

When a user visits this URL:
1. If no subscription exists: Creates a new subscription and shows management page
2. If subscription exists: Shows existing subscription management page

### Method 2: Traditional Token Method

To create a subscription entry manually, you would:

1. Add a record to the database with an email, campaign ID, and unique token
2. Send the user a link like: `https://yoursite.azurewebsites.net/manage/unique-token-here`
3. User clicks the link and can manage their subscription

This is a minimal, straightforward implementation focused on simplicity and Azure compatibility.