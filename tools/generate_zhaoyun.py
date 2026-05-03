#!/usr/bin/env python3
"""Generate improved Zhaoyun (朝云) sprite sheet and portrait for Stardew Valley mod."""

from PIL import Image

# === COLOR PALETTE (with hue shifting) ===
T = (0, 0, 0, 0)  # transparent

# Outline colors (colored, not pure black)
OL_DARK = (35, 20, 28, 255)    # deep plum-brown, main outline
OL_MED  = (55, 35, 42, 255)    # medium outline for inner details
OL_HAIR = (25, 18, 35, 255)    # dark blue-black for hair outline

# Skin (warm, top-left lighting)
SK_HI  = (252, 228, 205, 255)  # highlight - warm yellow
SK_BASE = (242, 210, 178, 255) # base
SK_SH  = (215, 175, 142, 255)  # shadow - shifts red
SK_DSH = (190, 140, 115, 255)  # deep shadow

# Hair (black with blue sheen)
HR_HI  = (55, 50, 70, 255)     # highlight - blue sheen
HR_BASE = (30, 25, 40, 255)    # base - very dark blue-black
HR_SH  = (20, 15, 28, 255)     # shadow

# Pink clothing (Song dynasty style)
CL_HI  = (248, 220, 225, 255)  # highlight - white-pink
CL_BASE = (235, 175, 190, 255) # base - rose pink
CL_SH  = (200, 130, 155, 255)  # shadow - shifts magenta
CL_DSH = (165, 95, 125, 255)   # deep shadow - plum

# Sash/belt accent
SA_HI  = (220, 195, 80, 255)   # gold highlight
SA_BASE = (195, 170, 60, 255)  # gold base
SA_SH  = (160, 135, 45, 255)   # gold shadow

# Hair ornament (golden)
HO_HI  = (245, 220, 100, 255)
HO_BASE = (218, 188, 72, 255)
HO_SH  = (180, 150, 50, 255)

# Lips
LIP = (215, 150, 145, 255)

# Eye colors
EYE_DARK = (30, 20, 25, 255)
EYE_IRIS = (80, 45, 55, 255)   # dark brown-red iris
EYE_HI   = (255, 255, 255, 255) # white highlight

# Shoe
SH_BASE = (140, 90, 110, 255)
SH_SH   = (110, 65, 85, 255)

# Shorthand aliases
O = OL_DARK
M = OL_MED
H = OL_HAIR
s0 = SK_HI
s1 = SK_BASE
s2 = SK_SH
s3 = SK_DSH
h0 = HR_HI
h1 = HR_BASE
h2 = HR_SH
c0 = CL_HI
c1 = CL_BASE
c2 = CL_SH
c3 = CL_DSH
sa0 = SA_HI
sa1 = SA_BASE
sa2 = SA_SH
ho0 = HO_HI
ho1 = HO_BASE
ho2 = HO_SH
lp = LIP
ed = EYE_DARK
ei = EYE_IRIS
eh = EYE_HI
sh0 = SH_BASE
sh1 = SH_SH

# === CHARACTER SPRITE (16x32 per frame) ===
# Redesigned with wider proportions matching original style
# Long flowing hair, wider skirt, proper Song dynasty look

