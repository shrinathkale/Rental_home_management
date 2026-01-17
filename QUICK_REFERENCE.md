# Quick Reference Guide - Security Setup

## 🚀 Quick Start (5 minutes)

### Step 1: Setup Environment File
```bash
# Copy template to .env
copy .env.example .env

# Or on Linux/Mac:
cp .env.example .env
```

### Step 2: Edit .env File
```bash
# Open .env and update with your values:
DEBUG=True
SECRET_KEY=your-key-here
DB_PASSWORD=your-password-here
EMAIL_HOST_PASSWORD=your-16-char-app-password
GOOGLE_MAPS_API_KEY=your-api-key-here
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Setup
```bash
python verify_env.py
```

### Step 5: Run Project
```bash
python manage.py runserver
```

---

## 📁 Important Files

| File | Purpose | Action |
|------|---------|--------|
| `.env` | Your local credentials | **NEVER commit to Git** ⚠️ |
| `.env.example` | Template for team | ✅ Commit to Git |
| `.gitignore` | Protect secrets | ✅ Commit to Git |
| `requirements.txt` | Python packages | ✅ Commit to Git |
| `myproject/settings.py` | Django config | ✅ Commit to Git |
| `verify_env.py` | Verification script | ✅ Commit to Git |

---

## 🔐 Environment Variables

### Django Settings
```env
DEBUG=True                          # False in production
SECRET_KEY=your-secret-key-here     # Keep it secret!
ALLOWED_HOSTS=localhost,127.0.0.1   # Add your domain
```

### Database (MySQL)
```env
DB_ENGINE=mysql.connector.django
DB_NAME=homes
DB_USER=root
DB_PASSWORD=your-strong-password
DB_HOST=localhost
DB_PORT=3306
```

### Email (Gmail)
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=16-character-app-password    # NOT regular password!
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Google Maps
```env
GOOGLE_MAPS_API_KEY=your-api-key-here
```

---

## ⚡ Common Commands

```bash
# Verify environment setup
python verify_env.py

# Create database tables
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Check for security issues
python manage.py check --deploy
```

---

## 📋 Team Collaboration

### For New Team Members:
```bash
# 1. Clone the repository
git clone <repo-url>

# 2. Copy environment template
copy .env.example .env

# 3. Get actual values from:
#    - Team lead via secure channel
#    - Password manager (if available)
#    - Setup meeting

# 4. Fill in .env with values
# (Ask team for: database password, email password, API key)

# 5. Install and verify
pip install -r requirements.txt
python verify_env.py

# 6. Run project
python manage.py runserver
```

---

## 🚀 Production Deployment

### On Render.com:
1. Go to Dashboard
2. Click Environment in your service
3. Add all variables from `.env` (one by one)
4. Set `DEBUG=False`
5. Use strong, unique `SECRET_KEY`
6. Deploy

### Environment Variables for Production:
```
DEBUG=False
SECRET_KEY=unique-strong-key-for-production
ALLOWED_HOSTS=your-domain.com,.onrender.com
DB_PASSWORD=strong-production-password
EMAIL_HOST_PASSWORD=production-email-password
GOOGLE_MAPS_API_KEY=production-api-key
```

---

## ✅ Checklist Before Committing

- [ ] `.env` is NOT in Git (check `.gitignore`)
- [ ] `.env.example` IS in Git (with placeholder values)
- [ ] `.gitignore` IS in Git (contains `.env`)
- [ ] `python-dotenv` is in `requirements.txt`
- [ ] `settings.py` uses `os.getenv()` for all secrets
- [ ] No hardcoded passwords in any file
- [ ] `python verify_env.py` passes all checks
- [ ] `python manage.py runserver` works without errors

---

## ❌ DO NOT

- ❌ Commit `.env` to Git
- ❌ Hardcode passwords in code
- ❌ Share `.env` file via email
- ❌ Use regular Gmail password (use App Password)
- ❌ Expose SECRET_KEY or API keys
- ❌ Push to production with `DEBUG=True`
- ❌ Use simple passwords
- ❌ Share credentials in chat or Slack

---

## ✅ DO

- ✅ Use `.env` for local development
- ✅ Share `.env.example` with team
- ✅ Use environment variables on production
- ✅ Keep `.env` in `.gitignore`
- ✅ Use Gmail App Passwords (16 characters)
- ✅ Rotate credentials regularly
- ✅ Use strong passwords (20+ characters)
- ✅ Share credentials via password manager
- ✅ Review Git history before pushing
- ✅ Run verification script regularly

---

## 📚 More Information

| Document | Content |
|----------|---------|
| [SECURITY_SETUP.md](SECURITY_SETUP.md) | Detailed setup guide |
| [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) | Complete checklist |
| [SECURITY_IMPLEMENTATION_SUMMARY.md](SECURITY_IMPLEMENTATION_SUMMARY.md) | What was done |
| [.env.example](.env.example) | Template file |

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: dotenv` | `pip install python-dotenv` |
| `.env` not loading | Ensure `.env` exists in project root |
| Database won't connect | Check DB_* variables in `.env` |
| Email not sending | Use 16-char Gmail App Password |
| Google Maps blank | Verify API key and enable Maps API |
| Settings won't load | Run `python verify_env.py` |

---

## 📞 Need Help?

1. Run verification script: `python verify_env.py`
2. Check log messages for specific issues
3. Review related documentation files
4. Verify `.env` file has all required variables
5. Ensure `requirements.txt` packages installed: `pip install -r requirements.txt`

---

**Last Updated**: January 17, 2026  
**Version**: 1.0  
**Status**: Ready to use
