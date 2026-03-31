#!/usr/bin/env python3
"""Add defer attribute to all script.js references."""

import re
from pathlib import Path

PROJECT_DIR = Path(__file__).parent

files_to_update = [
    "donate.html",
    "medical-missions.html",
    "project-battery.html",
    "project-community-movement.html",
    "project-covid.html",
    "project-haiti-2018.html",
    "project-philippines-2023.html",
    "project-philippines-2025.html",
    "project-philippines.html",
    "project-urban-gardening.html",
    "sponsors.html",
    "team.html",
    "volunteer.html"
]

for filename in files_to_update:
    file_path = PROJECT_DIR / filename
    content = file_path.read_text(encoding="utf-8")
    original = content

    # Add defer to <script src="script.js"></script>
    content = re.sub(
        r'<script src="script\.js">',
        '<script src="script.js" defer>',
        content
    )

    if content != original:
        file_path.write_text(content, encoding="utf-8")
        print(f"✓ Updated: {filename}")
    else:
        print(f"— No changes: {filename}")

print("\n✓ All script.js tags updated with defer.")