# Front-facing standing frame (facing down/south)
FRONT_STAND = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    [T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T],  # y0
    [T, T, T, T, T, H, ho1,ho0,ho0,ho1,H, T, T, T, T, T],  # y1 ornament
    [T, T, T, T, H, h0,h1,h1,h1,h1,h1,H, T, T, T, T],  # y2 hair top
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y3 hair
    [T, T, T, H, h0,s0,s0,s1,s1,s1,s2,h2,H, T, T, T],  # y4 forehead
    [T, T, T, H, h0,s0,s1,s1,s1,s1,s2,h2,H, T, T, T],  # y5 upper face
    [T, T, T, H, h0,s0,ed,s1,s1,ed,s1,s2,H, T, T, T],  # y6 eye top (lash line)
    [T, T, T, H, s0,eh,ei,s1,s1,ei,ed,s2,H, T, T, T],  # y7 eye bottom (iris+highlight)
    [T, T, T, H, s1,s1,s1,s2,s1,s1,s1,s2,H, T, T, T],  # y8 nose
    [T, T, T, H, s1,s1,s1,lp,lp,s1,s1,s3,H, T, T, T],  # y9 mouth
    [T, T, T, H, h1,s2,s1,s1,s1,s1,s2,h2,H, T, T, T],  # y10 chin + hair sides
    [T, T, T, H, h1,h1,s2,s2,s2,s2,h1,h2,H, T, T, T],  # y11 jaw + hair
    [T, T, H, h1,h0,c0,c1,s2,s2,c1,c1,h1,h2,H, T, T],  # y12 neck + collar + hair
    [T, T, H, h1,c0,c1,c1,c1,c1,c1,c1,c2,h2,H, T, T],  # y13 upper body + hair
    [T, O, H, h1,c0,c1,sa0,sa1,sa1,sa0,c1,c2,h2,H, O, T],  # y14 sash + hair
    [T, O, H, h1,c0,c1,sa1,sa2,sa2,sa1,c1,c2,h2,H, O, T],  # y15 sash lower
    [T, O, H, h0,c0,c1,c1,c1,c1,c1,c1,c2,h2,H, O, T],  # y16 waist
    [T, O, H, h0,c0,c1,c1,c1,c1,c1,c1,c2,h2,H, O, T],  # y17 hip
    [T, O, H, h0,c0,c1,c1,c2,c2,c1,c1,c2,h2,H, O, T],  # y18 skirt fold
    [T, O, H, h1,c0,c1,c1,c1,c1,c1,c2,c2,h2,H, O, T],  # y19 skirt
    [T, T, H, h1,c0,c1,c1,c2,c2,c1,c2,c3,h2,H, T, T],  # y20 skirt lower
    [T, T, H, h1,c1,c1,c2,c1,c1,c2,c2,c3,h2,H, T, T],  # y21 skirt
    [T, T, T, H, c1,c2,c2,c2,c2,c2,c2,c3,H, T, T, T],  # y22 skirt hem
    [T, T, T, H, c1,c2,c2,c3,c3,c2,c3,c3,H, T, T, T],  # y23 skirt bottom
    [T, T, T, T, O, c2,c3,c3,c3,c3,c3,O, T, T, T, T],  # y24 skirt tip
    [T, T, T, T, T, O, c3,O, O, c3,O, T, T, T, T, T],  # y25 ankles
    [T, T, T, T, T, O,sh0,sh1,sh1,sh0,O, T, T, T, T],  # y26 shoes
    [T, T, T, T, T, T, O, O, O, O, T, T, T, T, T, T],  # y27 shoe bottom
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y28
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y29
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y30
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y31
]

