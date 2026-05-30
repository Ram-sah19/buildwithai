# Brand Scraper Directive

## Goal
Use the Firecrawl API to scrape any website and extract a comprehensive brand intelligence package: colors, typography, fonts, key images (logos, hero/header images), UI component styles (buttons, inputs, effects), and a CSS starter kit — all organized into human-readable and machine-readable output files.

## Inputs
- `url` (required): The website URL to scrape.
- `subpages` (optional, flag): Also scrape a few sub-pages (about, contact, product) for richer data.
- `no_images` (optional, flag): Skip downloading images locally (still capture URLs).
- `output_dir` (optional): Custom output directory path. Default: `brand_assets/<domain>/`.

## Prerequisites
- `FIRECRAWL_API_KEY` must be set in `.env`.
  - Get an API key at https://firecrawl.dev
- Python dependencies: `pip install firecrawl-py python-dotenv`

## Steps (Workflow)

1. **Verify API key** is present in `.env` as `FIRECRAWL_API_KEY`.
2. **Run the scraper:**
   ```bash
   python execution/scrape_brand.py --url <URL>
   # With subpages:
   python execution/scrape_brand.py --url <URL> --subpages
   # Without downloading images:
   python execution/scrape_brand.py --url <URL> --no-images
   ```
3. **Locate outputs** in `brand_assets/<domain>/`:
   - `brand_report.md` — Full human-readable brand summary
   - `brand_data.json` — Raw structured JSON data
   - `images/` — Downloaded brand images (logo, hero, OG image, etc.)

4. **Summarize results** to the user — key colors (with hex), fonts, button styles, and any notable design patterns.

5. **Handle follow-ups:**
   - Specific hex values → read from `brand_data.json`
   - Image files → point to `brand_assets/<domain>/images/`
   - CSS code → derive from `brand_data.json` color and typography fields
   - New website build → offer the brand data as a design foundation

## Firecrawl API Calls Made

| # | Formats | Purpose |
|---|---------|---------|
| 1 | `branding`, `images`, `screenshot` | Full brand profile + image URLs + page screenshot |
| 2 | `json` (custom schema) | Structured hero/CTA/nav/effect extraction |
| 3+ | `branding` (per subpage) | Optional richer cross-page brand data |

## Error Handling
- **Missing API key:** Tell the user to add `FIRECRAWL_API_KEY` to `.env`.
- **Rate limit hit:** Script retries once after 10s delay.
- **Structured extraction fails:** Continues with partial data from branding call.
- **Image download fails:** Logs URL in report, skips download, continues.
- **Sub-page 404s:** Silently skips missing sub-pages.

## Constraints & Edge Cases
- Single-page scrapes use ~7 Firecrawl credits; with `--subpages` uses ~10–15 credits.
- Very JS-heavy sites (SPAs) may return limited branding data — recommend running without `--no-images` for best results.
- Image downloads are capped at 20 per run to avoid rate limits.
- Screenshot URLs from Firecrawl expire after 24 hours (not saved locally).

## Verification
- `brand_assets/<domain>/brand_report.md` should contain color hex codes, font names, and at least one image URL.
- `brand_assets/<domain>/brand_data.json` should contain `branding.colors.primary` and `branding.typography`.
- `brand_assets/<domain>/images/` should contain at least 1–2 downloaded files.
