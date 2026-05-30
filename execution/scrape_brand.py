#!/usr/bin/env python3
"""
Brand Scraper Execution Script
Uses the Firecrawl API to extract comprehensive brand identity data from any website.

Usage:
    python execution/scrape_brand.py --url https://example.com
    python execution/scrape_brand.py --url https://example.com --subpages
    python execution/scrape_brand.py --url https://example.com --no-images
    python execution/scrape_brand.py --url https://example.com --output-dir ./my_output
"""

import os
import sys
import json
import argparse
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------

def check_dependencies():
    missing = []
    try:
        from firecrawl import Firecrawl
    except ImportError:
        missing.append("firecrawl-py")
    try:
        from dotenv import load_dotenv
    except ImportError:
        missing.append("python-dotenv")
    if missing:
        print(f"Error: Missing dependencies: {', '.join(missing)}", file=sys.stderr)
        print(f"Install with: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(1)

check_dependencies()

from dotenv import load_dotenv
from firecrawl import Firecrawl

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape brand identity data from a website using Firecrawl."
    )
    parser.add_argument("--url", required=True, help="URL of the website to scrape.")
    parser.add_argument(
        "--subpages",
        action="store_true",
        help="Also scrape a few sub-pages (about, contact, product) for richer data.",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Skip downloading images locally (still capture URLs).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Override the default output directory (brand_assets/<domain>/).",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize_url(url: str) -> str:
    """Ensure the URL has a scheme."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def get_domain(url: str) -> str:
    """Extract a clean domain name from a URL (for use as a folder name)."""
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc or parsed.path
    # Strip www.
    domain = re.sub(r"^www\.", "", domain)
    # Remove port numbers and path
    domain = domain.split(":")[0].split("/")[0]
    # Sanitize for filesystem use
    domain = re.sub(r"[^\w\.\-]", "_", domain)
    return domain


def setup_output_dirs(output_dir: Path) -> dict:
    """Create output directories and return their paths."""
    dirs = {
        "root": output_dir,
        "images": output_dir / "images",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


def scrape_with_retry(firecrawl: Firecrawl, url: str, formats: list, retries: int = 2, **kwargs) -> Optional[dict]:
    """Call Firecrawl scrape with simple retry logic on failure."""
    for attempt in range(retries + 1):
        try:
            result = firecrawl.scrape(url, formats=formats, **kwargs)
            return result
        except Exception as e:
            err_str = str(e).lower()
            if "rate limit" in err_str and attempt < retries:
                print(f"  Rate limit hit, waiting 10s before retry {attempt + 1}...")
                time.sleep(10)
                continue
            print(f"  Warning: Scrape call failed for {url}: {e}", file=sys.stderr)
            return None
    return None


def download_image(url: str, dest_path: Path) -> bool:
    """Download an image from a URL to a local file. Returns True on success."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (brand-scraper/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            dest_path.write_bytes(response.read())
        return True
    except Exception as e:
        print(f"  Warning: Could not download image {url}: {e}", file=sys.stderr)
        return False


def score_image_url(url: str) -> int:
    """
    Score an image URL by how likely it is to be a meaningful brand asset.
    Higher = more interesting. Used to prioritize which images to download.
    """
    url_lower = url.lower()
    score = 0
    # Filename keywords that suggest brand-relevant images
    for keyword in ["logo", "hero", "banner", "header", "bg", "background", "og", "social", "brand", "cover", "splash"]:
        if keyword in url_lower:
            score += 10
    # Prefer SVG and PNG over JPG (logos are usually SVG/PNG)
    if url_lower.endswith(".svg"):
        score += 5
    elif url_lower.endswith(".png"):
        score += 3
    elif url_lower.endswith((".jpg", ".jpeg", ".webp")):
        score += 1
    # Prefer images in common asset paths
    for path_hint in ["/assets/", "/images/", "/img/", "/static/", "/media/"]:
        if path_hint in url_lower:
            score += 2
    # Prefer shorter URLs (often cleaner/more intentional assets)
    score -= len(url) // 50
    return score


def safe_get(obj, *keys, default=None):
    """Safely traverse nested dicts."""
    for key in keys:
        if obj is None:
            return default
        if isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return default
    return obj if obj is not None else default


# ---------------------------------------------------------------------------
# Brand Data Structured Schema (for Firecrawl JSON format)
# ---------------------------------------------------------------------------

BRAND_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "hero_headline": {
            "type": "string",
            "description": "The main headline text in the hero/banner section of the page.",
        },
        "hero_subheadline": {
            "type": "string",
            "description": "The subheadline or supporting text near the top of the page.",
        },
        "primary_cta_text": {
            "type": "string",
            "description": "The text of the main call-to-action button.",
        },
        "secondary_cta_text": {
            "type": "string",
            "description": "The text of any secondary call-to-action button.",
        },
        "navigation_links": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Top-level navigation menu items.",
        },
        "visual_effects": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Notable visual/CSS effects used on the page, e.g. glassmorphism, gradient backgrounds, card shadows, sticky headers, parallax, animations, dark mode.",
        },
        "hero_image_url": {
            "type": "string",
            "description": "URL of the main hero or header image, if any.",
        },
        "tagline": {
            "type": "string",
            "description": "The brand tagline or value proposition statement.",
        },
        "footer_links": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Key footer section labels or link groups.",
        },
        "social_proof_types": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Types of social proof present: testimonials, logos, star ratings, user counts, press mentions, etc.",
        },
    },
    "required": [],
}


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def color_block(hex_color: str) -> str:
    """Return a markdown-friendly color indicator."""
    if hex_color and hex_color.startswith("#"):
        return f"`{hex_color}`"
    return f"`{hex_color}`" if hex_color else "—"


