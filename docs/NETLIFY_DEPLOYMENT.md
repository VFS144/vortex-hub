# Vortex Hub - Netlify Deployment Guide

## Overview

This guide covers the deployment setup for Vortex Hub to **Netlify** with the domain `vortex-frame-studio1-hub.netlify.app`.

Your project has been configured with:
- ✅ **FastAPI CORS** explicitly allowing your Netlify domain
- ✅ **Frontend API Configuration** with environment variable support
- ✅ **Root Package.json** with concurrent development scripts
- ✅ **Netlify Redirects** for proper client-side routing (SPA)

---

## 📋 Files Created/Updated

### 1. **Backend CORS Configuration** (`backend/app/main.py`)
**Status:** ✅ Updated

The CORS middleware now uses `settings.CORS_ORIGINS` from your configuration instead of allowing all origins (`["*"]`).

**Change:**
```python
# Before
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ❌ Too permissive
    ...
)

# After
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # ✅ Uses configured origins
    ...
)
```

### 2. **Environment Files**

#### `.env.production` (Root Directory)
**Status:** ✅ Created

Contains production-specific configuration:
- `ENVIRONMENT=production`
- `CORS_ORIGINS=["https://vortex-frame-studio1-hub.netlify.app"]`
- Production database URL
- Secured JWT secret (you need to generate one)
- Production logging level

**⚠️ TODO:** Update these fields before deploying:
```bash
# Generate a secure JWT secret:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update in .env.production:
JWT_SECRET=<your-generated-secret>
DATABASE_URL=<your-production-db-url>
VITE_API_URL=<your-backend-api-url>
```

#### `frontend/.env.production` (Frontend Directory)
**Status:** ✅ Created

Contains frontend build-time variables:
```
VITE_API_URL=http://localhost:8000  # Update with your backend URL
VITE_WS_URL=ws://localhost:8000     # Update with your backend WebSocket URL
```

#### `.env.example` (Root Directory)
**Status:** ✅ Updated

Updated to show the proper JSON format for `CORS_ORIGINS`.

### 3. **Root `package.json`**
**Status:** ✅ Created

Enables workspace management and concurrent development:

**Available Commands:**
```bash
# Install all dependencies (root + both workspaces)
npm run install:all

# Run both servers simultaneously during development
npm run dev

# Run individual servers
npm run dev:backend    # FastAPI on port 8000
npm run dev:frontend   # Vite on port 5173

# Build both projects
npm run build

# Test both projects
npm run test
```

**Prerequisite:** Install `concurrently` as a dev dependency (already in package.json).

### 4. **`netlify.toml` Configuration**
**Status:** ✅ Created

Handles client-side routing and production settings:

```toml
[build]
  command = "npm run build --workspace=frontend"
  publish = "frontend/dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200  # Ensures all routes go to your React app
```

**Key Features:**
- ✅ **Client-side routing:** All unmatched routes redirect to `index.html`
- ✅ **Security headers:** Includes X-Content-Type-Options, X-Frame-Options, etc.
- ✅ **Cache control:** Static assets cached for 1 year
- ✅ **Environment variables:** Different API URLs for production vs. development

---

## 🚀 Deployment Steps

### **Step 1: Set Up Backend API**

Your FastAPI backend needs to be deployed separately (Netlify only hosts frontend). Options:

1. **Heroku** (Deprecated - use alternatives)
2. **Render.com** - Free tier available, excellent for FastAPI
3. **Railway.app** - Affordable, easy deployment
4. **AWS EC2** - More control, higher cost
5. **DigitalOcean App Platform** - Good balance of price/features

