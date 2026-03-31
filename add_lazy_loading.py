#!/usr/bin/env python3
"""
Add loading="lazy" attribute to all img tags (except logo/navigation).
Skips the logo image that appears in headers/footers.
"""

import re
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
HTML_FILES = sorted(PROJECT_DIR.glob("*.html"))

# Skip index.html since we already handled it
HTML_FILES = [f for f in HTML_FILES if f.name != "index.html"]

for html_file in HTML_FILES:
    content = html_file.read_text(encoding="utf-8")
    original = content

    # Add loading="lazy" to img tags that don't have it
    # But skip the logo image (shared/logo.webp)
    def add_lazy(match):
        tag = match.group(0)
        # Skip if already has loading attribute or is logo
        if 'loading=' in tag or 'logo.webp' in tag:
            return tag
        # Add loading="lazy" before the closing />
        return tag.replace('/>', ' loading="lazy" />')

    # Match <img ... /> tags
    content = re.sub(r'<img[^>]+/>', add_lazy, content)

    if content != original:
        html_file.write_text(content, encoding="utf-8")
        print(f"✓ Updated: {html_file.name}")
    else:
        print(f"— No changes: {html_file.name}")

print("\n✓ All HTML files updated with lazy loading.")
