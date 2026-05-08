#!/usr/bin/env python3
"""Generate SuShi/Zhaoyun/Foyin sprites by recoloring official Stardew Valley NPC templates.

Strategy:
  - SuShi  <- Sebastian (dark-haired male)
  - Zhaoyun <- Penny (red-haired female)
  - Foyin  <- Harvey (bearded male with hat)

Process:
  1. Load source sprite (64xH), crop to first 4 rows (64x128)
  2. Classify each pixel into semantic groups (hair, skin, clothes, etc.)
  3. Remap colors per group to target palette
  4. Apply shape modifications (turban for SuShi, bald for Foyin)
  5. Save as 64x128 character sprite and 128x128 portrait
"""

from PIL import Image
import os
import sys
import math
from collections import Counter

# === Paths ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = "/Users/tauwoo/Library/Application Support/Steam/steamapps/common/Stardew Valley/Contents/MacOS/Mods/SpriteExtractor/output"
CHAR_OUT_DIR = os.path.join(PROJECT_DIR, "assets", "Characters")
PORT_OUT_DIR = os.path.join(PROJECT_DIR, "assets", "Portraits")

# === Utility Functions ===

def rgb_to_hsv(r, g, b):
    """Convert RGB (0-255) to HSV (h: 0-360, s: 0-1, v: 0-1)."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn

    if diff == 0:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360

    s = 0 if mx == 0 else diff / mx
    v = mx
    return h, s, v


def hsv_to_rgb(h, s, v):
    """Convert HSV (h: 0-360, s: 0-1, v: 0-1) to RGB (0-255)."""
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return (
        max(0, min(255, int((r + m) * 255))),
        max(0, min(255, int((g + m) * 255))),
        max(0, min(255, int((b + m) * 255))),
    )


def color_distance(c1, c2):
    """Euclidean distance in RGB space."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))


def classify_pixel_sebastian(rgb):
    """Classify a Sebastian pixel into semantic groups.
    Returns: 'hair', 'skin', 'clothes', 'outline', 'eye', 'other'
    """
    r, g, b = rgb[:3]
    h, s, v = rgb_to_hsv(r, g, b)

    # Sebastian's palette analysis:
    # Hair/clothes (purple-dark): (49,0,37), (59,14,60), (58,31,72), (30,0,21), (91,34,86)
    # Skin: (255,189,132), (247,143,109), (216,99,101)
    # Jacket detail: (70,51,108), (135,139,221), (214,216,255)
    # Outline: (51,32,35), (39,39,46)
    # Pants: (69,40,89)

    # Very dark, low saturation -> outline
    if v < 0.22 and s < 0.5:
        return 'outline'

    # Skin tones (warm orange-peach, high value)
    if v > 0.55 and 10 < h < 40 and s > 0.3:
        return 'skin'

    # Eye whites / bright highlights
    if v > 0.8 and s < 0.2:
        return 'eye_white'

    # Purple/magenta range -> hair or clothes (Sebastian's main colors)
    if 270 < h < 360 or h < 20:
        if s > 0.3 and v < 0.55:
            return 'hair'  # dark purple = hair
        if s > 0.2 and v >= 0.55:
            return 'skin'  # lighter warm = skin

    # Blue-purple range -> jacket accent
    if 240 < h < 300 and v > 0.3:
        return 'clothes'

    # Default: treat as hair/clothes based on value
    if v < 0.45:
        return 'hair'
    return 'clothes'


def classify_pixel_penny(rgb):
    """Classify a Penny pixel into semantic groups."""
    r, g, b = rgb[:3]
    h, s, v = rgb_to_hsv(r, g, b)

    # Penny's palette:
    # Hair (red-brown): (96,10,55), (127,40,55), (173,31,35), (73,8,51)
    # Skin: (248,196,158)
    # Clothes (orange/yellow): (226,97,36), (247,190,79), (249,158,72), (173,77,47)
    # Dress detail: (211,99,88), (170,178,193), (247,153,165)
    # Lips/blush: (132,61,122), (213,124,182)

    # Very dark -> outline
    if v < 0.15:
        return 'outline'

    # Skin (warm peach, high value)
    if v > 0.7 and 15 < h < 40 and s > 0.2 and s < 0.6:
        return 'skin'

    # Eye whites
    if v > 0.85 and s < 0.15:
        return 'eye_white'

    # Hair (dark red/magenta, low-mid value)
    if (330 < h or h < 15) and s > 0.5 and v < 0.55:
        return 'hair'

    # Clothes (orange/yellow, mid-high value)
    if 20 < h < 55 and s > 0.4 and v > 0.5:
        return 'clothes'

    # Pink/blush accents
    if 280 < h < 340 and v > 0.4:
        return 'accessory'

    # Gray/blue (dress detail)
    if s < 0.2 and v > 0.5:
        return 'clothes_accent'

    # Red-orange mid tones -> clothes
    if 0 < h < 30 and s > 0.4 and v > 0.5:
        return 'clothes'

    # Default
    if v < 0.4:
        return 'hair'
    return 'clothes'


