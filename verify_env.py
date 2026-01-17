#!/usr/bin/env python
"""
Environment Setup Verification Script
This script verifies that all required environment variables are properly configured.
Usage: python verify_env.py
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists"""
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file found")
        return True
    else:
        print("❌ .env file NOT found")
        print("   Create it by copying: cp .env.example .env")
        return False

def check_dotenv_installed():
    """Check if python-dotenv is installed"""
    try:
        import dotenv
        print("✅ python-dotenv package installed")
        return True
    except ImportError:
        print("❌ python-dotenv package NOT installed")
        print("   Install it with: pip install python-dotenv")
        return False

def check_env_variables():
    """Check if all required environment variables are set"""
    from dotenv import load_dotenv
    
    load_dotenv()
    
    required_vars = {
        'Django': ['DEBUG', 'SECRET_KEY', 'ALLOWED_HOSTS'],
        'Database': ['DB_ENGINE', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT'],
        'Email': ['EMAIL_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS', 
                  'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL'],
        'APIs': ['GOOGLE_MAPS_API_KEY']
    }
    
    all_set = True
    
    for category, variables in required_vars.items():
        print(f"\n{category} Configuration:")
        for var in variables:
            value = os.getenv(var)
            if value:
                # Don't print sensitive values
                if 'PASSWORD' in var or 'KEY' in var:
                    print(f"  ✅ {var}: ****{'*' * len(value[2:])}")
                else:
                    print(f"  ✅ {var}: {value}")
            else:
                print(f"  ⚠️  {var}: NOT SET (using default)")
                all_set = False
    
    return all_set

def check_django_settings():
    """Check if Django settings loads properly"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
        import django
        django.setup()
        print("\n✅ Django settings loaded successfully")
        return True
    except Exception as e:
        print(f"\n❌ Error loading Django settings: {e}")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Environment Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python-dotenv Installation", check_dotenv_installed),
        (".env File Existence", check_env_file),
        ("Environment Variables", check_env_variables),
        ("Django Settings", check_django_settings),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n🔍 Checking: {check_name}")
        print("-" * 60)
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error during check: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your environment is properly configured.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
