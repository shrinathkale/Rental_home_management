# Security Configuration Setup Guide

## Overview
This guide explains the security configuration that has been implemented for your Django project using environment variables and `.env` files.

## What Has Been Changed

### 1. **Created `.env` File**
   - **Location**: Root directory of the project
   - **Purpose**: Stores all sensitive information like database credentials, API keys, and email passwords
   - **Contains**:
     - Django SECRET_KEY
     - Database connection details
     - Email credentials
     - Google Maps API key

### 2. **Created `.gitignore` File**
   - **Excludes** `.env` and other sensitive files from Git repository
   - **Protects** your credentials from being accidentally committed to version control
   - **Also excludes**:
     - Python cache files (`__pycache__/`, `*.pyc`)
     - Virtual environment (`venv/`)
     - Database files (`db.sqlite3`)
     - IDE settings (`.vscode/`, `.idea/`)
     - Media and temporary files

### 3. **Updated `requirements.txt`**
   - **Added**: `python-dotenv==1.0.0`
   - **Purpose**: Enables loading environment variables from `.env` file

### 4. **Updated `myproject/settings.py`**
   - **Imports**: Added `os` and `from dotenv import load_dotenv`
   - **Loads** environment variables from `.env` file at startup
   - **Replaced** all hardcoded sensitive values with environment variable calls:
     - `SECRET_KEY = os.getenv('SECRET_KEY', ...)`
     - `DEBUG = os.getenv('DEBUG', 'True') == 'True'`
     - `ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', ...).split(',')`
     - Database configuration uses `os.getenv()` for all parameters
     - Email configuration uses `os.getenv()` for all credentials
     - `GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')`

### 5. **Updated `myapp/views.py`**
   - Added `GOOGLE_MAPS_API_KEY` context to all template views
   - Ensures API key is available in templates dynamically

### 6. **Created `.env.example` File**
   - **Purpose**: Template showing what environment variables are needed
   - **For new developers**: Copy this file to `.env` and fill in actual values
   - **Should be committed** to version control (unlike `.env`)

## Setup Instructions

### For First-Time Setup

1. **Copy the example environment file**:
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` file** with your actual values:
   ```
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-actual-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com
   
   # Database Configuration
   DB_ENGINE=mysql.connector.django
   DB_NAME=homes
   DB_USER=root
   DB_PASSWORD=your-database-password
   DB_HOST=localhost
   DB_PORT=3306
   
   # Email Configuration
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-character-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   DEFAULT_FROM_EMAIL_NAME=rental_home
   
   # Google Maps API Key
   GOOGLE_MAPS_API_KEY=your-google-maps-api-key
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the setup**:
   ```bash
   python manage.py runserver
   ```

### For Deployment

1. **Do NOT include `.env` in your Git repository**
2. **Set environment variables** on your deployment platform:
   - Render.com: Set in Dashboard → Environment variables
   - Heroku: Set using `heroku config:set KEY=VALUE`
   - Other platforms: Refer to their environment variables documentation

3. **Alternative**: Upload `.env` file to your server (not recommended for security)

## Important Security Notes

### ✅ DO:
- ✓ Keep `.env` file locally and NEVER commit it
- ✓ Use strong database passwords
- ✓ Use Gmail App Passwords (not regular passwords)
- ✓ Rotate API keys regularly
- ✓ Share `.env.example` with team, NOT `.env`
- ✓ Set `DEBUG=False` in production
- ✓ Use unique SECRET_KEY for production

### ❌ DON'T:
- ✗ Commit `.env` file to Git
- ✗ Share `.env` file via email or chat
- ✗ Use simple passwords for database
- ✗ Use your actual Gmail password (use App Password)
- ✗ Push API keys to public repositories
- ✗ Set `DEBUG=True` in production
- ✗ Share your SECRET_KEY with anyone

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| DEBUG | Enable debug mode (False in production) | True |
| SECRET_KEY | Django secret key for CSRF protection | django-insecure-... |
| ALLOWED_HOSTS | Allowed hostnames | localhost,127.0.0.1 |
| DB_ENGINE | Database engine | mysql.connector.django |
| DB_NAME | Database name | homes |
| DB_USER | Database username | root |
| DB_PASSWORD | Database password | strong_password_123 |
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 3306 |
| EMAIL_BACKEND | Email backend | django.core.mail.backends.smtp.EmailBackend |
| EMAIL_HOST | SMTP host | smtp.gmail.com |
| EMAIL_PORT | SMTP port | 587 |
| EMAIL_USE_TLS | Use TLS for email | True |
| EMAIL_HOST_USER | Email username | your-email@gmail.com |
| EMAIL_HOST_PASSWORD | Email password (16-char app password) | app_password_16_char |
| DEFAULT_FROM_EMAIL | Default sender email | your-email@gmail.com |
| DEFAULT_FROM_EMAIL_NAME | Email sender name | rental_home |
| GOOGLE_MAPS_API_KEY | Google Maps API key | AIza... |

## Troubleshooting

### Issue: "Settings not loading"
**Solution**: Ensure `.env` file exists in the project root and `python-dotenv` is installed:
```bash
pip install python-dotenv
```

### Issue: "Database connection failed"
**Solution**: Check `.env` file has correct database credentials:
```bash
# Verify database credentials
# Test connection manually if needed
```

### Issue: "Email not sending"
**Solution**: Ensure you're using Gmail App Password, not regular password:
1. Enable 2FA on your Gmail account
2. Generate 16-character App Password from https://myaccount.google.com/apppasswords
3. Use this App Password in `EMAIL_HOST_PASSWORD`

### Issue: "Google Maps API not loading"
**Solution**: Verify API key is set in `.env` and enabled on Google Cloud Console:
1. Enable Maps JavaScript API
2. Add website domain to API restrictions
3. Copy the API key to `GOOGLE_MAPS_API_KEY` in `.env`

## Next Steps

1. **Distribute `.env.example`** to team members
2. **Each developer** creates their own `.env` from `.env.example`
3. **For production**: Set environment variables on deployment platform
4. **Regularly rotate** sensitive credentials
5. **Monitor** access to `.env` file

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/en/4.2/ref/settings/
- python-dotenv: https://github.com/thenv0/python-dotenv
- Gmail App Passwords: https://support.google.com/accounts/answer/185833
- Google Cloud Console: https://console.cloud.google.com/

---
**Last Updated**: January 17, 2026
