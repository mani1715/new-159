# 🚀 Quick Guide: Push Updated Code to GitHub

## Files That Were Updated/Created

### Core Fixes (Must Update):
1. ✅ `frontend/src/services/api.js` - **CRITICAL FIX**
   - Increased timeout from 15s to 60s
   - Added retry logic

### New Utilities (Recommended to Add):
2. ✅ `frontend/src/utils/healthCheck.js` - NEW FILE
3. ✅ `scripts/wake_up_backend.sh` - NEW FILE
4. ✅ `RENDER_TROUBLESHOOTING.md` - NEW FILE
5. ✅ `DEPLOYMENT_ERRORS_FIXED.md` - NEW FILE

---

## Method 1: Push from This Environment (If you have Git configured)

```bash
cd /app

# Check git status
git status

# Add all changes
git add frontend/src/services/api.js
git add frontend/src/utils/healthCheck.js
git add scripts/wake_up_backend.sh
git add RENDER_TROUBLESHOOTING.md
git add DEPLOYMENT_ERRORS_FIXED.md

# Commit
git commit -m "Fix: Resolve API timeout errors on Render deployment

- Increase API timeout from 15s to 60s for production (handles Render cold starts)
- Add retry logic for failed GET requests (max 2 retries)
- Create health check utility for backend availability monitoring
- Add wake-up script for sleeping backend
- Comprehensive troubleshooting documentation

Fixes #issue-number (if you have an issue)"

# Push to GitHub
git push origin main
```

---

## Method 2: Manual GitHub Web Interface

Since the GitHub repository was cloned to `/app/github_new_159`, you need to copy files:

### Step 1: Copy Updated Files
```bash
# From this environment, copy updated files
cp -r /app/frontend/* /app/github_new_159/frontend/
cp -r /app/scripts/* /app/github_new_159/scripts/
cp /app/RENDER_TROUBLESHOOTING.md /app/github_new_159/
cp /app/DEPLOYMENT_ERRORS_FIXED.md /app/github_new_159/
```

### Step 2: Push from github_new_159
```bash
cd /app/github_new_159

git add .
git commit -m "Fix: Resolve API timeout errors on Render deployment"
git push origin main
```

---

## Method 3: Download and Upload Manually

1. **Download these files from this workspace:**
   - `frontend/src/services/api.js`
   - `frontend/src/utils/healthCheck.js`
   - `scripts/wake_up_backend.sh`
   - `RENDER_TROUBLESHOOTING.md`
   - `DEPLOYMENT_ERRORS_FIXED.md`

2. **Go to https://github.com/mani1715/new-159**

3. **For existing files (like api.js):**
   - Navigate to the file
   - Click "Edit" (pencil icon)
   - Replace content
   - Commit changes

4. **For new files:**
   - Navigate to the directory
   - Click "Add file" → "Create new file"
   - Paste content
   - Commit changes

---

## After Pushing to GitHub

### Frontend (Vercel) - Will Auto-Deploy
If you have auto-deploy enabled on Vercel:
1. Vercel will automatically detect the push
2. Build and deploy new version
3. Wait 1-2 minutes
4. Check deployment logs on Vercel dashboard

If auto-deploy is not enabled:
1. Go to Vercel dashboard
2. Your project → Deployments
3. Click "Redeploy"

### Backend (Render) - No Changes Needed
No backend code was modified, so no need to redeploy backend.

---

## Verification After Push

### 1. Check Vercel Deployment
```
https://vercel.com/your-username/new-159
```
Look for:
- ✅ Build completed successfully
- ✅ No build errors

### 2. Test Your Website
Open your deployed site (e.g., https://new-159.vercel.app)

**Expected behavior:**
- First load might take 30-50 seconds (Render waking up)
- Console shows: `🔗 API Base URL: https://mspn-dev.onrender.com/api`
- After initial load, page works fine
- Refresh is fast

### 3. Check Browser Console (F12)
Should see:
```
🔗 API Base URL: https://mspn-dev.onrender.com/api
[API Request] GET https://mspn-dev.onrender.com/api/content/
```

If first request times out:
```
🔄 Retrying request (1/2)...
```

---

## Git Commands Cheat Sheet

```bash
# Check current branch
git branch

# See what files changed
git status

# View specific changes in a file
git diff frontend/src/services/api.js

# Add specific files
git add frontend/src/services/api.js

# Add all changes
git add .

# Commit with message
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest changes (if needed)
git pull origin main

# Check remote URL
git remote -v

# View commit history
git log --oneline -5
```

---

## Important Notes

### ⚠️ Don't Forget:
- ✅ Make sure you're on the correct branch (`main` or `master`)
- ✅ Pull latest changes before pushing if working with others
- ✅ Test locally before pushing (you've already done this ✅)
- ✅ Check Vercel deployment logs after push

### 🎯 Key File to Update:
**MOST IMPORTANT:** `frontend/src/services/api.js`
This file contains the timeout and retry logic fixes.

### 📝 Good Commit Message Template:
```
Fix: Brief description of what was fixed

- Bullet point 1
- Bullet point 2
- Bullet point 3

Fixes: #issue-number (optional)
```

---

## Troubleshooting Push Issues

### Error: "fatal: not a git repository"
```bash
cd /app/github_new_159  # Make sure you're in the cloned repo
git status
```

### Error: "Permission denied (publickey)"
You need to set up SSH keys or use HTTPS with token:
```bash
git remote set-url origin https://github.com/mani1715/new-159.git
git push origin main
# Enter your GitHub username and personal access token
```

### Error: "Updates were rejected"
Pull latest changes first:
```bash
git pull origin main --rebase
git push origin main
```

---

## Need Help?

If you encounter issues:
1. Check error messages carefully
2. Make sure you're in the right directory
3. Verify you have push access to the repository
4. Try using GitHub's web interface as an alternative

---

**Ready to push?** Choose the method that works best for you and follow the steps above!