# Right-facing standing frame - wider body, hair behind on left
RIGHT_STAND = [
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y0
    [T, T, T, T, T, H, ho1,ho0,ho0,H, T, T, T, T, T, T],  # y1 ornament
    [T, T, T, T, H, h1,h1,h1,h1,h1,H, T, T, T, T, T],  # y2
    [T, T, T, H, h1,h1,h1,h1,h1,h1,h1,H, T, T, T, T],  # y3
    [T, T, T, H, h1,h1,s0,s1,s1,s1,h1,H, T, T, T, T],  # y4 forehead
    [T, T, T, H, h1,s0,s1,s1,s1,s1,s2,H, T, T, T, T],  # y5
    [T, T, T, H, h1,s1,s1,ed,s1,s1,s2,H, T, T, T, T],  # y6 eye top
    [T, T, T, H, h1,s1,s1,ei,eh,s1,s2,H, T, T, T, T],  # y7 eye bottom
    [T, T, T, H, h1,s1,s1,s1,s2,s2,s2,H, T, T, T, T],  # y8 nose
    [T, T, T, H, h1,s1,s1,lp,s1,s2,s3,H, T, T, T, T],  # y9 mouth
    [T, T, T, H, h1,s2,s1,s1,s1,s2,h1,H, T, T, T, T],  # y10 chin
    [T, T, T, H, h1,h1,s2,s2,s2,h1,h1,H, T, T, T, T],  # y11 jaw
    [T, T, H, h1,c0,c0,c1,s2,c1,c1,c2,c2,H, T, T, T],  # y12 collar
    [T, O, H, h1,c0,c1,c1,c1,c1,c1,c1,c2,H, O, T, T],  # y13 body
    [T, O, H, h1,c0,c1,sa0,sa1,sa1,c1,c1,c2,H, O, T, T],  # y14 sash
    [T, O, H, h0,c0,c1,sa1,sa2,sa2,c1,c1,c2,H, O, T, T],  # y15
    [T, O, H, h0,c0,c1,c1,c1,c1,c1,c1,c2,H, O, T, T],  # y16
    [T, O, H, h0,c0,c1,c1,c1,c1,c1,c2,c2,H, O, T, T],  # y17
    [T, O, H, h0,c0,c1,c1,c2,c1,c1,c2,c2,H, O, T, T],  # y18 fold
    [T, O, H, h1,c0,c1,c1,c1,c1,c2,c2,c3,H, O, T, T],  # y19
    [T, T, H, h1,c1,c1,c2,c2,c1,c2,c3,c3,H, T, T, T],  # y20
    [T, T, H, h1,c1,c2,c2,c1,c2,c2,c3,c3,H, T, T, T],  # y21
    [T, T, T, H, c1,c2,c2,c2,c2,c3,c3,H, T, T, T, T],  # y22
    [T, T, T, T, H, c2,c3,c3,c3,c3,H, T, T, T, T, T],  # y23
    [T, T, T, T, T, O, c3,c3,c3,O, T, T, T, T, T, T],  # y24
    [T, T, T, T, T, O, c3,O, O,sh0,O, T, T, T, T, T],  # y25
    [T, T, T, T, T, T, O,sh0,sh1,sh0,O, T, T, T, T, T],  # y26
    [T, T, T, T, T, T, T, O, O, O, T, T, T, T, T, T],  # y27
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y28
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y29
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y30
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y31
]

# Back-facing standing frame - hair center strip, clothing visible on sides
BACK_STAND = [
    [T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T],  # y0
    [T, T, T, T, T, H, ho1,ho0,ho0,ho1,H, T, T, T, T, T],  # y1 ornament
    [T, T, T, T, H, h0,h1,h1,h1,h1,h1,H, T, T, T, T],  # y2
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y3
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y4
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y5
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y6
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y7
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y8
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y9
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y10
    [T, T, T, H, h0,h1,h1,h1,h1,h1,h1,h2,H, T, T, T],  # y11
    [T, T, H, h1,c0,c0,h1,h1,h1,h1,c1,c2,h2,H, T, T],  # y12 collar + hair
    [T, O, H, c0,c0,c1,h0,h1,h1,h1,c1,c2,c2,H, O, T],  # y13 body + hair
    [T, O, H, c0,c0,c1,h0,h1,h1,h1,c1,c2,c2,H, O, T],  # y14
    [T, O, H, c0,c0,c1,sa1,h1,h1,sa1,c1,c2,c2,H, O, T],  # y15 sash
    [T, O, H, c0,c0,c1,h0,h1,h1,h1,c1,c2,c2,H, O, T],  # y16
    [T, O, H, c0,c0,c1,h0,h1,h1,h1,c1,c2,c2,H, O, T],  # y17
    [T, O, H, c0,c0,c1,h0,h1,h1,h1,c1,c2,c2,H, O, T],  # y18
    [T, O, H, c0,c1,c1,h0,h1,h1,h1,c2,c2,c3,H, O, T],  # y19
    [T, T, H, c1,c1,c2,h0,h1,h1,h2,c2,c3,c3,H, T, T],  # y20
    [T, T, H, c1,c1,c2,h0,h1,h1,h2,c2,c3,c3,H, T, T],  # y21
    [T, T, T, H, c1,c2,h0,h1,h1,h2,c2,c3,H, T, T, T],  # y22
    [T, T, T, H, c1,c2,c2,h1,h1,c3,c3,c3,H, T, T, T],  # y23
    [T, T, T, T, O, c2,c3,c3,c3,c3,c3,O, T, T, T, T],  # y24
    [T, T, T, T, T, O, c3,O, O, c3,O, T, T, T, T, T],  # y25
    [T, T, T, T, T, O,sh0,sh1,sh1,sh0,O, T, T, T, T],  # y26
    [T, T, T, T, T, T, O, O, O, O, T, T, T, T, T, T],  # y27
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y28
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y29
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y30
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y31
]

