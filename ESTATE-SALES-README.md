# Estate Sales Weekly Update

## Two-Part Workflow

The estate sales update is now split into two parts so you can review the website before creating the email.

---

## Part 1: Website Pages

**First, paste your addresses:**

Edit `/scripts/addresses-input.txt` and paste the addresses from your report (one per line):

```
24668 Jutewood Pl, Lake Forest, CA 92630
6111 Del Cerro Boulevard, San Diego, CA 92120
8060 Shir Mar Place, El Cajon, CA 92021
```

**Then say to Clark:**

> **"Run the estate sales pages script"**

This will:
1. Fetch sales from EstateSales.net
2. **Match addresses by zip code** from your input file
3. Extract ALL images using Playwright
4. Validate images (parallel, removes 403s)
5. Generate website pages using `estate-sale-template.html`
6. Commit to staging branch
7. Give you staging URL to review

---

## Part 2: Mailchimp Email

After reviewing the staging site, say to Clark:

> **"Run the estate sales email script"**

This will:
1. Use the data from Part 1
2. Generate Mailchimp email using your templates
3. Create campaign as DRAFT
4. Give you preview link

---

## Templates (DO NOT CHANGE)

These templates are locked - the scripts use them exactly as-is:

1. **Website Page Template**  
   `/estate-sale-template.html`
   - Individual sale pages (e.g., `/upcoming-sales/jutewood-lake-forest/`)

2. **Email Main Template**  
   `/estate-sales-email-template.html`
   - Full email structure (header, footer, Mailchimp merge tags)

3. **Email Card Template**  
   `/estate-sale-card-template.html`
   - Repeating block for each sale (6-image grid)

---

## Address Matching

The script now:
- Reads addresses from `/scripts/addresses-input.txt` (your report)
- Matches them to sales by **zip code**
- Works great when all zips are different
- Falls back to "Address TBD" if no match found

---

## Manual Run

If you want to run it yourself without Clark:

**Part 1 (Pages):**
```bash
cd /Users/admin/.openclaw/workspace/tlh-rebuild
bash scripts/update-estate-sales-pages.sh
```

**Part 2 (Email):**
```bash
cd /Users/admin/.openclaw/workspace/tlh-rebuild
bash scripts/update-estate-sales-email.sh
```

---

## Output

**After Part 1:**
- **Staging URL:** https://staging.website-252.pages.dev/upcoming-sales/
- **Temp Files:** `/tmp/estate-sales-<timestamp>/`
  - `sales.json` - Raw sale data
  - `addresses.txt` - Full street addresses (matched to sale IDs)
  - `sale-{id}-guids.txt` - All extracted images
  - `sale-{id}-validated.txt` - Validated images (200 OK)
  - `weekend-dates.txt` - Calculated weekend dates

**After Part 2:**
- **Mailchimp Campaign:** Created as DRAFT (ready to review/send)
- **Email HTML:** `$TMP_DIR/email.html`

---

## Push to Production

After reviewing staging and sending the email:

```bash
cd /Users/admin/.openclaw/workspace/tlh-rebuild
git checkout main
git merge staging -m "Merge estate sales for [date]"
git push origin main
```

Production URL: https://www.truelegacyhomes.com/upcoming-sales/

---

## Scripts

**Part 1:**
- `scripts/update-estate-sales-pages.sh` - Main pages script
- `/Users/admin/.openclaw/workspace/scripts/fetch-estatesales-company.js` - Fetch sales
- `/Users/admin/.openclaw/workspace/scripts/extract-estatesales-images.js` - Playwright image extraction

**Part 2:**
- `scripts/update-estate-sales-email.sh` - Main email script
- `scripts/generate-mailchimp-email.py` - Email generator

---

## Why Two Parts?

1. **Review first** - You can check the staging site before committing to the email
2. **Address timing** - Addresses are often released Friday 9am, so you might run Part 1 Thursday (with images) and Part 2 Friday (once addresses are available)
3. **Flexibility** - You can re-run Part 2 if you want to tweak the email without regenerating pages

---

## Troubleshooting

**"Address TBD" appearing?**
- Addresses not released yet (usually Friday 9am PST)
- Wait and run Part 1 again once addresses are live

**Images not loading?**
- Check validated count vs extracted count
- Some sales have 403-protected images (normal, script filters them out)

**Part 2 says "no data found"?**
- Run Part 1 first
- Make sure the `/tmp/estate-sales-*` directory exists

**Email looks wrong?**
- Check `$TMP_DIR/email.html` for raw output
- Verify templates weren't modified

---

## Notes

- Scripts use the **new templates** (May 2026)
- Email stays as **DRAFT** for you to review/send
- Weekend dates are **automatically calculated**
- Address matching uses **JSON-LD streetAddress** (most reliable method)
- Instagram URL: **truelegacyestatesales** (not truelegacyhomes)
