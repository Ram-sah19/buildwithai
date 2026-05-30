---
name: brand-guidelines
description: Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Also used to apply externally scraped brand data (from the brand-scraper skill) to artifacts, websites, or design work. Use it when brand colors or style guidelines, visual formatting, or company design standards apply — either Anthropic's own brand or a scraped external brand.
license: Complete terms in LICENSE.txt
---

# Brand Styling Guide

## Overview

This skill covers two modes of brand styling:

1. **Anthropic Brand** — Anthropic's official brand identity and style resources
2. **Scraped Brand Data** — External brand data extracted via the `brand-scraper` skill from any website

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Anthropic brand, visual formatting, visual design, scraped brand, external brand, CSS variables, design system, color palette, fonts, logo, hero images, UI components

---

## Part 1: Anthropic Brand Guidelines

### Colors

**Main Colors:**

- Dark: `#141413` - Primary text and dark backgrounds
- Light: `#faf9f5` - Light backgrounds and text on dark
- Mid Gray: `#b0aea5` - Secondary elements
- Light Gray: `#e8e6dc` - Subtle backgrounds

**Accent Colors:**

- Orange: `#d97757` - Primary accent
- Blue: `#6a9bcc` - Secondary accent
- Green: `#788c5d` - Tertiary accent

### Typography