# Left-facing: mirror of right-facing
def mirror_frame(frame):
    return [list(reversed(row)) for row in frame]

LEFT_STAND = mirror_frame(RIGHT_STAND)


def make_walk_frame(stand, step_side, direction):
    """Generate a walk frame from standing frame.
    Head bobs down 1px, feet shift to show stepping.
    """
    import copy
    frame = copy.deepcopy(stand)

    # Find the first non-empty row (top of sprite)
    first_row = 0
    for i, row in enumerate(frame):
        if any(c != T for c in row):
            first_row = i
            break

    # Head bob: shift rows first_row..12 down by 1px (insert empty row at top)
    body_start = 12
    head_rows = frame[first_row:body_start]
    for i in range(first_row, body_start):
        frame[i] = [T] * 16
    for i, row in enumerate(head_rows):
        if first_row + i + 1 < body_start + 1:
            frame[first_row + i + 1] = row

    # Leg animation: wider stride, modify skirt bottom + feet (y23-y27)
    if direction in ('front', 'back'):
        if step_side == 'left':
            frame[23] = [T,T,T,H,c1,c2,c2,c3,c3,c2,c3,c3,H,T,T,T]
            frame[24] = [T,T,T,O,c2,c3,c3,T,T,c3,c3,c3,O,T,T,T]
            frame[25] = [T,T,T,O,sh0,O,T,T,T,T,T,O,sh0,O,T,T]
            frame[26] = [T,T,T,O,sh0,sh1,O,T,T,T,O,sh0,sh1,O,T,T]
            frame[27] = [T,T,T,T,O,O,T,T,T,T,T,O,O,T,T,T]
        else:
            frame[23] = [T,T,T,H,c1,c2,c2,c3,c3,c2,c3,c3,H,T,T,T]
            frame[24] = [T,T,O,c2,c3,c3,T,T,T,T,c3,c3,O,T,T,T]
            frame[25] = [T,O,sh0,O,T,T,T,T,T,T,T,O,sh0,O,T,T]
            frame[26] = [T,O,sh0,sh1,O,T,T,T,T,T,O,sh0,sh1,O,T,T]
            frame[27] = [T,T,O,O,T,T,T,T,T,T,T,O,O,T,T,T]
    elif direction == 'right':
        if step_side == 'left':
            frame[23] = [T,T,T,T,H,c2,c3,c3,c3,c3,H,T,T,T,T,T]
            frame[24] = [T,T,T,T,O,c3,c3,c3,O,T,T,T,T,T,T,T]
            frame[25] = [T,T,T,O,sh0,O,T,T,O,sh0,O,T,T,T,T,T]
            frame[26] = [T,T,T,O,sh0,sh1,O,T,O,sh0,sh1,O,T,T,T,T]
            frame[27] = [T,T,T,T,O,O,T,T,T,O,O,T,T,T,T,T]
        else:
            frame[23] = [T,T,T,T,H,c2,c3,c3,c3,c3,H,T,T,T,T,T]
            frame[24] = [T,T,T,T,T,T,O,c3,c3,c3,O,T,T,T,T,T]
            frame[25] = [T,T,T,T,T,O,sh0,O,T,O,sh0,O,T,T,T,T]
            frame[26] = [T,T,T,T,O,sh0,sh1,O,T,O,sh0,sh1,O,T,T,T]
            frame[27] = [T,T,T,T,T,O,O,T,T,T,O,O,T,T,T,T]
    elif direction == 'left':
        if step_side == 'left':
            frame[23] = [T,T,T,T,T,H,c3,c3,c3,c2,H,T,T,T,T,T]
            frame[24] = [T,T,T,T,T,T,O,c3,c3,c3,O,T,T,T,T,T]
            frame[25] = [T,T,T,T,T,O,sh0,O,T,O,sh0,O,T,T,T,T]
            frame[26] = [T,T,T,T,O,sh0,sh1,O,T,O,sh0,sh1,O,T,T,T]
            frame[27] = [T,T,T,T,T,O,O,T,T,T,O,O,T,T,T,T]
        else:
            frame[23] = [T,T,T,T,T,H,c3,c3,c3,c2,H,T,T,T,T,T]
            frame[24] = [T,T,T,T,O,c3,c3,c3,O,T,T,T,T,T,T,T]
            frame[25] = [T,T,T,O,sh0,O,T,T,O,sh0,O,T,T,T,T,T]
            frame[26] = [T,T,T,O,sh0,sh1,O,T,O,sh0,sh1,O,T,T,T,T]
            frame[27] = [T,T,T,T,O,O,T,T,T,O,O,T,T,T,T,T]

    return frame