def classify_pixel_harvey(rgb):
    """Classify a Harvey pixel into semantic groups."""
    r, g, b = rgb[:3]
    h, s, v = rgb_to_hsv(r, g, b)

    # Harvey's palette:
    # Hair/mustache (dark brown): (36,21,15), (75,26,32), (92,47,31), (139,55,40), (178,97,11)
    # Skin: (255,213,159), (238,139,97)
    # Clothes (green): (20,37,29), (39,76,54), (68,118,81), (79,154,94)
    # Tie/accent: (58,27,51), (81,14,46), (137,13,13), (113,51,58)
    # Glasses: (144,157,157), (208,208,208)

    # Very dark -> outline or hair
    if v < 0.15:
        return 'outline'

    # Skin (warm peach/orange, high value)
    if v > 0.65 and 15 < h < 40 and s > 0.25:
        return 'skin'

    # Eye whites / glasses
    if v > 0.75 and s < 0.15:
        return 'eye_white'

    # Hair/mustache (warm brown, low-mid value)
    if 0 < h < 40 and s > 0.3 and v < 0.6:
        return 'hair'

    # Green clothes
    if 80 < h < 170 and s > 0.2:
        return 'clothes'

    # Red/maroon tie
    if (330 < h or h < 15) and s > 0.4 and v < 0.5:
        return 'accessory'

    # Gray (glasses)
    if s < 0.15 and 0.4 < v < 0.85:
        return 'glasses'

    # Default
    if v < 0.4:
        return 'hair'
    return 'clothes'

def remap_color_sushi(rgb, group):
    """Remap Sebastian colors to SuShi palette.
    SuShi: Dongpo turban (dark blue-black), blue scholar robe, warm skin.
    """
    r, g, b = rgb[:3]
    h, s, v = rgb_to_hsv(r, g, b)

    if group == 'outline':
        # Keep dark outline, shift slightly blue
        return (38, 28, 18)

    elif group == 'skin':
        # Keep warm skin, slightly adjust
        # Map Sebastian's skin range to SuShi's warmer tone
        if v > 0.85:
            return (250, 218, 190)  # highlight
        elif v > 0.7:
            return (238, 200, 168)  # base
        elif v > 0.55:
            return (212, 172, 140)  # shadow
        else:
            return (188, 145, 115)  # deep shadow

    elif group == 'eye_white':
        return (255, 255, 255)

    elif group == 'hair':
        # Sebastian's dark purple hair -> SuShi's dark blue-black turban/hair
        if v > 0.35:
            return (52, 50, 68)   # turban highlight
        elif v > 0.2:
            return (30, 28, 42)   # turban base
        else:
            return (20, 18, 30)   # turban shadow

    elif group == 'clothes':
        # Sebastian's purple jacket -> SuShi's blue scholar robe
        if v > 0.7:
            return (148, 188, 228)  # highlight sky blue
        elif v > 0.5:
            return (108, 152, 202)  # base medium blue
        elif v > 0.35:
            return (72, 112, 168)   # shadow deeper blue
        else:
            return (48, 78, 132)    # deep shadow navy

    # Default: keep original with slight blue shift
    new_h = (h + 30) % 360  # shift toward blue
    return hsv_to_rgb(new_h, s * 0.8, v)


