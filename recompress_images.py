#!/usr/bin/env python3
"""
Re-compress all images with intelligent resizing.
Uses sips (macOS) to resize, then cwebp to convert to WebP.
Targets:
  - Carousel/hero images: max 1600px wide
  - Large project/community images: max 1000px wide
  - Small action/thumbnail images: max 600px wide
"""

import os
import re
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
IMAGES_DIR = PROJECT_DIR / "images"
BACKUP_DIR = PROJECT_DIR / "images_backup"

# Size targets by folder/image name pattern
SIZE_TARGETS = {
    "carousel": 1600,           # Hero carousel - full width
    "story-main": 1600,         # Full width story image
    "donate": 1600,             # Large donate image
    "project1": 1600,           # Large home project image
    "project2": 1600,           # Large home project image
    "community_movement": 1000, # Large community photos
    "haiti_project": 1000,      # Large haiti photos
    "medical_missions": 1000,   # Large medical photos
    "IMG_": 1000,               # Camera photos (high res originals)
    "DSCN": 1000,               # Camera photos
    "home": 1000,               # Home images (default)
    "battery_project": 600,     # Action diagrams
    "philippines_project": 800, # Project images
    "urban_gardening": 800,     # Garden image
    "volunteer": 800,           # Small volunteer image
    "donate1": 1000,            # Donate image variant
    "project3": 600,            # Small icon
    "shared": 600,              # Logo and small images
    "action": 600,              # Action diagrams
}


def get_target_width(filepath: Path) -> int:
    """Determine target width based on file path."""
    path_str = filepath.as_posix().lower()

    for pattern, width in SIZE_TARGETS.items():
        if pattern.lower() in path_str:
            return width
    return 1000  # Default fallback


def get_image_dimensions(img_path: Path) -> tuple:
    """Get image width and height using sips."""
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(img_path)],
        capture_output=True,
        text=True
    )

    try:
        lines = result.stdout.strip().split('\n')
        # Skip first line (filename), parse width and height
        width = int(lines[1].split(': ')[1])
        height = int(lines[2].split(': ')[1])
        return (width, height)
    except Exception as e:
        return None


def resize_image(src: Path, dest: Path, target_width: int) -> bool:
    """Resize image to target width using sips, maintaining aspect ratio."""
    try:
        # Get original dimensions
        dims = get_image_dimensions(src)
        if not dims:
            print(f"    ! Could not read dimensions: {src.name}")
            return False

        orig_width, orig_height = dims

        # Skip if already smaller than target
        if orig_width <= target_width:
            print(f"    → Already smaller than target ({orig_width}px < {target_width}px)")
            subprocess.run(
                ["cp", str(src), str(dest)],
                capture_output=True
            )
            return True

        # Calculate new height maintaining aspect ratio
        new_height = int((target_width / orig_width) * orig_height)

        # Resize using sips
        result = subprocess.run(
            ["sips", "-z", str(new_height), str(target_width), str(src), "-o", str(dest)],
            capture_output=True
        )

        if result.returncode == 0:
            return True
        else:
            print(f"    ! Resize failed: {result.stderr.decode()}")
            return False
    except Exception as e:
        print(f"    ! Error: {e}")
        return False


def convert_to_webp(src: Path, dest: Path) -> bool:
    """Convert image to WebP using cwebp."""
    quality = 75  # Slightly lower quality for pre-resized images
    result = subprocess.run(
        ["cwebp", "-q", str(quality), str(src), "-o", str(dest)],
        capture_output=True
    )
    return result.returncode == 0


def main():
    print("=== Image Recompression & Resize Script ===\n")

    print("[1/3] Creating temp workspace...")
    temp_dir = PROJECT_DIR / ".images_temp"
    if temp_dir.exists():
        import shutil
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    print("  ✓ Temp directory ready.\n")

    print("[2/3] Resizing and converting images...")
    converted, failed = 0, 0

    for src in sorted(BACKUP_DIR.rglob("*")):
        if not src.is_file() or src.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}:
            continue

        rel = src.relative_to(BACKUP_DIR)
        target_width = get_target_width(src)

        # Resize to temp
        temp_resized = temp_dir / rel.with_suffix('.tmp')
        temp_resized.parent.mkdir(parents=True, exist_ok=True)

        if not resize_image(src, temp_resized, target_width):
            print(f"  ✗ Resize failed: {rel}")
            failed += 1
            continue

        # Convert to WebP
        final_dest = IMAGES_DIR / rel.parent / (src.stem + ".webp")
        final_dest.parent.mkdir(parents=True, exist_ok=True)

        if convert_to_webp(temp_resized, final_dest):
            orig_kb = src.stat().st_size / 1024
            new_kb = final_dest.stat().st_size / 1024
            saving = (1 - new_kb / orig_kb) * 100
            print(f"  ✓ {rel.parent.name}/{src.stem}  →  {src.stem}.webp")
            print(f"      {orig_kb:.0f} KB → {new_kb:.0f} KB (-{saving:.0f}%)")
            converted += 1
        else:
            print(f"  ✗ Convert failed: {rel}")
            failed += 1

    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

    print(f"\n  ✓ Conversion complete: {converted} recompressed, {failed} failed.\n")

    print("[3/3] Summary")
    total_orig = sum(f.stat().st_size for f in BACKUP_DIR.rglob("*") if f.is_file()) / 1024 / 1024
    total_new = sum(f.stat().st_size for f in IMAGES_DIR.rglob("*") if f.is_file()) / 1024 / 1024
    savings = (1 - total_new / total_orig) * 100

    print(f"  Original total: {total_orig:.1f} MB")
    print(f"  New total: {total_new:.1f} MB")
    print(f"  Overall savings: {savings:.0f}%\n")
    print("=== Done! ===")


if __name__ == "__main__":
    main()