- **Headings**: Poppins (with Arial fallback)
- **Body Text**: Lora (with Georgia fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

### Features

#### Smart Font Application

- Applies Poppins font to headings (24pt and larger)
- Applies Lora font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

#### Text Styling

- Headings (24pt+): Poppins font
- Body text: Lora font
- Smart color selection based on background
- Preserves text hierarchy and formatting

#### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycles through orange, blue, and green accents
- Maintains visual interest while staying on-brand

### Technical Details

#### Font Management

- Uses system-installed Poppins and Lora fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Poppins and Lora fonts in your environment

#### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems

---

## Part 2: Scraped External Brand Data

When brand data has been extracted from an external website using the `brand-scraper` skill, use the structured outputs to apply that brand's visual identity to artifacts, websites, or design work.

### Where Scraped Brand Data Lives

After running `python execution/scrape_brand.py --url <URL>`, outputs are saved to:

```
brand_assets/<domain>/
├── brand_report.md     ← Human-readable summary (colors, fonts, buttons, effects)
├── brand_data.json     ← Raw structured data (primary source for applying brand)
└── images/
    ├── logo.svg / logo.png
    ├── og.png
    ├── hero.jpg
    └── ...
```

**For Feastables specifically**, all structured brand data is stored in the `brand_data/` folder in the project root:

```
brand_data/
├── brand.json          ← Full brand tokens (colors, typography, spacing, components)
├── images.json         ← All image URLs (logos, hero, products, textures)
└── variables.css       ← Ready-to-use CSS custom properties (:root block)
```

The built website using this data is in `website/`:
```
website/
├── index.html          ← Main Feastables-inspired website
├── style.css           ← Website styles (all brand tokens applied)
├── main.js             ← Interactivity (nav, cart, animations)
├── dashboard.html      ← Brand design system dashboard
├── dashboard.css       ← Dashboard styles
└── dashboard.js        ← Dashboard interactivity (copy, scroll-spy)
```


### Scraped Brand Data Structure (from `brand_data.json`)

```json
{
  "branding": {
    "colorScheme": "dark | light",
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
      "fontWeights": { "regular": 400, "medium": 500, "bold": 700 },
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
  },
  "structured": {
    "hero_headline": "...",
    "hero_subheadline": "...",
    "primary_cta_text": "...",
    "secondary_cta_text": "...",
    "navigation_links": ["..."],
    "visual_effects": ["glassmorphism", "gradient backgrounds", "card shadows", ...],
    "hero_image_url": "<url>",
    "tagline": "...",
    "social_proof_types": ["testimonials", "logos", "star ratings", ...]
  },
  "metadata": {
    "title": "...",
    "description": "...",
    "language": "...",
    "keywords": "...",
    "ogImage": "<url>"
  },
  "image_urls": ["<url>", ...],
  "images_downloaded": ["images/logo.svg", "images/og.png", ...]
}
```

### CSS Starter Variables (Auto-generated)

The `brand_report.md` includes a ready-to-use CSS `:root {}` block. Example:

```css
:root {
  --color-primary: #FF6B35;
  --color-secondary: #004E89;
  --color-accent: #F77F00;
  --color-bg: #1A1A1A;
  --color-text: #FFFFFF;
  --color-text-secondary: #B0B0B0;
  --font-primary: 'Inter', sans-serif;
  --font-heading: 'Inter', sans-serif;
  --size-h1: 48px;
  --size-h2: 36px;
  --size-body: 16px;
  --radius: 8px;
  --space-unit: 8px;
}
```

### Key Brand Images Extracted

The scraper prioritizes and downloads:

| Image Type | Source |
|------------|--------|
| **Logo** | `branding.logo` or `branding.images.logo` |
| **Favicon** | `branding.images.favicon` |
| **OG / Social Preview** | `branding.images.ogImage` or `metadata.ogImage` |
| **Hero Image** | `structured.hero_image_url` |
| **Top-scored page images** | Scored by filename patterns (logo, hero, banner, header, bg) |

Images are stored locally in `brand_assets/<domain>/images/`. SVG/PNG preferred over JPG for logos.

### UI Components Extracted

From `branding.components`:

- **Primary Button**: background color, text color, border radius
- **Secondary Button**: background, text color, border/border-color, border radius
- **Input Fields**: background, border, border radius

From `structured.visual_effects`:

- Notable CSS/visual patterns detected: glassmorphism, gradient backgrounds, card shadows, sticky headers, parallax, dark mode, animations

### Brand Personality

From `branding.personality`:
- **Tone**: e.g. professional, playful, minimal
- **Energy**: e.g. bold, calm, dynamic
- **Target audience**: e.g. developers, enterprises, creatives

### Applying Scraped Brand Data to New Work

When building a new website or artifact using scraped brand data:

1. **Read** `brand_assets/<domain>/brand_data.json` to get exact values
2. **Use CSS variables** from the auto-generated starter block as the design foundation
3. **Import Google Fonts** — the `brand_report.md` includes a ready-made `<link>` import tag
4. **Reference downloaded images** from `brand_assets/<domain>/images/` for logos and hero visuals
5. **Match button styles** using `components.buttonPrimary` and `components.buttonSecondary` values
6. **Apply spacing** using `spacing.baseUnit` (typically 8px) and `spacing.borderRadius`
7. **Replicate visual effects** listed in `structured.visual_effects`

### How to Trigger the Scraper

If brand data hasn't been scraped yet, run:

```bash
python execution/scrape_brand.py --url <URL>
# With sub-pages for richer data:
python execution/scrape_brand.py --url <URL> --subpages
```

Requires `FIRECRAWL_API_KEY` in `.env`. Each scrape uses ~7–15 Firecrawl credits.

See `directives/scrape_brand.md` for the full SOP.

---

## Part 3: Feastables Brand Identity

**Source:** https://feastables.com/pages/our-cocoa-story  
**Scraped:** 2026-05-30  
**Color scheme:** Light (paper-texture background)

> Feastables is a chocolate/snack brand co-created by MrBeast (Jimmy Donaldson). Their current mission: **eradicate child labor in the chocolate industry**. Every purchase helps build a better future for cocoa farmers.

---

### 🎨 Color Palette

| Role | Hex | Notes |
|------|-----|-------|
| **Brand Purple** | `#67318F` | Announcement bar / accent |
| **Checkout Accent / Button** | `#15CCFF` | Bright cyan-blue, CTA color |
| **Black** | `#000000` | Borders, heavy text, nav |
| **Off-White / Cream** | `#FAF9F5` (approx) | Card backgrounds (`bg-off-white`) |
| **Blue Cloud** | nav/card bg | Named token `bg-blue-cloud` (light periwinkle used in product card backgrounds) |
| **Checkout Background** | `#FFFFFF` | Checkout body |
| **Checkout Sidebar** | `#F5F5F5` | Light gray sidebar |
| **Error** | `#FF0000` | Checkout error color |
| **Text (dark)** | `#000000` | Primary text on light backgrounds |
| **Text (on dark)** | `#FFFFFF` | White on black/purple |

**Background texture:** Repeating paper texture image  
`https://feastables.com/cdn/shop/files/PaperTextureBg.jpg` (500×500px tile, `background-size: 500px 500px`)

---

### 🔤 Typography

Feastables uses a **custom multi-font system** — all fonts are self-hosted WOFF2 files on their CDN, not Google Fonts.

| Font Family | Style | Weights Available | Role |
|-------------|-------|-------------------|------|
| **Kanit** | Thai-inspired sans-serif | 100–900 (all weights + italics) | Navigation, product titles, body text |
| **Sohne** | Geometric sans-serif | 200–900 (all weights + italics) | Body / announcement bar (`font-sohne`) |
| **DrukWide** | Ultra-condensed display | 500 (medium), 700 (bold), 800 (heavy), 900 (super) | Hero headings, large display text |
| **OneZeroSix** | Display | 800 (ExtraBold only) | Special accent text |

**Font usage patterns (from CSS classes):**
- `font-kanit` — menu labels, product titles, CTAs
- `font-sohne` — announcement bar, body
- Navigation: uppercase italic (`italic uppercase text-[18px]`)
- Product card titles: `font-bold lg:font-extrabold text-base lg:text-2xl leading-none uppercase`

**Fallback fonts (checkout):**  
`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`

> ⚠️ All custom fonts are CDN-hosted. To replicate locally, use similar alternatives:
> - Kanit → available on Google Fonts
> - Sohne → commercial license required; substitute with `Inter` or `DM Sans`
> - DrukWide → commercial license (Typotheque); substitute with `Barlow Condensed ExtraBold` or `Impact`

---

### 🖼️ Key Brand Images

| Asset | URL |
|-------|-----|
| **Wordmark / Logo (nav)** | `https://feastables.com/cdn/shop/files/Feastables_Rebrand_Non_Tilted.png` (180px wide) |
| **Logo (square 32×32 favicon)** | `https://feastables.com/cdn/shop/files/Feastables_Rebrand_Lockup_Secondary__Square_32x32.png` |
| **Logo (2024 full)** | `https://feastables.com/cdn/shop/files/Feastables_Logo_2024.png` (500×173px) |
| **Checkout Logo** | `https://feastables.com/cdn/shop/files/Feastables_Logo_eef21c4d-5a99-4664-a3a1-f5ee2c5e8be9.png` |
| **Hero / About Us image** | `https://feastables.com/cdn/shop/files/aboutus-hero-web.jpg` (OG image, 1536px wide) |
| **Page background texture** | `https://feastables.com/cdn/shop/files/PaperTextureBg.jpg` |
| **Product: Mario Galaxy Cocoa Crunch** | `https://feastables.com/cdn/shop/files/Chocolate_MarioGalaxyCocoaCrunch_60g.png` |
| **Product: Cookies & Creme** | `https://feastables.com/cdn/shop/files/Chocolate_CookiesCreme_60g_2.5.png` |
| **Product: Caramel Chocolate** | `https://feastables.com/cdn/shop/files/Chocolate_Caramel_60g.png` |
| **Product: Milk Chocolate** | `https://feastables.com/cdn/shop/files/Chocolate_Milk_60g.png` |
| **Product: Milk Crunch** | `https://feastables.com/cdn/shop/files/Chocolate_MilkCrunch_60g_2.5.png` |

**OG / Social metadata:**
- Title: `Our Cocoa Story`
- Description: _"Feastables is still bringing the fun, now with bolder flavor and a bigger purpose. From chocolate bars to cups and beyond, every bite helps build a better future for the people behind it."_
- OG Image: `https://feastables.com/cdn/shop/files/aboutus-hero-web.jpg?v=1751051983&width=1536`

---

### 🔘 UI Components & Patterns

#### Product Cards
```
border: 4px solid #000000
border-radius: 0.75rem (rounded-xl)
background: off-white
hover: drop-shadow(5px 6px 0 #000000)  ← hard offset shadow, no blur
transition: ease-in 100ms
```
Product card images use a `bg-blue-cloud` (light blue) container with a wave-edge bottom cutout effect.

#### Navigation Header
```
background: bg-blue-cloud
height: 75px
border-bottom: 4px solid #000000
position: sticky top-0 z-20
transition: transform 500ms (hides on scroll)
```

#### Announcement Bar
```
background: #67318F (purple)
font: Kanit, underline, font-medium
padding: 8px 32px (mobile) / 6px 32px (desktop)
font-size: 14px (mobile) / 16px (desktop)
color: #ffffff
letter-spacing: 1px
```

#### Buttons (CTA)
```
checkout-button-color: #15CCFF
CTA text (add to cart): "ADD TO BAG"
```
Mobile menu buttons use `font-kanit uppercase italic` style with black backgrounds and white text.

#### Mobile Menu Accordions
```
border-bottom: 2px solid #000000
padding: 16px (py-4)
font: uppercase, italic, bold, 18px
```

---

### ✨ Visual Effects & Design Patterns

1. **Hard offset box shadows** — Cards use `drop-shadow(5px 6px 0 #000000)` — a pixel-art / retro aesthetic with no blur, just a solid black offset
2. **Paper texture background** — Full-page repeating texture (`500px × 500px`) gives a tactile, physical feel
3. **Wave-edge cutout** — Product card image containers have a custom wave-shaped bottom edge (`wave-edge-b` CSS class)
4. **4px solid black borders** — Used consistently on cards, buttons, modals, nav bar — gives a bold, graphic novel/comic feel
5. **Sticky hide-on-scroll nav** — Nav translates off-screen on scroll (`-translate-y-full`), reappears on focus/hover
6. **Bold uppercase italic text** — Navigation and headings consistently use uppercase + italic for an energetic, youthful feel
7. **Overlay modal pattern** — Announcement bar offers a modal pop-up on click with `bg-black/50` backdrop
8. **Alpine.js interactivity** — Entire UI uses Alpine.js (`x-data`, `x-show`, `x-on:click`) for lightweight reactive behavior

---

### 📐 Spacing & Layout

| Property | Value |
|----------|-------|
| Base grid | 3-column on mobile (grid-cols-3) |
| Card width | 200px fixed on desktop |
| Card aspect ratio | `1/0.75` (landscape) |
| Nav height | 75px |
| Border width | 4px (all major structural borders) |
| Border radius (cards) | `rounded-xl` (~12px) |
| Border radius (modal) | `rounded-xl` (~12px) |
| Card hover shadow offset | `5px 6px` |
| Announcement bar padding | `8px 32px` mobile / `6px 32px` desktop |

---

### 🧠 Brand Personality

| Dimension | Value |
|-----------|-------|
| **Tone** | Playful, bold, youthful, direct |
| **Energy** | High energy — uppercase, italic, exclamation points |
| **Visual style** | Retro-comic / graphic novel meets modern e-commerce |
| **Mission** | Purpose-driven: eradicate child labor in chocolate industry |
| **Target audience** | Gen Z / young millennials, MrBeast fans, snack enthusiasts |
| **Founder** | Jimmy Donaldson (MrBeast) |
| **Socials** | Instagram, Twitter/X, TikTok (`@feastables`) |
| **Headquarters** | 220 North Green Street Suite 100, Chicago, IL 60607 |

---

### 💻 CSS Starter Variables for Feastables-Inspired Design

```css
:root {
  /* Colors */
  --color-primary: #67318F;       /* brand purple */
  --color-accent: #15CCFF;        /* CTA cyan-blue */
  --color-black: #000000;         /* borders, text */
  --color-off-white: #FAF9F5;     /* card / page background */
  --color-blue-cloud: #D6E4F0;    /* product card container (approx) */
  --color-text: #000000;
  --color-text-on-dark: #FFFFFF;
  --color-error: #FF0000;

  /* Typography */
  --font-heading: 'Kanit', 'Barlow Condensed', sans-serif;
  --font-body: 'Kanit', 'Inter', sans-serif;
  --font-display: 'DrukWide', 'Impact', 'Barlow Condensed', sans-serif;

  /* Spacing */
  --border-width: 4px;
  --radius-card: 0.75rem;         /* rounded-xl */
  --radius-modal: 0.75rem;
  --nav-height: 75px;
  --shadow-offset: 5px 6px 0 #000000;  /* hard shadow, no blur */

  /* Background */
  --bg-texture: url('https://feastables.com/cdn/shop/files/PaperTextureBg.jpg');
  --bg-texture-size: 500px 500px;
}

/* Apply texture */
body {
  background-image: var(--bg-texture);
  background-repeat: repeat;
  background-size: var(--bg-texture-size);
}

/* Feastables card style */
.card {
  border: var(--border-width) solid var(--color-black);
  border-radius: var(--radius-card);
  background: var(--color-off-white);
  transition: filter 100ms ease-in;
}
.card:hover {
  filter: drop-shadow(var(--shadow-offset));
}
```

**Google Fonts approximation (Kanit is available):**
```html
<link href="https://fonts.googleapis.com/css2?family=Kanit:ital,wght@0,400;0,700;0,900;1,700&family=Barlow+Condensed:ital,wght@1,800&display=swap" rel="stylesheet">
```

---

### 📋 Navigation Structure

- SHOP → Chocolate (submenu with product cards), Snacks, Bundles
- Our Story / About Us (`/pages/our-cocoa-story`)
- Cart / Bag (icon, top right)
- Account (login redirect)
- Search

### 🏪 E-Commerce Context

- Platform: **Shopify** (custom theme named "Feastables", schema v2.0.0)
- Cart CTA: `"ADD TO BAG"` (not "Add to Cart")
- Currency: USD
- Checkout accent: `#15CCFF`
- Checkout logo position: center, size: medium
- Integrations: Klaviyo, Kustomer (chat), Tolstoy (video), MikMak (shoppable), OneTrust (cookie), TikTok/Meta/Google pixels
