# Rooted Landing Page

Marketing site for growwithrooted.com.

## Stack
- Plain HTML5 with embedded CSS, single file
- No build step
- Deployed via Vercel (free Hobby tier)
- Email capture wired to Beehiiv (Rooted Weekly publication) — currently using a placeholder JS handler

## Brand
Forest deep #174038, sage #EDF0E8, terracotta #C47454. Georgia body, Fraunces italic display.

## Local preview
open index.html

## Deploy
1. Push to GitHub: gh repo create eyedripmedia/rooted-landing --public --source=. --push
2. Vercel: import the repo from the dashboard
3. Add custom domain growwithrooted.com in Vercel project settings
4. Vercel issues DNS records → add to Cloudflare (DNS only, gray cloud, not proxied) → live

## TODO before launch
- Wire Beehiiv embed (replace placeholder JS handler with real POST to Beehiiv subscribe endpoint)
- Add real /privacy and /terms pages (currently link to non-existent routes)
- Generate OG image (currently meta uses summary card, no image preview on social shares)
