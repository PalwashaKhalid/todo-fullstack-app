# Deployment Checklist

## Pre-Deployment Setup

### 1. Database Setup (Neon)
- [ ] Create Neon account: https://neon.tech
- [ ] Create new project: `todo-app-production`
- [ ] Copy connection string (starts with `postgresql://`)
- [ ] Test connection: `psql <connection-string>`
- [ ] Enable connection pooling if needed

### 2. Environment Variables Preparation

**Backend Variables (copy these):**
```bash
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
JWT_SECRET_KEY=<generate-32-char-random-string>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
BETTER_AUTH_SECRET=<generate-32-char-random-string>
BETTER_AUTH_URL=https://your-app.vercel.app
CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
API_HOST=0.0.0.0
API_PORT=8000
```

**Frontend Variables (copy these):**
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
DATABASE_URL=<same-as-backend>
BETTER_AUTH_SECRET=<same-as-backend>
BETTER_AUTH_URL=https://your-app.vercel.app
```

**Generate secrets:**
```bash
# Generate JWT_SECRET_KEY
openssl rand -base64 32

# Generate BETTER_AUTH_SECRET
openssl rand -base64 32
```

---

## Frontend Deployment (Vercel)

### Step 1: Push Code to GitHub
- [x] Code pushed to repository
- [ ] Deployment files committed

### Step 2: Deploy to Vercel
1. [ ] Go to https://vercel.com
2. [ ] Click "Add New..." → "Project"
3. [ ] Import `PalwashaKhalid/todo-fullstack-app`
4. [ ] Configure:
   - Framework: Next.js (auto-detected)
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. [ ] Add environment variables (from preparation above)
6. [ ] Click "Deploy"
7. [ ] Wait for deployment to complete (~2-3 minutes)
8. [ ] Copy deployment URL (e.g., `https://todo-app-xyz.vercel.app`)

### Step 3: Verify Frontend
- [ ] Visit Vercel URL
- [ ] Check login page loads
- [ ] Check signup page loads
- [ ] Note: API calls will fail until backend is deployed

---

## Backend Deployment (Railway - Recommended)

### Step 1: Deploy to Railway
1. [ ] Go to https://railway.app
2. [ ] Sign in with GitHub
3. [ ] Click "New Project"
4. [ ] Select "Deploy from GitHub repo"
5. [ ] Choose `PalwashaKhalid/todo-fullstack-app`
6. [ ] Railway will detect the backend automatically

### Step 2: Configure Railway
1. [ ] Go to project settings
2. [ ] Set Root Directory: `backend`
3. [ ] Set Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. [ ] Add all environment variables (from preparation above)
5. [ ] Deploy

### Step 3: Get Backend URL
1. [ ] Go to Settings → Networking
2. [ ] Click "Generate Domain"
3. [ ] Copy the URL (e.g., `https://todo-backend-production.up.railway.app`)

### Step 4: Update Frontend Environment
1. [ ] Go back to Vercel project
2. [ ] Settings → Environment Variables
3. [ ] Update `NEXT_PUBLIC_API_URL` with Railway URL
4. [ ] Redeploy frontend (Deployments → Redeploy)

### Step 5: Update Backend CORS
1. [ ] Go to Railway project
2. [ ] Update `CORS_ORIGINS` environment variable
3. [ ] Add your Vercel URL: `https://your-app.vercel.app`
4. [ ] Redeploy backend

---

## Alternative: Backend Deployment (Render)

### Step 1: Deploy to Render
1. [ ] Go to https://render.com
2. [ ] Sign in with GitHub
3. [ ] Click "New +" → "Web Service"
4. [ ] Connect `PalwashaKhalid/todo-fullstack-app`
5. [ ] Configure:
   - Name: `todo-backend`
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

### Step 2: Add Environment Variables
- [ ] Add all backend environment variables
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (~5-10 minutes)

### Step 3: Follow Steps 3-5 from Railway section above

---

## Post-Deployment Testing

### 1. Test Backend Health
```bash
curl https://your-backend-url.com/health
# Expected: {"success":true,"status":"healthy","message":"API is operational"}
```

### 2. Test Frontend
- [ ] Visit your Vercel URL
- [ ] Sign up with test account
- [ ] Create a task
- [ ] Edit the task
- [ ] Toggle task completion
- [ ] Delete the task
- [ ] Sign out
- [ ] Sign in again

### 3. Test Authentication Flow
- [ ] Sign up creates account
- [ ] Sign in works with correct credentials
- [ ] Sign in fails with wrong credentials
- [ ] Dashboard redirects when not logged in
- [ ] Tasks are user-specific (create second account to verify)