**Create a Procfile in root:**
```
web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### **Step 2: Update Environment Variables**

Create a `.env.production` with your actual backend URL:

```bash
# .env.production
VITE_API_URL=https://your-backend-api-url.com
```

Update `frontend/.env.production`:
```bash
VITE_API_URL=https://your-backend-api-url.com
VITE_WS_URL=wss://your-backend-api-url.com
```

### **Step 3: Deploy Backend**

Deploy your FastAPI backend to your chosen platform:

```bash
# Example for Render.com
# 1. Create a new Web Service on Render
# 2. Connect your GitHub repo
# 3. Set runtime environment
# 4. Configure environment variables with values from .env.production
# 5. Deploy
```

**Important:** Update `CORS_ORIGINS` in backend to include your frontend URL:
```python
# .env.production
CORS_ORIGINS=["https://vortex-frame-studio1-hub.netlify.app"]
```

### **Step 4: Deploy Frontend to Netlify**

1. **Connect your GitHub repo:**
   ```
   https://github.com/your-username/vortex-hub
   ```

2. **Set build settings in Netlify dashboard:**
   - Build command: `npm run build --workspace=frontend`
   - Publish directory: `frontend/dist`

3. **Add environment variables in Netlify UI:**
   - Go to **Site settings** → **Build & deploy** → **Environment**
   - Add:
     ```
     VITE_API_URL = https://your-backend-api-url.com
     ```

4. **Deploy:**
   - Push to GitHub
   - Netlify auto-builds and deploys

### **Step 5: Verify CORS**

Test that your frontend can reach the backend:

```javascript
// In browser console
fetch('https://your-backend-api-url.com/health')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error('CORS Error:', err))
```

---

## 🛠️ Local Development

### **Option 1: Run Both Servers Simultaneously**

```bash
# Install all dependencies
npm run install:all

# Start both servers
npm run dev

# Backend will run on http://localhost:8000
# Frontend will run on http://localhost:5173
```

### **Option 2: Run Servers Separately**

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Security Checklist

- [ ] Update `JWT_SECRET` in `.env.production` to a secure random value
- [ ] Update `DATABASE_URL` to your production database
- [ ] Update `CORS_ORIGINS` to your exact Netlify domain (no `*`)
- [ ] Set `DEBUG=false` in production
- [ ] Use HTTPS for all production URLs
- [ ] Set strong database passwords
- [ ] Keep sensitive values out of version control (use `.env.production`, not `.env.production.example`)

---

## 📁 Updated Project Structure

```
vortex-hub/
├── .env.production              ✅ NEW - Production backend config
├── netlify.toml                 ✅ NEW - Netlify deployment config
├── package.json                 ✅ NEW - Root monorepo config
├── .env.example                 ✅ UPDATED - CORS format clarified
│
├── backend/
│   ├── app/
│   │   ├── main.py             ✅ UPDATED - CORS uses settings
│   │   └── core/config.py
│   └── requirements.txt
│
├── frontend/
│   ├── .env.production          ✅ NEW - Frontend production config
│   ├── src/
│   │   └── lib/api.ts           ✅ Uses VITE_API_URL env var
│   └── package.json
│
└── docs/
    └── ... (other docs)
```

---

## 🐛 Troubleshooting

### **CORS Errors in Console**

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
1. Check that your Netlify domain is in `CORS_ORIGINS` in `.env.production`
2. Ensure backend is restarted/redeployed after changing `.env`
3. Verify correct API URL in `frontend/.env.production`

### **Routes Return 404 Instead of Loading SPA**

**Error:** Direct navigation to `/projects` returns 404

**Solution:**
- Ensure `netlify.toml` has the redirect rule (it's already configured)
- Rebuild and redeploy to Netlify

### **API Requests Use Wrong URL**

**Problem:** Requests go to wrong backend URL

**Solution:**
1. Check `VITE_API_URL` environment variable
2. Verify it's set in Netlify dashboard under **Environment**
3. Clear browser cache and rebuild frontend

---

## 📚 Additional Resources

- [Netlify SPA Routing](https://docs.netlify.com/routing/overview/#syntax-for-the-redirects-file)
- [FastAPI CORS Docs](https://fastapi.tiangolo.com/tutorial/cors/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/settings/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)

---

## ✅ Checklist for Deployment

- [ ] Generate secure `JWT_SECRET`
- [ ] Update `.env.production` with production values
- [ ] Deploy backend to your chosen platform
- [ ] Get backend API URL from deployed platform
- [ ] Update `CORS_ORIGINS` in backend `.env.production`
- [ ] Update `VITE_API_URL` in frontend build environment
- [ ] Connect GitHub repo to Netlify
- [ ] Configure build settings in Netlify
- [ ] Set environment variables in Netlify dashboard
- [ ] Deploy frontend to Netlify
- [ ] Test CORS requests in browser console
- [ ] Test SPA routing by navigating directly to routes
- [ ] Test authentication flow end-to-end

---

**Questions?** Check the FastAPI docs, Netlify docs, or refer to your platform's deployment guides.
