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

1. Users receive a subscription link with a unique token: `/manage/<token>`
2. The page displays their current subscription status
3. Users can click OK (to maintain/resubscribe) or NO (to unsubscribe)
4. Changes are saved to the database and confirmation is displayed

## Database Schema

The application uses a simple SQLite database (upgradeable to PostgreSQL for Azure) with a `Subscription` table:

- `id`: Primary key
- `email`: User's email address
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

To create a subscription entry, you would typically:

1. Add a record to the database with an email and unique token
2. Send the user a link like: `https://yoursite.azurewebsites.net/manage/unique-token-here`
3. User clicks the link and can manage their subscription

This is a minimal, straightforward implementation focused on simplicity and Azure compatibility.