def paint_frame(img, frame_data, offset_x, offset_y):
    """Paint a 16x32 frame onto the image at the given offset."""
    for y, row in enumerate(frame_data):
        for x, color in enumerate(row):
            if color != T:
                img.putpixel((offset_x + x, offset_y + y), color)


def generate_character_sheet():
    """Generate the 64x128 character sprite sheet."""
    img = Image.new("RGBA", (64, 128), (0, 0, 0, 0))

    directions = [
        ("front", FRONT_STAND),
        ("right", RIGHT_STAND),
        ("back",  BACK_STAND),
        ("left",  LEFT_STAND),
    ]

    for row_idx, (dir_name, stand_frame) in enumerate(directions):
        base_y = row_idx * 32
        # Frame 0: standing
        paint_frame(img, stand_frame, 0, base_y)
        # Frame 1: walk left foot
        walk_l = make_walk_frame(stand_frame, 'left', dir_name)
        paint_frame(img, walk_l, 16, base_y)
        # Frame 2: standing (same as frame 0)
        paint_frame(img, stand_frame, 32, base_y)
        # Frame 3: walk right foot
        walk_r = make_walk_frame(stand_frame, 'right', dir_name)
        paint_frame(img, walk_r, 48, base_y)

    return img


def generate_portrait_default(img, ox, oy):
    """Draw the default expression portrait at offset (ox, oy) in 64x64.
    Wider face, long flowing hair, detailed clothing with collar and sash.
    """
    def p(x, y, c):
        if 0 <= x < 64 and 0 <= y < 64:
            img.putpixel((ox + x, oy + y), c)

    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)

    def fill_rect(x1, y1, x2, y2, c):
        for yy in range(y1, y2 + 1):
            hline(x1, x2, yy, c)

    # --- Hair (long, flowing past shoulders) ---
    # Hair top dome
    fill_rect(20, 2, 43, 3, h1)
    fill_rect(18, 4, 45, 7, h1)
    # Hair highlight (left, light source top-left)
    fill_rect(20, 2, 28, 6, h0)
    # Hair sides flowing down (long hair to y52)
    fill_rect(14, 8, 19, 50, h1)   # left hair
    fill_rect(44, 8, 49, 50, h2)   # right hair
    # Hair highlight on left side
    fill_rect(14, 8, 16, 35, h0)
    # Hair tips taper
    fill_rect(15, 51, 18, 52, h1)
    fill_rect(45, 51, 48, 52, h2)
    fill_rect(16, 53, 17, 54, h1)
    fill_rect(46, 53, 47, 54, h2)

    # Hair outline
    hline(20, 43, 1, H)
    for y in range(2, 4):
        p(19, y, H); p(44, y, H)
    for y in range(4, 8):
        p(17, y, H); p(46, y, H)
    for y in range(8, 51):
        p(13, y, H); p(50, y, H)
    for y in range(51, 53):
        p(14, y, H); p(49, y, H)
    for y in range(53, 55):
        p(15, y, H); p(48, y, H)

    # --- Hair ornament (golden hairpin) ---
    hline(28, 35, 0, ho0)
    fill_rect(27, 1, 36, 2, ho1)
    hline(28, 35, 3, ho2)

    # --- Face ---
    fill_rect(20, 8, 43, 30, s1)
    # Forehead highlight
    fill_rect(20, 8, 32, 13, s0)
    # Right face shadow
    fill_rect(39, 8, 43, 30, s2)
    # Chin area shadow
    fill_rect(22, 28, 41, 30, s2)
    hline(24, 39, 30, s3)

    # --- Eyebrows ---
    hline(23, 27, 14, M)
    hline(35, 39, 14, M)

    # --- Eyes (3x3 with iris and highlight) ---
    # Left eye
    p(23, 16, ed); p(24, 16, ed); p(25, 16, ed); p(26, 16, ed)
    p(23, 17, eh); p(24, 17, ei); p(25, 17, ei); p(26, 17, ed)
    p(23, 18, ed); p(24, 18, ed); p(25, 18, ed); p(26, 18, ed)
    # Right eye
    p(36, 16, ed); p(37, 16, ed); p(38, 16, ed); p(39, 16, ed)
    p(36, 17, ed); p(37, 17, ei); p(38, 17, ei); p(39, 17, eh)
    p(36, 18, ed); p(37, 18, ed); p(38, 18, ed); p(39, 18, ed)

    # --- Nose ---
    p(31, 21, s2); p(32, 21, s3)
    p(31, 22, s3)

    # --- Mouth ---
    hline(29, 34, 24, lp)
    hline(30, 33, 25, LIP)

    # --- Neck ---
    fill_rect(27, 31, 36, 34, s1)
    fill_rect(27, 31, 32, 32, s0)
    fill_rect(34, 31, 36, 34, s2)

    # --- Clothing ---
    # Collar (V-neck style, Song dynasty)
    fill_rect(20, 35, 43, 37, c1)
    hline(20, 28, 35, c0)
    hline(35, 43, 35, c2)
    # V-collar lines
    for i in range(3):
        p(29 - i, 35 + i, s2)
        p(34 + i, 35 + i, s2)

    # Body
    fill_rect(14, 38, 49, 58, c1)
    fill_rect(14, 38, 22, 58, c0)
    fill_rect(42, 38, 49, 58, c2)

    # Sash/belt
    fill_rect(24, 42, 39, 45, sa1)
    hline(24, 32, 42, sa0)
    hline(33, 39, 44, sa2)
    hline(24, 39, 45, sa2)

    # Clothing folds
    for y in range(48, 58):
        p(28, y, c2)
        p(35, y, c2)

    # Bottom clothing
    fill_rect(14, 58, 49, 63, c2)
    fill_rect(14, 58, 22, 63, c1)
    fill_rect(42, 58, 49, 63, c3)

    # Clothing outline
    for y in range(35, 63):
        p(13, y, O)
        p(50, y, O)
    hline(13, 50, 63, O)


