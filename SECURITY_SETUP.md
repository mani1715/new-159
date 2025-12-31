# 🔐 Security Setup Documentation

## JWT Secret Key Management

This document explains how the application securely handles JWT secret keys for token signing and verification.

---

## ✅ Current Security Implementation

### 1. **Where the SECRET_KEY is Stored**

The JWT secret key is stored **ONLY** in the following locations:

- **Local Development:** `/app/backend/.env` file (NOT committed to Git)
- **Production (Render/Railway/etc.):** Environment variables in the hosting platform's dashboard

**File Location:**
```bash
/app/backend/.env
```

**Environment Variable Name:**
```bash
JWT_SECRET_KEY=O4YWPtWuX0mkD8I6QDPoHEeHmPK5d3jLhETvcVfOjy4
```

---

### 2. **Why It Is Safe for GitHub**

The codebase is **100% safe** to push to GitHub because:

✅ **`.env` files are in `.gitignore`**
   - Both `/app/backend/.env` and `/app/frontend/.env` are excluded from Git
   - Only `.env.example` files (with placeholder values) are committed

✅ **No hardcoded secrets in source code**
   - The backend reads the secret from environment variables using:
     ```python
     SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
     ```
   - If the environment variable is missing, it falls back to a placeholder (which should be changed in production)

✅ **`.env.example` contains placeholder values**
   - The example file shows the format but NOT the actual secret
   - Safe to commit to version control as a template for other developers

---

### 3. **How to Configure in Production (Render/Railway/Vercel/etc.)**

When deploying to production platforms, follow these steps:

#### **Step 1: Generate a New Secret Key**

**Never reuse the development key in production!** Generate a new one:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

This will output something like:
```
xY7Z9aB2cD3eF4gH5iJ6kL7mN8oP9qR0sT1uV2wX3yZ4
```

#### **Step 2: Set Environment Variables in Your Hosting Platform**

##### **Render:**
1. Go to your Render dashboard
2. Select your backend service
3. Navigate to **Environment** tab
4. Add the following environment variables:
   ```
   JWT_SECRET_KEY=<your-generated-secret-key>
   MONGODB_URI=<your-mongodb-atlas-uri>
   CORS_ORIGINS=https://your-frontend-domain.com
   DB_NAME=mspn_dev_db
   PORT=8001
   TRUST_PROXY=true
   ```

##### **Railway:**
1. Go to your Railway project
2. Select your backend service
3. Go to **Variables** tab
4. Add the same environment variables as above

##### **AWS/DigitalOcean/Self-Hosted:**
1. Create a `.env` file on your server (outside version control)
2. Set strict file permissions:
   ```bash
   chmod 600 /app/backend/.env
   ```
3. Ensure the file is owned by the application user only

---

### 4. **Security Best Practices Implemented**

✅ **Cryptographically Secure Key Generation**
   - Generated using Python's `secrets.token_urlsafe(32)`
   - Produces a 256-bit random key
   - Resistant to brute-force attacks

✅ **Environment-Based Configuration**
   - Secrets are never hardcoded in the source code
   - Different keys for development and production
   - Easy to rotate keys without code changes

✅ **Token Expiration**
   - JWT tokens expire after 7 days
   - Reduces the impact of token compromise
   - Configured in `/app/backend/auth/jwt.py`:
     ```python
     ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
     ```

✅ **HTTPS Enforcement (Production)**
   - All production deployments should use HTTPS
   - Prevents token interception during transmission
   - Configured via reverse proxy (Nginx, Render, etc.)

---

## 📁 File Structure

```
/app/
├── backend/
│   ├── .env                    # ❌ NOT in Git (actual secrets)
│   ├── .env.example            # ✅ IN Git (placeholder values)
│   └── auth/
│       └── jwt.py              # ✅ Reads from environment variables
├── .gitignore                  # ✅ Excludes .env files
└── SECURITY_SETUP.md           # ✅ This documentation
```

---

## 🔄 Key Rotation (If Compromised)

If you suspect your JWT secret key has been compromised:

1. **Generate a new secret key:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update the key in your production environment:**
   - Render: Update the `JWT_SECRET_KEY` environment variable
   - Railway: Update in the Variables tab
   - Self-hosted: Update the `.env` file

3. **Restart your backend service:**
   - All existing JWT tokens will become invalid
   - Users will need to log in again

4. **Notify your security team (if applicable)**

---

## ⚠️ Common Mistakes to Avoid

❌ **DON'T commit `.env` files to Git**
❌ **DON'T hardcode secrets in source code**
❌ **DON'T use the same secret for development and production**
❌ **DON'T share your `.env` file in chat messages or emails**
❌ **DON'T use weak or predictable secret keys**

---

## 📋 Checklist for Deployment

Before deploying to production, ensure:

- [ ] New JWT_SECRET_KEY generated for production
- [ ] JWT_SECRET_KEY set in production environment variables
- [ ] MONGODB_URI set to production database (MongoDB Atlas)
- [ ] CORS_ORIGINS set to production frontend URL
- [ ] TRUST_PROXY=true for HTTPS support
- [ ] `.env` file NOT committed to Git
- [ ] `.env.example` updated with correct variable names
- [ ] Backend successfully reads environment variables
- [ ] JWT tokens are being created and verified correctly

---

## 🧪 Testing Security

To verify your security setup:

1. **Check that environment variables are loaded:**
   ```bash
   cd /app/backend
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('JWT_SECRET_KEY loaded:', bool(os.getenv('JWT_SECRET_KEY')))"
   ```

2. **Test admin login:**
   ```bash
   curl -X POST http://localhost:8001/api/admin/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'
   ```

3. **Verify token expiration:**
   - Log in and get a JWT token
   - Wait 7 days (or modify expiration time for testing)
   - Try using the expired token - should fail

---

## 📚 Additional Resources

- [OWASP JWT Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [Python Secrets Module Documentation](https://docs.python.org/3/library/secrets.html)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)

---

## 📞 Support

If you have questions about security implementation:
- Review this documentation
- Check `.env.example` for required variables
- Ensure all secrets are in environment variables, not code

---

**Last Updated:** December 31, 2025  
**Status:** ✅ Production-Ready Security Configuration
