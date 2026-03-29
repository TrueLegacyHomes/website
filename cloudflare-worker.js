/**
 * Cloudflare Worker for True Legacy Homes
 * Handles dynamic blog post redirects from old WordPress structure to new /blog/ structure
 * 
 * Old URL: truelegacyhomes.com/hummel-figurines
 * New URL: truelegacyhomes.com/blog/hummel-figurines
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // Skip if already in /blog/, /upcoming-sales/, or other known paths
    const skipPaths = ['/blog/', '/upcoming-sales/', '/locations/', '/services/', '/about/', '/contact/', '/care-placement/', '/cash-home-offer/', '/fiduciaries/', '/joinourlist/'];
    if (skipPaths.some(prefix => path.startsWith(prefix))) {
      return fetch(request);
    }
    
    // Skip root, favicon, assets
    if (path === '/' || path.startsWith('/.') || path.match(/\.(css|js|jpg|jpeg|png|gif|svg|ico|webp|woff|woff2|ttf|pdf)$/i)) {
      return fetch(request);
    }
    
    // Remove trailing slash for consistency
    const cleanPath = path.replace(/\/$/, '');
    
    // Try redirecting to /blog/ version
    const blogPath = `/blog${cleanPath}`;
    const blogUrl = new URL(blogPath, url.origin);
    
    // Check if /blog/ version exists by making a HEAD request
    const testResponse = await fetch(blogUrl.toString(), { method: 'HEAD' });
    
    if (testResponse.ok) {
      // /blog/ version exists - return 301 redirect
      return Response.redirect(blogUrl.toString(), 301);
    }
    
    // No match - pass through to normal site (will hit 404 if doesn't exist)
    return fetch(request);
  }
};
