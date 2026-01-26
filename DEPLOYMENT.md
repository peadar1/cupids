# Deployment Guide - Cupid's Matcher

This guide walks you through deploying the app using **Vercel** (frontend) and **Render** (backend).

## Prerequisites

1. Push your code to GitHub
2. Have accounts on:
   - [GitHub](https://github.com)
   - [Vercel](https://vercel.com) (sign up with GitHub)
   - [Render](https://render.com) (sign up with GitHub)
3. Your Supabase project credentials (already have these)

---

## Step 1: Deploy Backend on Render

### 1.1 Create New Web Service

1. Go to [render.com/dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:
   - **Name:** `cupids-api` (or whatever you want)
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 1.2 Add Environment Variables

In the Render dashboard, add these environment variables:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Your Supabase service role key |
| `SUPABASE_ANON_KEY` | Your Supabase anon key |
| `JWT_SECRET_KEY` | Your JWT secret (generate with `openssl rand -hex 32`) |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` |
| `CORS_ORIGINS` | `https://your-app.vercel.app` (update after Vercel deploy) |

### 1.3 Deploy

Click **"Create Web Service"** and wait for deployment.

**Save your Render URL** (e.g., `https://cupids-api.onrender.com`) - you'll need it for the frontend.

---

## Step 2: Deploy Frontend on Vercel

### 2.1 Import Project

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repo
4. Configure:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (auto-detected)

### 2.2 Add Environment Variables

| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | Your Render backend URL (e.g., `https://cupids-api.onrender.com`) |

### 2.3 Deploy

Click **"Deploy"** and wait for it to complete.

**Save your Vercel URL** (e.g., `https://cupids-matcher.vercel.app`)

---

## Step 3: Update CORS (Important!)

Go back to Render and update the `CORS_ORIGINS` environment variable:

```
https://cupids-matcher.vercel.app
```

(Use your actual Vercel URL)

Then **redeploy** the backend (Manual Deploy → Deploy latest commit).

---

## Step 4: Test Your Deployment

1. Visit your Vercel URL
2. Try signing up / logging in
3. Create an event
4. Test registration

---

## Troubleshooting

### Backend won't start
- Check Render logs for errors
- Verify all environment variables are set
- Make sure `requirements.txt` is in the `backend` folder

### Frontend can't connect to backend
- Check browser console for CORS errors
- Verify `VITE_API_BASE_URL` is set correctly (no trailing slash)
- Verify `CORS_ORIGINS` on Render includes your Vercel URL

### "Invalid token" errors
- Make sure `JWT_SECRET_KEY` is set on Render
- Clear browser localStorage and try logging in again

---

## Custom Domain (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed

### Render
1. Go to Service Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed

---

## Costs

| Service | Free Tier |
|---------|-----------|
| **Vercel** | Unlimited static sites, 100GB bandwidth |
| **Render** | 750 hours/month (sleeps after 15 min inactivity) |
| **Supabase** | 500MB database, 1GB storage |

For a college event app, the free tiers should be plenty!