### 4. Test API Endpoints
```bash
# Get auth token first
TOKEN="your-jwt-token"

# Test tasks endpoint
curl -H "Authorization: Bearer $TOKEN" https://your-backend-url.com/api/tasks/

# Test create task
curl -X POST https://your-backend-url.com/api/tasks/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Testing deployment"}'
```

---

## Troubleshooting

### Frontend Issues

**Build fails on Vercel:**
- [ ] Check build logs in Vercel dashboard
- [ ] Verify Node.js version (18+)
- [ ] Check all dependencies are in package.json
- [ ] Verify environment variables are set

**API calls return CORS errors:**
- [ ] Check CORS_ORIGINS in backend includes Vercel URL
- [ ] Verify NEXT_PUBLIC_API_URL is correct
- [ ] Check backend is running

**Authentication doesn't work:**
- [ ] Verify BETTER_AUTH_SECRET matches between frontend and backend
- [ ] Check DATABASE_URL is accessible from Vercel
- [ ] Verify JWT_SECRET_KEY is set in backend

### Backend Issues

**Deployment fails:**
- [ ] Check deployment logs
- [ ] Verify requirements.txt has all dependencies
- [ ] Check Python version (3.11+)
- [ ] Verify Dockerfile syntax

**Database connection fails:**
- [ ] Verify DATABASE_URL format
- [ ] Check Neon database is running
- [ ] Ensure SSL mode: `?sslmode=require`
- [ ] Test connection from deployment platform

**Health check fails:**
- [ ] Check `/health` endpoint returns 200
- [ ] Verify app is listening on correct port
- [ ] Check logs for startup errors

---

## Security Checklist

- [ ] All secrets are in environment variables (not in code)
- [ ] GitHub token has been revoked and regenerated
- [ ] JWT secrets are strong (32+ characters)
- [ ] BETTER_AUTH_SECRET matches between frontend and backend
- [ ] CORS is configured to only allow your frontend domain
- [ ] Database connection uses SSL (`?sslmode=require`)
- [ ] No .env files committed to git
- [ ] Production URLs use HTTPS

---

## Monitoring Setup

### Vercel
- [ ] Enable Analytics: Project → Analytics
- [ ] Set up error tracking
- [ ] Monitor function logs

### Railway/Render
- [ ] Check metrics dashboard
- [ ] Set up log retention
- [ ] Configure alerts for downtime

### Neon
- [ ] Monitor database usage
- [ ] Check query performance
- [ ] Set up usage alerts

---

## Optional: Custom Domain

### Vercel (Frontend)
1. [ ] Go to Project Settings → Domains
2. [ ] Add your domain (e.g., `todo.yourdomain.com`)
3. [ ] Configure DNS records as shown
4. [ ] Wait for SSL certificate (~5 minutes)

### Railway/Render (Backend)
1. [ ] Go to Settings → Custom Domain
2. [ ] Add your domain (e.g., `api.yourdomain.com`)
3. [ ] Configure DNS records
4. [ ] Update CORS_ORIGINS with new domain
5. [ ] Update NEXT_PUBLIC_API_URL in Vercel

---

## Rollback Plan

### If deployment fails:

**Frontend:**
1. [ ] Go to Vercel → Deployments
2. [ ] Find last working deployment
3. [ ] Click "..." → "Promote to Production"

**Backend:**
1. [ ] Go to Railway/Render → Deployments
2. [ ] Find last working deployment
3. [ ] Click "Rollback" or redeploy previous commit

---

## Success Criteria

- [ ] Frontend is accessible at Vercel URL
- [ ] Backend health check returns 200
- [ ] User can sign up and sign in
- [ ] User can create, read, update, delete tasks
- [ ] Tasks are isolated per user
- [ ] No CORS errors in browser console
- [ ] No authentication errors
- [ ] All environment variables are set correctly
- [ ] HTTPS is working on both frontend and backend

---

## Next Steps After Deployment

1. [ ] Share app URL with users
2. [ ] Monitor error logs for first 24 hours
3. [ ] Set up automated backups for database
4. [ ] Configure CI/CD for automatic deployments
5. [ ] Add monitoring and alerting
6. [ ] Consider adding rate limiting
7. [ ] Set up staging environment
8. [ ] Document API for other developers

---

## Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **Neon Docs**: https://neon.tech/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js Docs**: https://nextjs.org/docs

---

## Estimated Deployment Time

- Frontend (Vercel): 5-10 minutes
- Backend (Railway): 10-15 minutes
- Testing: 10-15 minutes
- **Total: 25-40 minutes**

---

## Cost Summary (Free Tiers)

- **Vercel**: Free (100 GB bandwidth/month)
- **Railway**: $5 free credit/month (~500 hours)
- **Render**: Free (750 hours/month, sleeps after 15 min)
- **Neon**: Free (0.5 GB storage, auto-suspend)
- **Total Monthly Cost**: $0 (within free tier limits)
