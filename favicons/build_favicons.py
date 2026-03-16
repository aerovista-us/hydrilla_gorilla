#!/usr/bin/env python3
"""
Generate favicon pack from a source image (images/hg-logo.png or favicons/source.png).
Requires: pip install Pillow
"""
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
SOURCE_OPTIONS = [
    os.path.join(SCRIPT_DIR, "source.png"),
    os.path.join(ROOT, "images", "hg-logo.png"),
]

SIZES = [
    (16, "favicon-16x16.png"),
    (32, "favicon-32x32.png"),
    (180, "apple-touch-icon.png"),
    (192, "android-chrome-192x192.png"),
    (512, "android-chrome-512x512.png"),
]


def main():
    src = None
    for p in SOURCE_OPTIONS:
        if os.path.isfile(p):
            src = p
            break
    if not src:
        print("No source image found. Add images/hg-logo.png or favicons/source.png")
        sys.exit(1)

    im = Image.open(src).convert("RGBA")
    # Prefer square crop from center if not square
    w, h = im.size
    if w != h:
        s = min(w, h)
        left = (w - s) // 2
        top = (h - s) // 2
        im = im.crop((left, top, left + s, top + s))

    for size, name in SIZES:
        out = im.resize((size, size), Image.Resampling.LANCZOS)
        path = os.path.join(SCRIPT_DIR, name)
        out.save(path, "PNG")
        print("  ", name)

    # Build favicon.ico (16 and 32)
    ico_path = os.path.join(SCRIPT_DIR, "favicon.ico")
    i16 = im.resize((16, 16), Image.Resampling.LANCZOS)
    i32 = im.resize((32, 32), Image.Resampling.LANCZOS)
    i16.save(ico_path, format="ICO", append_images=[i32])
    print("  favicon.ico")

    # Ensure web manifest exists
    manifest_path = os.path.join(SCRIPT_DIR, "site.webmanifest")
    if not os.path.isfile(manifest_path):
        manifest = """{
  "name": "EchoVerse | Hydrilla Gorilla",
  "short_name": "Hydrilla Gorilla",
  "icons": [
    { "src": "android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#0f130f",
  "background_color": "#070807"
}
"""
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest)
        print("  site.webmanifest (created)")
    else:
        print("  site.webmanifest (unchanged)")

    print("Favicon pack built from", os.path.basename(src))


if __name__ == "__main__":
    main()
