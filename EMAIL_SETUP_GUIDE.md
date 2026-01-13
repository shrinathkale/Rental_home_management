# Email Configuration Guide for Password Reset

## Issues Fixed

### 1. **TemplateSyntaxError - json_script tag** ✅
   - **Problem**: The `{% load json_script %}` tag at line 90 of `property_detail.html` was causing a TemplateSyntaxError
   - **Solution**: Removed the unnecessary tag - it's not needed for displaying amenities
   - **Result**: Property detail page now loads without errors

### 2. **Search Form UI Update** ✅
   - **Problem**: Search and Clear buttons were on different lines with inconsistent styling
   - **Solution**: 
     - Moved both buttons to the same line (col-md-1)
     - Changed Clear button color from secondary to primary (same blue as Search)
     - Used flexbox with gap for proper alignment
     - Adjusted column widths for better layout (4-4-3-1)
   - **Result**: Buttons now appear side-by-side with matching colors and proper spacing

### 3. **Email Configuration for Password Reset** ⚙️

## Setup Instructions

### Option A: Using Gmail SMTP (Recommended)

1. **Enable 2-Factor Authentication on your Gmail Account:**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Google will generate a 16-character password
   - Copy this password

3. **Update `settings.py`:**
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your_email@gmail.com'  # Your Gmail address
   EMAIL_HOST_PASSWORD = 'your_16_char_app_password'  # Paste the generated password here
   DEFAULT_FROM_EMAIL = 'your_email@gmail.com'
   ```

### Option B: Using Console Backend (Testing Only)

For development/testing without actually sending emails:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Emails will be printed to your Django console instead of being sent.

### Option C: Using Other Email Providers

**SendGrid:**
```python
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'your_sendgrid_api_key'
```

**AWS SES:**
```python
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
```

## Testing the Email Configuration

1. **Test with Console Backend first:**
   - Update settings to use console backend
   - Try the password reset form
   - Check Django console for the reset email content

2. **Test with Gmail:**
   - Update settings with your Gmail credentials
   - Try the password reset form
   - Check your Gmail inbox (and spam folder)

## Troubleshooting

### Email Not Sending?

1. **Check your email configuration in `settings.py`:**
   - Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct
   - Gmail requires "Less secure app" enabled OR App Passwords (recommended)

2. **Check Django logs:**
   ```
   python manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail('Test', 'This is a test', 'your_email@gmail.com', ['recipient@example.com'])
   ```

3. **Common Issues:**
   - Using regular Gmail password instead of App Password → Use App Password
   - 2FA not enabled → Enable it first
   - Firewall/Network blocking SMTP → Check port 587 access
   - EMAIL_HOST_USER/PASSWORD typo → Double-check credentials

### Gmail Specific Issues

- **"Less secure app" required:** Modern Gmail requires either:
  - App Passwords (recommended), or
  - Enable "Less secure apps" in Gmail settings (not recommended)

- **502 Bad Gateway:** Usually a network/firewall issue. Contact your IT team.

## Features Implemented

✅ Password reset email sending with:
  - Unique token generation for security
  - Clickable reset link
  - User-friendly message in email
  - Error handling with user feedback
  - Security: Don't reveal if email exists in system

## Security Notes

1. **Never commit credentials** to version control
2. Use environment variables for sensitive data in production:
   ```python
   import os
   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
   ```

3. The email contains a secure token that expires in 24 hours
4. Tokens cannot be reused for security purposes

---

For more information, refer to [Django Email Documentation](https://docs.djangoproject.com/en/4.2/topics/email/)