def remap_color_zhaoyun(rgb, group):
    """Remap Penny colors to Zhaoyun (朝云) palette.
    Zhaoyun: Black hair with gold ornament, pink clothes, fair skin.
    """
    r, g, b = rgb[:3]
    h, s, v = rgb_to_hsv(r, g, b)

    if group == 'outline':
        return (50, 30, 35)

    elif group == 'skin':
        # Slightly fairer skin than Penny
        if v > 0.9:
            return (255, 232, 210)  # highlight
        elif v > 0.75:
            return (245, 214, 186)  # base
        elif v > 0.6:
            return (222, 185, 155)  # shadow
        else:
            return (198, 158, 130)  # deep shadow

    elif group == 'eye_white':
        return (255, 255, 255)

    elif group == 'hair':
        # Penny's red hair -> Zhaoyun's black hair
        if v > 0.4:
            return (62, 55, 78)   # highlight (blue sheen)
        elif v > 0.25:
            return (35, 28, 48)   # base
        else:
            return (22, 16, 32)   # shadow

    elif group == 'clothes':
        # Penny's orange/yellow -> Zhaoyun's pink
        if v > 0.8:
            return (240, 200, 210)  # light pink highlight
        elif v > 0.6:
            return (220, 150, 170)  # medium pink
        elif v > 0.4:
            return (180, 100, 130)  # deep pink
        else:
            return (140, 70, 100)   # dark pink shadow

    elif group == 'accessory':
        # Pink accents -> gold hair ornament
        if v > 0.6:
            return (255, 220, 100)  # gold highlight
        elif v > 0.4:
            return (220, 180, 60)   # gold base
        else:
            return (180, 140, 30)   # gold shadow

    elif group == 'clothes_accent':
        # Gray/blue accents -> lighter pink accent
        return (245, 215, 220)

    # Default
    new_h = 340  # shift to pink
    return hsv_to_rgb(new_h, min(s * 0.6, 0.5), v)


def remap_color_foyin(rgb, group):
    """Remap Harvey colors to Foyin (佛印) palette.
    Foyin: Bald (skin-colored head), ochre/saffron kasaya robes, stocky.
    """
    r, g, b = rgb[:3]
    h, s, v = rgb_to_hsv(r, g, b)

    if group == 'outline':
        return (50, 32, 18)

    elif group == 'skin':
        # Warm golden skin (slightly tanned monk)
        if v > 0.85:
            return (252, 225, 190)  # highlight
        elif v > 0.7:
            return (238, 202, 162)  # base
        elif v > 0.55:
            return (212, 172, 132)  # shadow
        else:
            return (188, 145, 108)  # deep shadow

    elif group == 'eye_white':
        return (255, 255, 255)

    elif group == 'hair':
        # Harvey's brown hair -> Foyin's BALD head (use skin color!)
        # This makes the hair area look like bare scalp
        if v > 0.5:
            return (255, 240, 215)  # dome highlight (shiny bald)
        elif v > 0.35:
            return (252, 225, 190)  # skin highlight
        elif v > 0.2:
            return (238, 202, 162)  # skin base
        else:
            return (212, 172, 132)  # skin shadow

    elif group == 'clothes':
        # Harvey's green -> Foyin's ochre/saffron kasaya
        if v > 0.6:
            return (225, 188, 98)   # highlight warm gold
        elif v > 0.4:
            return (198, 158, 65)   # base ochre
        elif v > 0.25:
            return (165, 125, 48)   # shadow deeper ochre
        else:
            return (132, 98, 35)    # deep shadow brown

    elif group == 'accessory':
        # Tie -> prayer beads (dark brown)
        if v > 0.4:
            return (92, 62, 35)
        else:
            return (62, 42, 22)

    elif group == 'glasses':
        # Remove glasses -> skin tone (they become part of face)
        return (238, 202, 162)

    # Default
    new_h = 40  # shift to warm ochre
    return hsv_to_rgb(new_h, min(s, 0.7), v)


def process_character(source_path, classify_fn, remap_fn, output_path):
    """Load source sprite, crop to 64x128, classify and remap each pixel."""
    img = Image.open(source_path).convert("RGBA")
    # Crop to first 4 rows (64x128) — walking animations only
    cropped = img.crop((0, 0, 64, 128))
    result = Image.new("RGBA", (64, 128), (0, 0, 0, 0))

    for y in range(128):
        for x in range(64):
            px = cropped.getpixel((x, y))
            if px[3] == 0:
                continue  # keep transparent
            rgb = px[:3]
            group = classify_fn(rgb)
            new_rgb = remap_fn(rgb, group)
            result.putpixel((x, y), (*new_rgb, px[3]))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result.save(output_path)
    return result