def generate_portrait_happy(img, ox, oy):
    """Happy expression - closed eyes, wider smile."""
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    # Clear default eyes and redraw as happy ^_^
    for x in range(23, 27):
        p(x, 16, s1); p(x, 18, s1)
    for x in range(36, 40):
        p(x, 16, s1); p(x, 18, s1)
    # Curved happy eyes
    p(23, 17, M); p(24, 16, M); p(25, 16, M); p(26, 17, M)
    p(36, 17, M); p(37, 16, M); p(38, 16, M); p(39, 17, M)
    # Wider smile
    p(28, 24, lp); p(35, 24, lp)
    p(29, 25, lp); p(34, 25, lp)


def generate_portrait_sad(img, ox, oy):
    """Sad expression - angled brows, downturned mouth."""
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    # Sad eyebrows (angled down toward center)
    for x in range(23, 28):
        p(x, 14, s1)
    for x in range(35, 40):
        p(x, 14, s1)
    p(24, 13, M); p(25, 13, M); p(26, 14, M); p(27, 14, M)
    p(38, 13, M); p(37, 13, M); p(36, 14, M); p(35, 14, M)
    # Downturned mouth
    for x in range(29, 35):
        p(x, 24, s1)
    p(29, 24, lp); p(34, 24, lp)
    p(28, 25, lp); p(35, 25, lp)
    for x in range(29, 35):
        p(x, 25, lp)