def build_brand_report(
    url: str,
    domain: str,
    branding: dict,
    structured: dict,
    images_downloaded: list,
    all_image_urls: list,
    screenshot_url: str,
    metadata: dict,
    subpage_data: list,
) -> str:
    """Assemble the human-readable brand_report.md."""

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colors = safe_get(branding, "colors", default={})
    typography = safe_get(branding, "typography", default={})
    font_families = safe_get(typography, "fontFamilies", default={})
    font_sizes = safe_get(typography, "fontSizes", default={})
    font_weights = safe_get(typography, "fontWeights", default={})
    fonts = safe_get(branding, "fonts", default=[])
    spacing = safe_get(branding, "spacing", default={})
    components = safe_get(branding, "components", default={})
    brand_images = safe_get(branding, "images", default={})
    personality = safe_get(branding, "personality", default={})
    animations = safe_get(branding, "animations", default={})

    lines = []

    # ---------- Header ----------
    lines += [
        f"# Brand Report: {domain}",
        f"**Scraped:** {now}  ",
        f"**Source:** {url}  ",
        f"**Color Scheme:** {safe_get(branding, 'colorScheme', default='unknown')}  ",
        "",
        "---",
        "",
    ]

    # ---------- Color Palette ----------
    lines += [
        "## 🎨 Color Palette",
        "",
        "| Role | Hex |",
        "|------|-----|",
    ]
    color_roles = [
        ("Primary", "primary"),
        ("Secondary", "secondary"),
        ("Accent", "accent"),
        ("Background", "background"),
        ("Text (Primary)", "textPrimary"),
        ("Text (Secondary)", "textSecondary"),
        ("Link", "link"),
        ("Success", "success"),
        ("Warning", "warning"),
        ("Error", "error"),
    ]
    for label, key in color_roles:
        val = colors.get(key)
        if val:
            lines.append(f"| {label} | {color_block(val)} |")
    lines += ["", ""]

    # ---------- Typography ----------
    lines += [
        "## 🔤 Typography",
        "",
        f"- **Primary font:** {font_families.get('primary', '—')}",
        f"- **Heading font:** {font_families.get('heading', '—')}",
        f"- **Code/mono font:** {font_families.get('code', '—')}",
        "",
    ]
    if font_sizes:
        lines.append("**Font sizes:**")
        for size_name, size_val in font_sizes.items():
            lines.append(f"- {size_name}: {size_val}")
        lines.append("")

    if font_weights:
        lines.append("**Font weights:**")
        for weight_name, weight_val in font_weights.items():
            lines.append(f"- {weight_name}: {weight_val}")
        lines.append("")

    if fonts:
        all_families = [f.get("family", "") if isinstance(f, dict) else str(f) for f in fonts]
        all_families = [f for f in all_families if f]
        if all_families:
            lines.append(f"**All font families detected:** {', '.join(all_families)}")
            lines.append("")

    lines.append("")

    # ---------- Key Images ----------
    lines += [
        "## 🖼️ Key Images",
        "",
    ]
    logo = safe_get(branding, "logo") or brand_images.get("logo")
    favicon = brand_images.get("favicon")
    og_image = brand_images.get("ogImage") or metadata.get("ogImage")
    hero_img = safe_get(structured, "hero_image_url")

    if logo:
        lines.append(f"- **Logo:** {logo}")
    if favicon:
        lines.append(f"- **Favicon:** {favicon}")
    if og_image:
        lines.append(f"- **OG / Social Preview:** {og_image}")
    if hero_img:
        lines.append(f"- **Hero Image:** {hero_img}")

    if images_downloaded:
        lines.append("")
        lines.append("**Downloaded brand images (saved locally):**")
        for img in images_downloaded:
            lines.append(f"- `{img}`")

    if screenshot_url:
        lines.append("")
        lines.append(f"**Page Screenshot:** {screenshot_url}")

    if all_image_urls:
        lines.append("")
        lines.append(f"**Total images found on page:** {len(all_image_urls)}")
        top_images = sorted(all_image_urls, key=score_image_url, reverse=True)[:10]
        lines.append("**Top-scored images (most likely brand assets):**")
        for img_url in top_images:
            lines.append(f"- {img_url}")

    lines.append("")

    # ---------- UI Components ----------
    lines += [
        "## 🔘 UI Components",
        "",
    ]
    btn_primary = components.get("buttonPrimary", {})
    btn_secondary = components.get("buttonSecondary", {})
    input_style = components.get("input", {})

    if btn_primary:
        lines += [
            "### Primary Button",
            f"- Background: {color_block(btn_primary.get('background', '—'))}",
            f"- Text color: {color_block(btn_primary.get('textColor', '—'))}",
            f"- Border radius: {btn_primary.get('borderRadius', '—')}",
            f"- Border: {btn_primary.get('border', '—')}",
            "",
        ]
    if btn_secondary:
        lines += [
            "### Secondary Button",
            f"- Background: {color_block(btn_secondary.get('background', '—'))}",
            f"- Text color: {color_block(btn_secondary.get('textColor', '—'))}",
            f"- Border: {btn_secondary.get('border', '—')} / Border color: {color_block(btn_secondary.get('borderColor', '—'))}",
            f"- Border radius: {btn_secondary.get('borderRadius', '—')}",
            "",
        ]
    if input_style:
        lines += [
            "### Input Fields",
            f"- Background: {color_block(input_style.get('background', '—'))}",
            f"- Border: {input_style.get('border', '—')}",
            f"- Border radius: {input_style.get('borderRadius', '—')}",
            "",
        ]

    # ---------- Styling Effects ----------
    lines += [
        "## ✨ Styling Effects & Patterns",
        "",
    ]
    visual_effects = safe_get(structured, "visual_effects", default=[])
    if visual_effects:
        for effect in visual_effects:
            lines.append(f"- {effect}")
    else:
        lines.append("— No notable effects detected (or not enough page data)")

    if animations:
        lines.append("")
        lines.append("**Animations / Transitions:**")
        for anim_key, anim_val in animations.items():
            if anim_val:
                lines.append(f"- {anim_key}: {anim_val}")

    lines.append("")

    # ---------- Spacing & Layout ----------
    lines += [
        "## 📐 Spacing & Layout",
        "",
        f"- **Base unit:** {spacing.get('baseUnit', '—')}px",
        f"- **Border radius:** {spacing.get('borderRadius', '—')}",
        f"- **Padding:** {spacing.get('padding', '—')}",
        f"- **Margins:** {spacing.get('margins', '—')}",
        "",
    ]

    layout = safe_get(branding, "layout", default={})
    if layout:
        lines.append("**Layout:**")
        for k, v in layout.items():
            if v:
                lines.append(f"- {k}: {v}")
        lines.append("")

    # ---------- Hero / CTA ----------
    lines += [
        "## 🎯 Hero & Content",
        "",
    ]
    headline = safe_get(structured, "hero_headline")
    subheadline = safe_get(structured, "hero_subheadline")
    tagline = safe_get(structured, "tagline")
    cta_primary = safe_get(structured, "primary_cta_text")
    cta_secondary = safe_get(structured, "secondary_cta_text")
    nav_links = safe_get(structured, "navigation_links", default=[])
    social_proof = safe_get(structured, "social_proof_types", default=[])

    if tagline:
        lines.append(f"- **Tagline:** _{tagline}_")
    if headline:
        lines.append(f"- **Hero headline:** _{headline}_")
    if subheadline:
        lines.append(f"- **Hero subheadline:** _{subheadline}_")
    if cta_primary:
        lines.append(f"- **Primary CTA:** `{cta_primary}`")
    if cta_secondary:
        lines.append(f"- **Secondary CTA:** `{cta_secondary}`")
    if nav_links:
        lines.append(f"- **Navigation:** {', '.join(nav_links)}")
    if social_proof:
        lines.append(f"- **Social proof types:** {', '.join(social_proof)}")
    lines.append("")

    # ---------- Brand Personality ----------
    lines += [
        "## 🧠 Brand Personality",
        "",
    ]
    if personality:
        for k, v in personality.items():
            if v:
                lines.append(f"- **{k}:** {v}")
    else:
        lines.append("— Not detected")
    lines.append("")

    # ---------- CSS Starter Kit ----------
    lines += [
        "## 💻 CSS Starter Variables",
        "",
        "Copy this into your new project's `:root {}` as a starting point:",
        "",
        "```css",
        ":root {",
    ]
    if colors.get("primary"):
        lines.append(f"  --color-primary: {colors['primary']};")
    if colors.get("secondary"):
        lines.append(f"  --color-secondary: {colors['secondary']};")
    if colors.get("accent"):
        lines.append(f"  --color-accent: {colors['accent']};")
    if colors.get("background"):
        lines.append(f"  --color-bg: {colors['background']};")
    if colors.get("textPrimary"):
        lines.append(f"  --color-text: {colors['textPrimary']};")
    if colors.get("textSecondary"):
        lines.append(f"  --color-text-secondary: {colors['textSecondary']};")
    if font_families.get("primary"):
        lines.append(f"  --font-primary: '{font_families['primary']}', sans-serif;")
    if font_families.get("heading"):
        lines.append(f"  --font-heading: '{font_families['heading']}', sans-serif;")
    if font_sizes.get("h1"):
        lines.append(f"  --size-h1: {font_sizes['h1']};")
    if font_sizes.get("h2"):
        lines.append(f"  --size-h2: {font_sizes['h2']};")
    if font_sizes.get("body"):
        lines.append(f"  --size-body: {font_sizes['body']};")
    if spacing.get("borderRadius"):
        lines.append(f"  --radius: {spacing['borderRadius']};")
    if spacing.get("baseUnit"):
        lines.append(f"  --space-unit: {spacing['baseUnit']}px;")
    lines += [
        "}",
        "```",
        "",
    ]

    # Google Fonts import suggestion
    google_font_families = []
    for f in fonts:
        fam = f.get("family", "") if isinstance(f, dict) else str(f)
        if fam and fam not in ["system-ui", "-apple-system", "sans-serif", "serif", "monospace"]:
            google_font_families.append(fam)
    if google_font_families:
        query = "+".join([f.replace(" ", "+") for f in google_font_families[:3]])
        lines += [
            "**Google Fonts import suggestion:**",
            f"```html",
            f'<link href="https://fonts.googleapis.com/css2?family={query}&display=swap" rel="stylesheet">',
            "```",
            "",
        ]

    # ---------- Subpage Notes ----------
    if subpage_data:
        lines += [
            "## 📄 Subpage Brand Notes",
            "",
        ]
        for sp in subpage_data:
            sp_url = sp.get("url", "")
            sp_branding = sp.get("branding", {})
            sp_colors = safe_get(sp_branding, "colors", default={})
            lines += [
                f"### {sp_url}",
                f"- Color scheme: {safe_get(sp_branding, 'colorScheme', default='—')}",
                f"- Primary color: {color_block(sp_colors.get('primary', '—'))}",
                "",
            ]

    # ---------- Metadata ----------
    lines += [
        "## 📊 Page Metadata",
        "",
        f"- **Title:** {metadata.get('title', '—')}",
        f"- **Description:** {metadata.get('description', '—')}",
        f"- **Language:** {metadata.get('language', '—')}",
        f"- **Keywords:** {metadata.get('keywords', '—')}",
        "",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main scraper
# ---------------------------------------------------------------------------

def main():
    load_dotenv()
    args = parse_args()

    url = normalize_url(args.url)
    domain = get_domain(url)

    # -- API Key --
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("Error: FIRECRAWL_API_KEY not found in environment or .env file.", file=sys.stderr)
        print("Add it to .env: FIRECRAWL_API_KEY=fc-YOUR_KEY", file=sys.stderr)
        sys.exit(1)

    # -- Output dirs --
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    if args.output_dir:
        base_dir = Path(args.output_dir)
    else:
        base_dir = project_root / "brand_assets" / domain
    dirs = setup_output_dirs(base_dir)

    print(f"\n🔍 Brand Scraper — Target: {url}")
    print(f"📁 Output directory: {dirs['root']}")
    print()

    firecrawl = Firecrawl(api_key=api_key)

    # ----------------------------------------------------------------
    # CALL 1: Branding + Images + Screenshot
    # ----------------------------------------------------------------
    print("📡 Call 1/3: Fetching branding profile, images, and screenshot...")
    result_1 = scrape_with_retry(
        firecrawl, url,
        formats=["branding", "images", "screenshot"],
    )

    if result_1 is None:
        print("Error: Primary scrape call failed. Cannot continue.", file=sys.stderr)
        sys.exit(2)

    branding = result_1.get("branding", {}) if isinstance(result_1, dict) else {}
    all_image_urls = result_1.get("images", []) if isinstance(result_1, dict) else []
    screenshot_url = result_1.get("screenshot", "") if isinstance(result_1, dict) else ""
    metadata = result_1.get("metadata", {}) if isinstance(result_1, dict) else {}

    # Handle SDK object responses (not plain dicts)
    if hasattr(result_1, "branding"):
        branding = result_1.branding or {}
    if hasattr(result_1, "images"):
        all_image_urls = result_1.images or []
    if hasattr(result_1, "screenshot"):
        screenshot_url = result_1.screenshot or ""
    if hasattr(result_1, "metadata"):
        metadata = result_1.metadata or {}

    # Coerce to plain dicts if they're pydantic models or similar
    if hasattr(branding, "model_dump"):
        branding = branding.model_dump()
    if hasattr(metadata, "model_dump"):
        metadata = metadata.model_dump()

    print(f"  ✓ Branding profile received. Color scheme: {safe_get(branding, 'colorScheme', default='unknown')}")
    print(f"  ✓ Found {len(all_image_urls)} images on page")

    # ----------------------------------------------------------------
    # CALL 2: Structured JSON extraction
    # ----------------------------------------------------------------
    print("📡 Call 2/3: Extracting structured data (hero, CTAs, effects)...")
    result_2 = scrape_with_retry(
        firecrawl, url,
        formats=[{"type": "json", "schema": BRAND_JSON_SCHEMA, "prompt": "Extract hero content, navigation, CTAs, visual effects, and brand information from this website."}],
        only_main_content=False,
        timeout=120000,
    )

    structured = {}
    if result_2 is not None:
        structured_raw = result_2.get("json", {}) if isinstance(result_2, dict) else {}
        if hasattr(result_2, "json"):
            structured_raw = result_2.json or {}
        if hasattr(structured_raw, "model_dump"):
            structured_raw = structured_raw.model_dump()
        structured = structured_raw if isinstance(structured_raw, dict) else {}
        print(f"  ✓ Structured data extracted")
    else:
        print("  ⚠ Structured extraction failed — continuing with partial data")

    # ----------------------------------------------------------------
    # CALL 3: Sub-pages (optional)
    # ----------------------------------------------------------------
    subpage_data = []
    if args.subpages:
        print("📡 Call 3+: Fetching sub-pages for richer brand data...")
        base = url.rstrip("/")
        subpage_paths = ["/about", "/contact", "/product", "/pricing", "/blog"]
        for path in subpage_paths[:3]:
            sp_url = base + path
            print(f"  Trying {sp_url}...")
            sp_result = scrape_with_retry(
                firecrawl, sp_url,
                formats=["branding"],
            )
            if sp_result:
                sp_branding = sp_result.get("branding", {}) if isinstance(sp_result, dict) else {}
                if hasattr(sp_result, "branding"):
                    sp_branding = sp_result.branding or {}
                if hasattr(sp_branding, "model_dump"):
                    sp_branding = sp_branding.model_dump()
                if sp_branding:
                    subpage_data.append({"url": sp_url, "branding": sp_branding})
                    print(f"    ✓ Got branding for {sp_url}")
    else:
        print("📡 Call 3/3: Skipping sub-pages (use --subpages to enable)")

    # ----------------------------------------------------------------
    # Download key images
    # ----------------------------------------------------------------
    images_downloaded = []

    if not args.no_images:
        print("\n📥 Downloading key brand images...")

        # Build prioritized list of images to download
        candidate_urls = list(all_image_urls) if all_image_urls else []

        # Add high-priority images from branding profile
        priority_urls = []
        brand_images_map = safe_get(branding, "images", default={})
        if isinstance(brand_images_map, dict):
            for key in ["logo", "favicon", "ogImage"]:
                img_url = brand_images_map.get(key)
                if img_url and img_url not in priority_urls:
                    priority_urls.append(img_url)

        logo_url = safe_get(branding, "logo")
        if logo_url and logo_url not in priority_urls:
            priority_urls.insert(0, logo_url)

        og_from_meta = metadata.get("ogImage") or metadata.get("og_image")
        if og_from_meta and og_from_meta not in priority_urls:
            priority_urls.append(og_from_meta)

        hero_img_url = safe_get(structured, "hero_image_url")
        if hero_img_url and hero_img_url not in priority_urls:
            priority_urls.append(hero_img_url)

        # Score and sort general images
        scored_candidates = sorted(
            [u for u in candidate_urls if u not in priority_urls and u.startswith("http")],
            key=score_image_url,
            reverse=True,
        )

        download_list = priority_urls + scored_candidates[:15]

        for img_url in download_list:
            if not img_url or not img_url.startswith("http"):
                continue
            # Determine a filename
            parsed_img = urllib.parse.urlparse(img_url)
            basename = Path(parsed_img.path).name or "image"
            # Ensure unique filename
            dest = dirs["images"] / basename
            counter = 1
            while dest.exists():
                stem = Path(basename).stem
                suffix = Path(basename).suffix or ".png"
                dest = dirs["images"] / f"{stem}_{counter}{suffix}"
                counter += 1

            success = download_image(img_url, dest)
            if success:
                images_downloaded.append(str(dest.relative_to(dirs["root"])))
                print(f"  ✓ {dest.name}")
            # Limit to top 20 downloads
            if len(images_downloaded) >= 20:
                print("  (Reached 20-image download limit)")
                break
    else:
        print("\n⏭️  Skipping image downloads (--no-images)")

    # ----------------------------------------------------------------
    # Build and save report + JSON
    # ----------------------------------------------------------------
    print("\n📝 Generating brand report...")

    report_md = build_brand_report(
        url=url,
        domain=domain,
        branding=branding,
        structured=structured,
        images_downloaded=images_downloaded,
        all_image_urls=all_image_urls if isinstance(all_image_urls, list) else [],
        screenshot_url=screenshot_url,
        metadata=metadata,
        subpage_data=subpage_data,
    )

    report_path = dirs["root"] / "brand_report.md"
    report_path.write_text(report_md, encoding="utf-8")
    print(f"  ✓ Saved brand_report.md")

    # Save raw JSON data
    raw_data = {
        "url": url,
        "domain": domain,
        "scraped_at": datetime.now().isoformat(),
        "branding": branding,
        "structured": structured,
        "metadata": metadata,
        "image_urls": all_image_urls if isinstance(all_image_urls, list) else [],
        "screenshot_url": screenshot_url,
        "images_downloaded": images_downloaded,
        "subpages": subpage_data,
    }

    json_path = dirs["root"] / "brand_data.json"
    json_path.write_text(json.dumps(raw_data, indent=2, default=str), encoding="utf-8")
    print(f"  ✓ Saved brand_data.json")

    # ----------------------------------------------------------------
    # Summary
    # ----------------------------------------------------------------
    print(f"""
✅ Brand scrape complete!

📁 Output: {dirs['root']}
├── brand_report.md   ← Human-readable brand summary
├── brand_data.json   ← Raw structured data (JSON)
└── images/           ← {len(images_downloaded)} brand images downloaded

Key findings:
  Color scheme : {safe_get(branding, 'colorScheme', default='unknown')}
  Primary color: {safe_get(branding, 'colors', 'primary', default='not detected')}
  Primary font : {safe_get(branding, 'typography', 'fontFamilies', 'primary', default='not detected')}
  Images found : {len(all_image_urls) if isinstance(all_image_urls, list) else 0}
  Downloaded   : {len(images_downloaded)}
""")

    print(f"OUTPUT_DIR={dirs['root']}")


if __name__ == "__main__":
    main()