def process_portrait(source_path, classify_fn, remap_fn, output_path):
    """Load source portrait, crop to 128x128 (2x2 grid), classify and remap."""
    img = Image.open(source_path).convert("RGBA")
    # Crop to first 2x2 grid (128x128)
    cropped = img.crop((0, 0, 128, 128))
    result = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

    for y in range(128):
        for x in range(128):
            px = cropped.getpixel((x, y))
            if px[3] == 0:
                continue
            rgb = px[:3]
            group = classify_fn(rgb)
            new_rgb = remap_fn(rgb, group)
            result.putpixel((x, y), (*new_rgb, px[3]))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result.save(output_path)
    return result


def apply_sushi_turban(img):
    """Modify SuShi's sprite to reshape Sebastian's emo hair into a Dongpo turban.
    The turban is a flat-topped rectangular cap — we flatten the top of the hair area.
    """
    # For each frame (4 frames per row, 4 rows)
    for row in range(4):
        for frame in range(4):
            ox = frame * 16
            oy = row * 32
            # Find the topmost non-transparent pixel in this frame's head area (y0-y10)
            top_y = None
            for y in range(0, 11):
                for x in range(16):
                    px = img.getpixel((ox + x, oy + y))
                    if px[3] > 0:
                        if top_y is None:
                            top_y = y
                        break
                if top_y is not None:
                    break

            if top_y is None:
                continue

            # Make the top of the hat flat by filling in gaps at the top row
            # Find leftmost and rightmost non-transparent pixels in the hat area
            hat_left = 16
            hat_right = 0
            for y in range(top_y, min(top_y + 4, 11)):
                for x in range(16):
                    px = img.getpixel((ox + x, oy + y))
                    if px[3] > 0:
                        hat_left = min(hat_left, x)
                        hat_right = max(hat_right, x)

            # Fill the top row to make it flat (rectangular turban shape)
            turban_color = (30, 28, 42, 255)  # dark blue-black base
            turban_highlight = (52, 50, 68, 255)
            outline_color = (38, 28, 18, 255)

            if hat_right > hat_left:
                # Top outline row
                for x in range(hat_left, hat_right + 1):
                    px = img.getpixel((ox + x, oy + top_y))
                    if px[3] == 0:
                        img.putpixel((ox + x, oy + top_y), outline_color)
                # Fill second row for flat top
                if top_y + 1 < 11:
                    for x in range(hat_left + 1, hat_right):
                        px = img.getpixel((ox + x, oy + top_y + 1))
                        # Make it flat — fill with turban color
                        if px[3] == 0:
                            img.putpixel((ox + x, oy + top_y + 1), turban_color)

    return img


def apply_foyin_bald(img):
    """Modify Foyin's sprite to remove Harvey's hair and make it bald (skin-colored).
    We identify the hair region (top of head above face) and replace with skin tones.
    """
    # Skin colors for the bald dome
    skin_highlight = (255, 240, 215, 255)
    skin_base = (252, 225, 190, 255)
    skin_shadow = (238, 202, 162, 255)

    for row in range(4):
        for frame in range(4):
            ox = frame * 16
            oy = row * 32
            # The hair region is typically y0-y5 in each frame
            # We want to keep the outline but change hair interior to skin
            for y in range(0, 7):
                for x in range(16):
                    px = img.getpixel((ox + x, oy + y))
                    if px[3] == 0:
                        continue
                    r, g, b = px[:3]
                    # Check if this pixel looks like it was remapped to "bald" skin
                    # (from the remap_color_foyin function, hair -> skin tones)
                    # The remap already converts hair to skin, so we just need to
                    # ensure the dome looks smooth and shiny
                    h, s, v = rgb_to_hsv(r, g, b)
                    # If it's a warm skin-like color in the top area, add dome shine
                    if 20 < h < 50 and s < 0.4 and v > 0.7:
                        # Add a highlight gradient (brighter at top)
                        brightness_factor = 1.0 + (7 - y) * 0.03
                        new_v = min(1.0, v * brightness_factor)
                        new_rgb = hsv_to_rgb(h, s * 0.8, new_v)
                        img.putpixel((ox + x, oy + y), (*new_rgb, px[3]))

    return img


