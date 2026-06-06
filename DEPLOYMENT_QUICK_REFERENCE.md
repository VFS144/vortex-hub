# Vortex Hub - Deployment Quick Reference

## 🎯 Quick Start - Local Development

```bash
# Install everything at once
npm run install:all

# Run both servers simultaneously
npm run dev

# Frontend: http://localhost:5173
# Backend: http://localhost:8000
```

---

## 📤 Deploy Frontend to Netlify

### Prerequisites
- GitHub repo connected to Netlify
- Backend API deployed and running

### Environment Variables for Netlify Dashboard
```
VITE_API_URL = https://your-backend-url.com
```

### Build Configuration
- **Build command:** `npm run build --workspace=frontend`
- **Publish directory:** `frontend/dist`

### Deploy
```bash
git push origin main  # Netlify auto-deploys
```

---

## 📤 Deploy Backend (Example: Render.com)

### 1. Environment Variables to Set
```
ENVIRONMENT=production
DATABASE_URL=postgresql://...
JWT_SECRET=<secure-random-key>
CORS_ORIGINS=["https://vortex-frame-studio1-hub.netlify.app"]
VITE_API_URL=<your-backend-url>
DEBUG=false
```

### 2. Procfile (Create in root `backend/` folder)
```
web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 3. Deploy
- Connect GitHub repo to Render.com
- Set environment variables
- Deploy

---

## 🔧 Update Backend Dynamically

If you change `CORS_ORIGINS` in `.env.production`:

```bash
cd backend
# Rebuild and test locally
python -m uvicorn app.main:app --reload --port 8000

# Then push changes
git add .env.production
git commit -m "Update CORS origins for production"
git push origin main
```

---

## 🧪 Test CORS Before Deploying

### In Browser Console (on your Netlify domain)
```javascript
fetch('https://your-backend-url.com/health')
  .then(res => res.json())
  .then(data => console.log('✅ CORS Works:', data))
  .catch(err => console.error('❌ CORS Error:', err))
```

### Expected Response
```json
{
  "message": "OK",
  "status": "healthy"
}
```

---

## 🚨 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `CORS Error` | Backend doesn't allow Netlify domain | Update `CORS_ORIGINS` in `.env.production` |
| Routes return 404 | SPA routing not configured | Check `netlify.toml` redirect rule exists |
| API requests fail | Wrong `VITE_API_URL` | Update in Netlify dashboard environment |
| Can't login | JWT secret mismatch | Ensure same `JWT_SECRET` in `.env.production` |

---

## 📝 Environment Variable Reference

### Frontend (`frontend/.env.production`)
```bash
VITE_API_URL=https://your-backend-url.com    # Backend API base URL
VITE_WS_URL=wss://your-backend-url.com       # WebSocket URL (if used)
```

### Backend (`.env.production`)
```bash
ENVIRONMENT=production
CORS_ORIGINS=["https://vortex-frame-studio1-hub.netlify.app"]
DATABASE_URL=postgresql://...
JWT_SECRET=<generate-with>: python -c "import secrets; print(secrets.token_urlsafe(32))"
DEBUG=false
```

---

## 🔐 Security Reminders

- ✅ Never commit `.env` files with secrets to GitHub
- ✅ Generate new `JWT_SECRET` for production: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- ✅ Use HTTPS for all production URLs
- ✅ Set `CORS_ORIGINS` to your exact domain (not `["*"]`)
- ✅ Set `DEBUG=false` in production

---

## 📊 Deployment Status Checklist

| Component | Status | URL |
|-----------|--------|-----|
| Frontend | [ ] Deployed | `https://vortex-frame-studio1-hub.netlify.app` |
| Backend | [ ] Deployed | `https://your-backend-url.com` |
| Database | [ ] Configured | - |
| CORS | [ ] Verified | - |
| Auth | [ ] Tested | - |

---

## 🆘 Getting Help

1. **CORS Issues:** Check FastAPI CORS documentation
2. **Netlify Issues:** Check Netlify deployment logs
3. **Backend Deployment:** See your platform's docs (Render, Railway, etc.)
4. **Environment Variables:** Use `ENVIRONMENT=production` with specific URLs

---

**Last Updated:** 2026-06-03
**Project:** Vortex Hub
**Netlify Domain:** vortex-frame-studio1-hub.netlify.app
