# Brand Scraper References

## Firecrawl API — Branding Format Output Structure

The `branding` format from Firecrawl returns:

```json
{
  "colorScheme": "dark" | "light",
  "logo": "<url>",
  "colors": {
    "primary": "#hex",
    "secondary": "#hex",
    "accent": "#hex",
    "background": "#hex",
    "textPrimary": "#hex",
    "textSecondary": "#hex",
    "link": "#hex",
    "success": "#hex",
    "warning": "#hex",
    "error": "#hex"
  },
  "fonts": [{ "family": "Inter" }, ...],
  "typography": {
    "fontFamilies": { "primary": "Inter", "heading": "Inter", "code": "Roboto Mono" },
    "fontSizes": { "h1": "48px", "h2": "36px", "h3": "24px", "body": "16px" },
    "fontWeights": { "light": 300, "regular": 400, "medium": 500, "bold": 700 },
    "lineHeights": { "body": "1.6", "heading": "1.2" }
  },
  "spacing": {
    "baseUnit": 8,
    "borderRadius": "8px",
    "padding": "...",
    "margins": "..."
  },
  "components": {
    "buttonPrimary": { "background": "#hex", "textColor": "#hex", "borderRadius": "8px" },
    "buttonSecondary": { "background": "transparent", "textColor": "#hex", "borderColor": "#hex", "borderRadius": "8px" },
    "input": { "background": "#hex", "border": "1px solid #hex", "borderRadius": "8px" }
  },
  "images": { "logo": "<url>", "favicon": "<url>", "ogImage": "<url>" },
  "animations": { "transition": "...", "duration": "..." },
  "layout": { "grid": "...", "headerHeight": "...", "footerHeight": "..." },
  "personality": { "tone": "...", "energy": "...", "targetAudience": "..." }
}
```

## Image Scoring Heuristic

Images are scored to prioritize brand-relevant downloads:

| Signal | Points |
|--------|--------|
| Filename contains: logo, hero, banner, header | +10 each |
| SVG format | +5 |
| PNG format | +3 |
| JPG/WEBP | +1 |
| Path contains /assets/, /images/, /img/, /static/ | +2 |
| Short URL (fewer extra segments) | negative |

Priority order: branding.logo > branding.images.* > metadata.ogImage > structured.hero_image_url > scored general images

## Firecrawl Credits Used Per Run

| Mode | Approx Credits |
|------|---------------|
| Basic scrape (no subpages) | ~7 credits |
| With --subpages (3 sub-pages) | ~10–13 credits |
| Per sub-page added | +1–2 credits |

## Common Firecrawl SDK Patterns

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-...")

# Branding + images
result = firecrawl.scrape(url, formats=["branding", "images", "screenshot"])

# Structured JSON with schema
result = firecrawl.scrape(
    url,
    formats=[{"type": "json", "schema": schema_dict, "prompt": "..."}],
    only_main_content=False,
    timeout=120000
)

# Access data (SDK may return object OR dict)
branding = result.get("branding", {})           # dict access
branding = getattr(result, "branding", {})      # attribute access (pydantic)
if hasattr(branding, "model_dump"):             # coerce pydantic → dict
    branding = branding.model_dump()
```

## Output Directory Structure

```
brand_assets/
└── <domain>/
    ├── brand_report.md     ← Human-readable report
    ├── brand_data.json     ← Raw structured data
    └── images/
        ├── logo.svg
        ├── og.png
        ├── hero.jpg
        └── ...
```