def verify_output(path, expected_size, name):
    """Verify output file exists and has correct dimensions."""
    if not os.path.exists(path):
        print(f"  FAIL: {name} not found at {path}")
        return False
    img = Image.open(path)
    if img.size != expected_size:
        print(f"  FAIL: {name} size {img.size} != expected {expected_size}")
        return False
    # Count non-transparent pixels
    non_empty = sum(1 for y in range(img.size[1]) for x in range(img.size[0])
                    if img.getpixel((x, y))[3] > 0)
    if non_empty < 100:
        print(f"  FAIL: {name} has only {non_empty} non-transparent pixels")
        return False
    print(f"  OK: {name} — {img.size}, {non_empty} non-transparent pixels")
    return True


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Generating character sprites from official NPC templates")
    print("=" * 60)

    os.makedirs(CHAR_OUT_DIR, exist_ok=True)
    os.makedirs(PORT_OUT_DIR, exist_ok=True)

    # === Character definitions ===
    characters = [
        {
            "name": "SuShi",
            "source_char": "Characters_Sebastian.png",
            "source_port": "Portraits_Sebastian.png",
            "classify": classify_pixel_sebastian,
            "remap": remap_color_sushi,
            "post_process": apply_sushi_turban,
        },
        {
            "name": "Zhaoyun",
            "source_char": "Characters_Penny.png",
            "source_port": "Portraits_Penny.png",
            "classify": classify_pixel_penny,
            "remap": remap_color_zhaoyun,
            "post_process": None,
        },
        {
            "name": "Foyin",
            "source_char": "Characters_Harvey.png",
            "source_port": "Portraits_Harvey.png",
            "classify": classify_pixel_harvey,
            "remap": remap_color_foyin,
            "post_process": apply_foyin_bald,
        },
    ]

    all_ok = True

    for char in characters:
        print(f"\n--- {char['name']} ---")
        source_char_path = os.path.join(SOURCE_DIR, char["source_char"])
        source_port_path = os.path.join(SOURCE_DIR, char["source_port"])
        out_char_path = os.path.join(CHAR_OUT_DIR, f"{char['name']}.png")
        out_port_path = os.path.join(PORT_OUT_DIR, f"{char['name']}.png")

        # Check source exists
        if not os.path.exists(source_char_path):
            print(f"  ERROR: Source not found: {source_char_path}")
            all_ok = False
            continue
        if not os.path.exists(source_port_path):
            print(f"  ERROR: Source not found: {source_port_path}")
            all_ok = False
            continue

        # Process character sprite
        print(f"  Processing character sprite from {char['source_char']}...")
        char_img = process_character(
            source_char_path, char["classify"], char["remap"], out_char_path
        )
        # Apply post-processing (shape modifications)
        if char["post_process"]:
            char_img = char["post_process"](char_img)
            char_img.save(out_char_path)
            print(f"  Applied post-processing: {char['post_process'].__name__}")

        # Process portrait
        print(f"  Processing portrait from {char['source_port']}...")
        process_portrait(
            source_port_path, char["classify"], char["remap"], out_port_path
        )

    # === Verification ===
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    for char in characters:
        out_char_path = os.path.join(CHAR_OUT_DIR, f"{char['name']}.png")
        out_port_path = os.path.join(PORT_OUT_DIR, f"{char['name']}.png")
        ok1 = verify_output(out_char_path, (64, 128), f"{char['name']} character")
        ok2 = verify_output(out_port_path, (128, 128), f"{char['name']} portrait")
        if not (ok1 and ok2):
            all_ok = False

    # Check animation frames differ
    print("\nAnimation check:")
    for char in characters:
        out_char_path = os.path.join(CHAR_OUT_DIR, f"{char['name']}.png")
        if not os.path.exists(out_char_path):
            continue
        img = Image.open(out_char_path)
        dirs = ["Front", "Right", "Back", "Left"]
        for row_idx, dir_name in enumerate(dirs):
            frame0 = []
            frame1 = []
            for y in range(32):
                for x in range(16):
                    frame0.append(img.getpixel((x, row_idx * 32 + y)))
                    frame1.append(img.getpixel((16 + x, row_idx * 32 + y)))
            diffs = sum(1 for a, b in zip(frame0, frame1) if a != b)
            if diffs == 0:
                print(f"  WARNING: {char['name']} {dir_name} — no animation difference!")
            else:
                print(f"  {char['name']} {dir_name}: {diffs} pixel diffs between frames")

    if all_ok:
        print("\nAll characters generated successfully!")
    else:
        print("\nSome issues detected — check output above.")

    sys.exit(0 if all_ok else 1)
