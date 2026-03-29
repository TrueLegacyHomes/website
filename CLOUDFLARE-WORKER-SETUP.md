# Cloudflare Worker Setup for Blog Redirects

## What This Does
Automatically redirects old WordPress blog URLs to the new `/blog/` structure:
- `truelegacyhomes.com/hummel-figurines` → `truelegacyhomes.com/blog/hummel-figurines`
- Handles ALL blog posts (current + future)
- Proper 301 redirects for SEO
- Free (100k requests/day limit)

## Setup Instructions

### Option 1: Deploy via Cloudflare Dashboard (Easiest)

1. **Log in to Cloudflare Dashboard**
   - Go to: https://dash.cloudflare.com
   - Select your account

2. **Navigate to Workers & Pages**
   - Left sidebar → Workers & Pages
   - Click "Create Application"
   - Choose "Create Worker"

3. **Name the Worker**
   - Name: `tlh-blog-redirects`
   - Click "Deploy"

4. **Edit the Worker Code**
   - Click "Edit Code"
   - Delete the default code
   - Copy the entire contents of `cloudflare-worker.js` (this directory)
   - Paste into the editor
   - Click "Save and Deploy"

5. **Add Route to Your Site**
   - Go back to Workers & Pages
   - Click on your `tlh-blog-redirects` worker
   - Click "Triggers" tab
   - Click "Add Route"
   - Route: `truelegacyhomes.com/*`
   - Zone: `truelegacyhomes.com`
   - Click "Save"

6. **Test**
   - Wait 30 seconds for deployment
   - Visit: https://truelegacyhomes.com/hummel-figurines/
   - Should redirect to: https://truelegacyhomes.com/blog/hummel-figurines

---

### Option 2: Deploy via Wrangler CLI (Advanced)

```bash
# Install Wrangler (if not already installed)
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy the worker
wrangler deploy cloudflare-worker.js --name tlh-blog-redirects

# Add route
wrangler route add "truelegacyhomes.com/*" tlh-blog-redirects
```

---

## How It Works

1. **Request comes in** for `/hummel-figurines`
2. **Worker checks** if path is already `/blog/`, `/upcoming-sales/`, etc. (skip if yes)
3. **Worker tests** if `/blog/hummel-figurines` exists (HEAD request)
4. **If exists:** Returns 301 redirect to `/blog/hummel-figurines`
5. **If not:** Passes through to normal site (will 404 if page doesn't exist)

## What Gets Redirected

✅ **Old blog posts:** `/hummel-figurines` → `/blog/hummel-figurines`
✅ **Future posts:** Automatically handles new content
✅ **Works for all 98 blog posts** without listing them individually

## What Doesn't Get Redirected

❌ Already `/blog/` URLs (pass through)
❌ Core pages (`/about/`, `/contact/`, etc. - pass through)
❌ Static assets (CSS, JS, images - pass through)
❌ Homepage (`/` - pass through)

## Monitoring

Check usage in Cloudflare Dashboard:
- Workers & Pages → `tlh-blog-redirects` → Metrics

Free tier limit: **100,000 requests/day**

Your site traffic is well below this - you're safe.

---

## Troubleshooting

**"Worker not triggering"**
- Check Routes tab - make sure `truelegacyhomes.com/*` is added
- Clear browser cache
- Wait 60 seconds after deployment

**"Still getting 404"**
- Verify the `/blog/` version of the page actually exists
- Check Worker logs in dashboard (Real-time Logs)

**"Redirect loop"**
- Check that skipPaths includes all your main sections
- Shouldn't happen with this code, but verify in logs

---

## Cost

**Free Plan:**
- 100,000 requests/day
- More than enough for your traffic

**If you exceed (unlikely):**
- Paid plan: $5/month for 10 million requests
- You'd need 3,333+ visitors/day to hit the free limit
