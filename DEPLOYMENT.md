# Deployment Guide

## Frontend Deployment (Vercel)

### Option 1: Deploy via Vercel Web UI (Recommended)

1. **Go to Vercel**: https://vercel.com
2. **Sign in** with your GitHub account
3. **Import Project**:
   - Click "Add New..." → "Project"
   - Select your repository: `PalwashaKhalid/todo-fullstack-app`
   - Vercel will auto-detect Next.js

4. **Configure Project**:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

5. **Environment Variables** (Add these in Vercel dashboard):
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   DATABASE_URL=your-neon-database-url
   BETTER_AUTH_SECRET=your-secret-key-min-32-chars
   BETTER_AUTH_URL=https://your-vercel-app.vercel.app
   ```

6. **Deploy**: Click "Deploy"

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from frontend directory
cd frontend
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: todo-fullstack-app
# - Directory: ./
# - Override settings? No

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL
vercel env add DATABASE_URL
vercel env add BETTER_AUTH_SECRET
vercel env add BETTER_AUTH_URL

# Deploy to production
vercel --prod
```

---

## Backend Deployment

### ⚠️ Important Note
Hugging Face Spaces is designed for ML models, not traditional APIs. For FastAPI backends, consider these better alternatives:

**Recommended Options:**
1. **Railway** (easiest, free tier available)
2. **Render** (free tier available)
3. **Fly.io** (free tier available)
4. **AWS/GCP/Azure** (production-grade)

### Option A: Deploy to Railway (Recommended)

1. **Go to Railway**: https://railway.app
2. **Sign in** with GitHub
3. **New Project** → "Deploy from GitHub repo"
4. **Select** your repository
5. **Configure**:
   - Root Directory: `backend`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

6. **Environment Variables**:
   ```
   DATABASE_URL=your-neon-database-url
   JWT_SECRET_KEY=your-secret-key-min-32-chars
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_MINUTES=30
   BETTER_AUTH_SECRET=same-as-frontend
   BETTER_AUTH_URL=https://your-vercel-app.vercel.app
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

7. **Deploy**: Railway will auto-deploy

### Option B: Deploy to Render

1. **Go to Render**: https://render.com
2. **Sign in** with GitHub
3. **New** → "Web Service"
4. **Connect** your repository
5. **Configure**:
   - Name: `todo-backend`
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

6. **Environment Variables**: (Same as Railway above)

7. **Deploy**: Click "Create Web Service"

### Option C: Deploy to Hugging Face Spaces (Not Recommended for APIs)

If you still want to use Hugging Face:

1. **Create Space**: https://huggingface.co/spaces
2. **New Space**:
   - Name: `todo-backend`
   - SDK: Docker
   - Visibility: Public or Private

3. **Create Dockerfile** in backend directory:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 7860

   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
   ```

4. **Push to Hugging Face**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-backend
   cd todo-backend
   cp -r /path/to/backend/* .
   git add .
   git commit -m "Initial backend deployment"
   git push
   ```

5. **Configure Secrets** in Space settings (same environment variables as above)

---

## Post-Deployment Steps

### 1. Update Frontend Environment Variables

After backend is deployed, update Vercel environment variables:
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Enter your backend URL: https://your-backend.railway.app
```

### 2. Update Backend CORS

Ensure backend allows your Vercel frontend:
```python
# In backend/src/main.py
CORS_ORIGINS = [
    "https://your-app.vercel.app",
    "http://localhost:3000"  # for local development
]
```

### 3. Test Deployment

1. Visit your Vercel frontend URL
2. Sign up for a new account
3. Create, edit, delete tasks
4. Verify all functionality works

### 4. Set Up Custom Domain (Optional)

**Vercel:**
- Go to Project Settings → Domains
- Add your custom domain

**Railway/Render:**
- Go to Settings → Custom Domain
- Add your domain and configure DNS

---

## Troubleshooting

### Frontend Issues

**Build fails:**
- Check Node.js version (should be 18+)
- Verify all dependencies are in package.json
- Check environment variables are set

**API calls fail:**
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS settings on backend
- Verify backend is running

### Backend Issues

**Database connection fails:**
- Verify DATABASE_URL is correct
- Check Neon database is accessible
- Ensure SSL mode is enabled: `?sslmode=require`

**Authentication fails:**
- Verify BETTER_AUTH_SECRET matches between frontend and backend
- Check JWT_SECRET_KEY is set
- Verify token expiration settings

**CORS errors:**
- Add Vercel URL to CORS_ORIGINS
- Restart backend after changes

---

## Cost Estimates

### Free Tier Limits

**Vercel:**
- 100 GB bandwidth/month
- Unlimited deployments
- Custom domains included

**Railway:**
- $5 free credit/month
- ~500 hours of runtime
- 1 GB RAM, 1 vCPU

**Render:**
- Free tier available
- 750 hours/month
- Sleeps after 15 min inactivity

**Neon:**
- Free tier: 0.5 GB storage
- 1 project, 10 branches
- Auto-suspend after 5 min inactivity

---

## Security Checklist

- [ ] All environment variables are set correctly
- [ ] No secrets in code or git history
- [ ] CORS is configured properly
- [ ] Database uses SSL connection
- [ ] JWT secrets are strong (32+ characters)
- [ ] GitHub token has been revoked and regenerated
- [ ] Production URLs are using HTTPS
- [ ] Rate limiting is configured (optional)

---

## Monitoring

**Vercel:**
- Analytics: Project → Analytics
- Logs: Deployments → View Function Logs

**Railway:**
- Metrics: Project → Metrics
- Logs: Project → Deployments → View Logs

**Render:**
- Metrics: Service → Metrics
- Logs: Service → Logs

**Neon:**
- Monitoring: Project → Monitoring
- Query performance: Operations tab
