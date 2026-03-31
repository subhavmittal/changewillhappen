#!/usr/bin/env python3
"""
Converts all images in the images/ folder to WebP format.
- Backs up originals to images_backup/ (same structure)
- Converts JPG/JPEG/PNG to WebP in images/ (same structure)
- Updates all HTML files to reference the new .webp paths
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
IMAGES_DIR = PROJECT_DIR / "images"
BACKUP_DIR = PROJECT_DIR / "images_backup"

SOURCE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def convert_image(src: Path, dest: Path) -> bool:
    ext = src.suffix.lower()
    quality = 82 if ext in {'.jpg', '.jpeg'} else 85
    result = subprocess.run(
        ["cwebp", "-q", str(quality), str(src), "-o", str(dest)],
        capture_output=True
    )
    return result.returncode == 0


def main():
    print("=== WebP Image Conversion Script ===\n")

    # ── Step 1: Backup ────────────────────────────────────────────────────────
    print("[1/3] Creating backup at images_backup/ ...")
    if BACKUP_DIR.exists():
        print("  ! images_backup/ already exists — skipping backup step.")
    else:
        shutil.copytree(IMAGES_DIR, BACKUP_DIR)
        print("  ✓ Backup created.\n")

    # ── Step 2: Convert images to WebP ───────────────────────────────────────
    print("[2/3] Converting images to WebP ...")
    converted, skipped, failed = 0, 0, 0

    for src in sorted(BACKUP_DIR.rglob("*")):
        if not src.is_file():
            continue

        rel = src.relative_to(BACKUP_DIR)
        dest_dir = IMAGES_DIR / rel.parent
        dest_dir.mkdir(parents=True, exist_ok=True)

        ext = src.suffix.lower()

        if ext in SOURCE_EXTENSIONS:
            dest = dest_dir / (src.stem + ".webp")
            if convert_image(src, dest):
                orig_kb = src.stat().st_size / 1024
                new_kb = dest.stat().st_size / 1024
                saving = (1 - new_kb / orig_kb) * 100
                print(f"  ✓ {rel}  →  {src.stem}.webp  "
                      f"({orig_kb:.0f} KB → {new_kb:.0f} KB, -{saving:.0f}%)")
                converted += 1
            else:
                print(f"  ✗ FAILED: {rel}")
                failed += 1

        elif ext == ".webp":
            shutil.copy2(src, dest_dir / src.name)
            print(f"  → Copied (already WebP): {rel}")
            skipped += 1

    # Remove original non-WebP files from images/ now that WebP versions exist
    print("\n  Removing original files from images/ ...")
    for f in IMAGES_DIR.rglob("*"):
        if f.is_file() and f.suffix.lower() in SOURCE_EXTENSIONS:
            f.unlink()
    print(f"  ✓ Conversion complete: {converted} converted, "
          f"{skipped} already WebP, {failed} failed.\n")

    # ── Step 3: Update HTML files ─────────────────────────────────────────────
    print("[3/3] Updating image paths in HTML files ...")

    # Match any path starting with images/ and ending with a convertible extension
    pattern = re.compile(
        r'(images/[^"\'<>]*?)\.(jpg|jpeg|png|JPG|JPEG|PNG)'
    )

    html_files = sorted(PROJECT_DIR.glob("*.html"))
    updated_count = 0

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        new_content = pattern.sub(r'\1.webp', content)

        if new_content != content:
            html_file.write_text(new_content, encoding="utf-8")
            print(f"  ✓ Updated: {html_file.name}")
            updated_count += 1
        else:
            print(f"  — No changes: {html_file.name}")

    print(f"\n  {updated_count} HTML file(s) updated.")
    print("\n=== All done! ===")


if __name__ == "__main__":
    main()
