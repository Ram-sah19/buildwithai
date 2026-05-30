---
name: brand-scraper
description: >
  Scrapes any website using the Firecrawl API to extract a comprehensive brand intelligence package.
  Use this skill whenever a user wants to:
  - Extract brand colors, typography, fonts, or design systems from a website
  - Pull logos, hero images, header images, or other key visuals from a site
  - Gather UI styling data (buttons, spacing, effects) to inform a new website build
  - Research a competitor's or client's visual identity
  - Understand the design language of any website before building something new
  - Get structured brand data from a URL for design reference
  Trigger this skill for any request involving "scrape a site for branding", "pull brand colors from", "get the fonts from", "extract design from", "what does X's brand look like", or similar design/brand research requests. Even if the user just pastes a URL and says "get everything useful about this site's design", use this skill.
---

# Brand Scraper Skill

This skill uses the Firecrawl API to extract a complete brand intelligence package from any website — colors, typography, images, UI components, and styling patterns — and produces an organized report useful for building a new website or referencing a brand's design system.

## What This Skill Produces

For any URL, it generates:

1. **`brand_report.md`** — Human-readable markdown summary with all brand data
2. **`brand_data.json`** — Structured JSON with raw extracted data for downstream use
3. **`images/`** — Downloaded copies of key brand images (logos, OG images, favicons, hero images)

All outputs go to `brand_assets/<domain>/` in the project root.

## How to Use This Skill

When a user provides a URL (or asks you to scrape a site), follow this workflow:

### Step 1: Validate setup

Check that `FIRECRAWL_API_KEY` exists in `.env`. If it's missing, tell the user:
> "Please add your Firecrawl API key to `.env` as `FIRECRAWL_API_KEY=fc-YOUR_KEY`."
> You can get one at https://firecrawl.dev

### Step 2: Run the scraper

Run the execution script with the target URL:

```bash
python execution/scrape_brand.py --url <URL>
```

Optional flags:
- `--subpages` — also scrape a few sub-pages (about, contact, product) for richer data
- `--no-images` — skip downloading images (URLs only)
- `--output-dir <path>` — override the default output directory

The script handles all Firecrawl API calls and saves outputs automatically.

### Step 3: Present the results

After the script finishes:
1. Read and summarize `brand_assets/<domain>/brand_report.md` to the user
2. Point them to the `images/` folder for downloaded visuals
3. Highlight the most actionable insights: primary brand colors (with hex codes), font families, button styles, and any interesting UI patterns

### Step 4: Answer follow-up questions

The user may want to:
- Know specific hex values → read from `brand_data.json`
- See the hero/logo images → point to `brand_assets/<domain>/images/`
- Get CSS snippets derived from the brand data → generate them from the JSON
- Use this to start building a website → offer to use the brand data as a design foundation

## What the Scraper Extracts

The script makes **three Firecrawl API calls** per URL:

| Call | Formats Requested | What We Get |
|------|-------------------|-------------|
| Primary | `branding`, `images`, `screenshot` | Full brand profile + all image URLs + page screenshot |
| Structured | `json` (custom schema) | Hero section, CTAs, nav structure, UI patterns |
| Content | `markdown` | Raw page content for LLM analysis of design context |

### Branding Profile Fields Captured

From the `branding` format:
- **Color scheme** (light/dark)
- **Colors**: primary, secondary, accent, background, text colors, link/success/warning/error
- **Fonts**: all font families in use
- **Typography**: font sizes for h1–h3 and body, weights, line heights
- **Spacing**: base unit, border radius, padding/margins
- **Components**: button styles (primary/secondary), input fields
- **Images**: logo URL, favicon, OG image
- **Animations**: transition styles if detected
- **Brand personality**: tone, energy, target audience (if detectable)

### Images Captured

From the `images` format + branding:
- Logo (SVG/PNG)
- Favicon
- OG image (social preview)
- All `<img>` src URLs from the page
- Screenshots (full-page)

The script filters for "interesting" images — it scores images by filename patterns (logo, hero, banner, header, bg, background) and by image dimensions (larger images are more likely to be hero/header images).

### Structured Data (JSON Schema)

The structured extraction captures:
- Hero section text + CTA button labels/colors
- Navigation structure (top-level links)
- Key UI patterns (cards, grids, modals detected)
- Notable visual effects (gradients, glassmorphism, shadows, animations)
- Footer structure

## Brand Report Format

The output `brand_report.md` always follows this template:

```markdown
# Brand Report: <Domain>
Scraped: <timestamp>
Source: <URL>

---

## 🎨 Color Palette
| Role | Color | Hex |
|------|-------|-----|
| Primary | ██████ | #... |
...

## 🔤 Typography
- **Primary font**: ...
- **Heading font**: ...
- **Code/mono font**: ...
- **Font sizes**: H1: ..., H2: ..., Body: ...

## 🖼️ Key Images
- **Logo**: [link]
- **OG Image**: [link]
- **Hero/Header images**: [links]

## 🔘 UI Components
### Primary Button
- Background: #...
- Text color: #...
- Border radius: ...

### Secondary Button
...

## ✨ Styling Effects & Patterns
[Any notable effects detected: glassmorphism, gradients, animations, card styles, etc.]

## 📐 Spacing & Layout
- Base unit: ...px
- Border radius: ...

## 🧠 Brand Personality
[Tone, energy level, target audience if detected]

## 📋 Notes for New Website Build
[Actionable synthesis: what CSS variables to set, what Google Fonts to import, etc.]
```

## Error Handling

If a scrape fails:
- **Rate limit** → wait 10s and retry once
- **Invalid URL** → tell the user and ask for a corrected URL
- **Missing branding data** → fall back to `html` + `markdown` formats and extract colors/fonts using CSS parsing in the script
- **Image download fails** → log the URL in the report, skip local download, continue

## Credit Usage Note

Each full brand scrape uses approximately **10–15 Firecrawl credits**:
- 1 credit (branding + images + screenshot)
- 5 credits (json format with schema)
- 1 credit (markdown)
- ~1–5 credits per image download attempt (if enhanced proxy needed)

Let the user know if they ask about cost.