def generate_portrait_surprised(img, ox, oy):
    """Surprised expression - raised brows, open mouth."""
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    # Raised eyebrows (higher up)
    for x in range(23, 28):
        p(x, 14, s1)
    for x in range(35, 40):
        p(x, 14, s1)
    for x in range(23, 28):
        p(x, 13, M)
    for x in range(35, 40):
        p(x, 13, M)
    # Open mouth (O shape)
    for x in range(29, 35):
        p(x, 24, s1)
    p(30, 24, ed); p(31, 24, ed); p(32, 24, ed); p(33, 24, ed)
    p(30, 25, ed); p(31, 25, lp); p(32, 25, lp); p(33, 25, ed)
    p(30, 26, ed); p(31, 26, ed); p(32, 26, ed); p(33, 26, ed)


def generate_portrait_sheet():
    """Generate 128x128 portrait sheet (2x2 grid of 64x64)."""
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

    generate_portrait_default(img, 0, 0)      # top-left
    generate_portrait_happy(img, 64, 0)        # top-right
    generate_portrait_sad(img, 0, 64)          # bottom-left
    generate_portrait_surprised(img, 64, 64)   # bottom-right

    return img


# === MAIN ===
if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    char_path = os.path.join(base_dir, "assets", "Characters", "Zhaoyun.png")
    port_path = os.path.join(base_dir, "assets", "Portraits", "Zhaoyun.png")

    # Backup originals
    for path in [char_path, port_path]:
        backup = path + ".bak"
        if os.path.exists(path) and not os.path.exists(backup):
            import shutil
            shutil.copy2(path, backup)
            print(f"Backed up: {backup}")

    # Generate
    char_img = generate_character_sheet()
    char_img.save(char_path)
    print(f"Character sprite saved: {char_path} ({char_img.size})")

    port_img = generate_portrait_sheet()
    port_img.save(port_path)
    print(f"Portrait saved: {port_path} ({port_img.size})")

    # Verification
    verify_char = Image.open(char_path)
    verify_port = Image.open(port_path)
    print(f"\nVerification:")
    print(f"  Character: {verify_char.size} mode={verify_char.mode}")
    print(f"  Portrait:  {verify_port.size} mode={verify_port.mode}")

    # Check walk animation has different frames
    for row in range(4):
        frame0 = []
        frame1 = []
        for y in range(32):
            for x in range(16):
                frame0.append(verify_char.getpixel((x, row*32+y)))
                frame1.append(verify_char.getpixel((16+x, row*32+y)))
        diffs = sum(1 for a, b in zip(frame0, frame1) if a != b)
        dirs = ["Front", "Right", "Back", "Left"]
        print(f"  {dirs[row]}: frame0 vs frame1 = {diffs} pixel diffs {'OK' if diffs > 0 else 'NO ANIMATION!'}")
