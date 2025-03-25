import os

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
EMAIL_HOST = "smtp.your-email.com"
EMAIL_PORT = 587
EMAIL_USER = "your-email@example.com"
EMAIL_PASSWORD = "your-email-password"
EXCHANGE_RATE_API_KEY = "your-exchange-rate-api-key"
SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY']
