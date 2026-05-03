#!/usr/bin/env python3
"""Generate improved Foyin (佛印) sprite sheet and portrait for Stardew Valley mod.

Foyin is a Northern Song dynasty Buddhist monk, Su Shi's close friend.
Key visual traits: BALD head, saffron/orange kasaya robes, stocky/round build,
kind face with slightly squinting eyes.
"""

from PIL import Image

# === COLOR PALETTE (with hue shifting, top-left light source) ===
T = (0, 0, 0, 0)  # transparent

# Outline colors (warm brown tones, not pure black)
OL_DARK = (45, 28, 15, 255)    # deep warm brown, main outline
OL_MED  = (65, 42, 25, 255)    # medium outline for inner details

# Skin (warm, slightly tanned monk - top-left lighting)
SK_HI  = (248, 220, 185, 255)  # highlight - warm golden
SK_BASE = (235, 198, 158, 255) # base
SK_SH  = (210, 168, 128, 255)  # shadow - shifts orange
SK_DSH = (185, 138, 105, 255)  # deep shadow

# Bald head sheen (subtle highlight on dome)
HD_HI  = (255, 235, 200, 255)  # bright sheen on bald head

# Kasaya / robe (saffron-orange, Song dynasty monk)
CL_HI  = (245, 205, 95, 255)   # highlight - bright saffron
CL_BASE = (218, 168, 58, 255)  # base - warm orange-gold
CL_SH  = (182, 132, 42, 255)   # shadow - deeper orange
CL_DSH = (148, 105, 35, 255)   # deep shadow - brown-orange

# Inner robe / collar (darker earth brown)
IR_HI  = (165, 120, 65, 255)   # inner robe highlight
IR_BASE = (138, 95, 48, 255)   # inner robe base
IR_SH  = (110, 72, 35, 255)    # inner robe shadow

# Prayer beads (dark wood)
BD_HI  = (95, 65, 35, 255)     # bead highlight
BD_BASE = (68, 45, 25, 255)    # bead base

# Eye colors (kind, slightly squinting)
EYE_DARK = (35, 22, 15, 255)
EYE_IRIS = (75, 48, 28, 255)   # warm brown iris
EYE_HI   = (255, 252, 245, 255) # warm white highlight

# Sandal / shoe
SN_BASE = (125, 85, 45, 255)
SN_SH   = (95, 62, 32, 255)

# Shorthand aliases
O = OL_DARK
M = OL_MED
s0 = SK_HI
s1 = SK_BASE
s2 = SK_SH
s3 = SK_DSH
hd = HD_HI
c0 = CL_HI
c1 = CL_BASE
c2 = CL_SH
c3 = CL_DSH
ir0 = IR_HI
ir1 = IR_BASE
ir2 = IR_SH
bd0 = BD_HI
bd1 = BD_BASE
ed = EYE_DARK
ei = EYE_IRIS
eh = EYE_HI
sn0 = SN_BASE
sn1 = SN_SH

# === CHARACTER SPRITE (16x32 per frame) ===
# Foyin: bald monk, stocky build, wide kasaya robes
# Wider body than Zhaoyun (uses cols 2-13 instead of 3-12)

# Front-facing standing frame (facing down/south)
# Bald dome, wide body, kasaya robes, prayer beads
FRONT_STAND = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    [T, T, T, T, T, T, O, O, O, O, T, T, T, T, T, T],  # y0  head top outline
    [T, T, T, T, T, O, hd,s0,s0,hd,O, T, T, T, T, T],  # y1  bald dome sheen
    [T, T, T, T, O, hd,s0,s0,s0,s0,s1,O, T, T, T, T],  # y2  bald dome
    [T, T, T, O, s0,s0,s1,s1,s1,s1,s1,s2,O, T, T, T],  # y3  upper head
    [T, T, T, O, s0,s0,s1,s1,s1,s1,s1,s2,O, T, T, T],  # y4  forehead
    [T, T, T, O, s0,s1,s1,s1,s1,s1,s1,s2,O, T, T, T],  # y5  upper face
    [T, T, T, O, s0,s1,ed,s1,s1,ed,s1,s2,O, T, T, T],  # y6  eye top (lash)
    [T, T, T, O, s0,eh,ei,s1,s1,ei,ed,s2,O, T, T, T],  # y7  eye bottom (iris)
    [T, T, T, O, s1,s1,s1,s2,s1,s1,s1,s2,O, T, T, T],  # y8  cheeks + nose
    [T, T, T, O, s1,s1,s1,s1,s1,s1,s1,s3,O, T, T, T],  # y9  lower face
    [T, T, T, O, s1,s2,s1,s1,s1,s1,s2,s3,O, T, T, T],  # y10 chin (round)
    [T, T, T, T, O, s2,s1,s1,s1,s1,s2,O, T, T, T, T],  # y11 jaw
    [T, T, O, ir0,ir1,s2,s2,s2,s2,s2,ir1,ir2,O, T, T, T],  # y12 neck + collar
    [T, O, ir0,c0,c1,c1,ir1,ir1,ir1,c1,c1,c2,ir2,O, T, T],  # y13 upper body + inner robe
    [T, O, c0,c0,c1,bd0,bd1,c1,c1,bd0,bd1,c1,c2,c3,O, T],  # y14 chest + beads
    [O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c1,c1,c2,c3,O, T],  # y15 wide torso
    [O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c1,c1,c2,c3,c3,O],  # y16 belly (widest)
    [O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c1,c1,c2,c3,c3,O],  # y17 belly
    [O, c0,c1,c1,c1,c2,c1,c1,c1,c1,c2,c1,c2,c3,c3,O],  # y18 robe fold
    [T, O, c0,c1,c1,c1,c1,c2,c2,c1,c1,c2,c2,c3,O, T],  # y19 lower robe
    [T, O, c0,c1,c1,c2,c2,c1,c1,c2,c2,c2,c3,c3,O, T],  # y20 robe
    [T, T, O, c1,c1,c2,c1,c2,c2,c1,c2,c3,c3,O, T, T],  # y21 robe lower
    [T, T, O, c1,c2,c2,c2,c2,c2,c2,c2,c3,c3,O, T, T],  # y22 robe hem
    [T, T, T, O, c2,c2,c3,c3,c3,c2,c3,c3,O, T, T, T],  # y23 robe bottom
    [T, T, T, T, O, c3,c3,c3,c3,c3,c3,O, T, T, T, T],  # y24 robe tip
    [T, T, T, T, T, O, s2,O, O, s2,O, T, T, T, T, T],  # y25 ankles
    [T, T, T, T, T, O,sn0,sn1,sn1,sn0,O, T, T, T, T],  # y26 sandals
    [T, T, T, T, T, T, O, O, O, O, T, T, T, T, T, T],  # y27 sandal bottom
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y28
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y29
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y30
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y31
]

# Right-facing standing frame - wider body, bald head profile
RIGHT_STAND = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y0
    [T, T, T, T, T, O, O, O, O, O, T, T, T, T, T, T],  # y1  head top
    [T, T, T, T, O, s0,s0,s1,s1,s1,O, T, T, T, T, T],  # y2  bald dome
    [T, T, T, O, s0,s0,s1,s1,s1,s1,s1,O, T, T, T, T],  # y3  head
    [T, T, T, O, s0,s1,s1,s1,s1,s1,s2,O, T, T, T, T],  # y4  forehead
    [T, T, T, O, s0,s1,s1,s1,s1,s1,s2,O, T, T, T, T],  # y5  upper face
    [T, T, T, O, s1,s1,s1,ed,s1,s1,s2,O, T, T, T, T],  # y6  eye top
    [T, T, T, O, s1,s1,s1,ei,eh,s1,s2,O, T, T, T, T],  # y7  eye bottom
    [T, T, T, O, s1,s1,s1,s1,s2,s2,s2,O, T, T, T, T],  # y8  nose
    [T, T, T, O, s1,s1,s1,s1,s1,s2,s3,O, T, T, T, T],  # y9  mouth area
    [T, T, T, O, s1,s2,s1,s1,s1,s2,s3,O, T, T, T, T],  # y10 chin
    [T, T, T, T, O, s2,s1,s1,s2,s2,O, T, T, T, T, T],  # y11 jaw
    [T, T, O, ir0,ir1,s2,s2,s2,ir1,ir2,O, T, T, T, T],  # y12 neck + collar
    [T, O, c0,c0,c1,c1,ir1,c1,c1,c2,c2,O, T, T, T, T],  # y13 upper body
    [T, O, c0,c1,c1,bd0,bd1,c1,c1,c2,c2,c3,O, T, T, T],  # y14 chest + beads
    [O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c2,c3,c3,O, T, T],  # y15 wide torso
    [O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c2,c3,c3,O, T, T],  # y16 belly
    [O, c0,c1,c1,c1,c1,c1,c1,c1,c2,c2,c3,c3,O, T, T],  # y17 belly
    [O, c0,c1,c1,c1,c2,c1,c1,c2,c2,c2,c3,c3,O, T, T],  # y18 fold
    [T, O, c0,c1,c1,c1,c1,c2,c2,c2,c3,c3,O, T, T, T],  # y19 lower robe
    [T, O, c1,c1,c2,c2,c1,c2,c2,c3,c3,c3,O, T, T, T],  # y20 robe
    [T, T, O, c1,c2,c2,c2,c2,c3,c3,c3,O, T, T, T, T],  # y21 robe lower
    [T, T, T, O, c2,c2,c2,c3,c3,c3,O, T, T, T, T, T],  # y22 robe hem
    [T, T, T, T, O, c2,c3,c3,c3,O, T, T, T, T, T, T],  # y23 robe bottom
    [T, T, T, T, T, O, c3,c3,c3,O, T, T, T, T, T, T],  # y24 robe tip
    [T, T, T, T, T, O, s2,O, O,sn0,O, T, T, T, T, T],  # y25 ankles
    [T, T, T, T, T, T, O,sn0,sn1,sn0,O, T, T, T, T, T],  # y26 sandals
    [T, T, T, T, T, T, T, O, O, O, T, T, T, T, T, T],  # y27 sandal bottom
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y28
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y29
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y30
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y31
]

# Back-facing standing frame - bald head, wide kasaya
BACK_STAND = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    [T, T, T, T, T, T, O, O, O, O, T, T, T, T, T, T],  # y0  head top
    [T, T, T, T, T, O, s1,s1,s1,s1,O, T, T, T, T, T],  # y1  bald dome back
    [T, T, T, T, O, s1,s1,s1,s1,s1,s2,O, T, T, T, T],  # y2  bald dome
    [T, T, T, O, s1,s1,s1,s1,s1,s1,s2,s2,O, T, T, T],  # y3  head
    [T, T, T, O, s1,s1,s1,s1,s1,s1,s2,s2,O, T, T, T],  # y4  head
    [T, T, T, O, s1,s1,s1,s1,s1,s1,s2,s2,O, T, T, T],  # y5  head
    [T, T, T, O, s1,s1,s1,s1,s1,s1,s2,s2,O, T, T, T],  # y6  head
    [T, T, T, O, s1,s1,s1,s1,s1,s1,s2,s2,O, T, T, T],  # y7  head
    [T, T, T, O, s1,s1,s1,s1,s1,s1,s2,s2,O, T, T, T],  # y8  head
    [T, T, T, O, s1,s2,s1,s1,s1,s1,s2,s3,O, T, T, T],  # y9  head
    [T, T, T, O, s2,s2,s1,s1,s1,s2,s2,s3,O, T, T, T],  # y10 head back
    [T, T, T, T, O, s2,s2,s2,s2,s2,s3,O, T, T, T, T],  # y11 neck
    [T, T, O, ir0,ir1,s2,s2,s2,s2,s2,ir1,ir2,O, T, T, T],  # y12 collar
    [T, O, c0,c0,c1,c1,ir1,ir1,ir1,c1,c1,c2,c3,O, T, T],  # y13 upper body
    [T, O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c2,c3,O, T, T],  # y14 body
    [O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c1,c2,c3,c3,O, T],  # y15 wide torso
    [O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c1,c2,c3,c3,c3,O],  # y16 belly
    [O, c0,c0,c1,c1,c1,c1,c1,c1,c1,c1,c2,c3,c3,c3,O],  # y17 belly
    [O, c0,c1,c1,c1,c2,c1,c1,c1,c2,c1,c2,c3,c3,c3,O],  # y18 fold
    [T, O, c0,c1,c1,c1,c2,c2,c2,c1,c2,c2,c3,c3,O, T],  # y19 lower robe
    [T, O, c1,c1,c2,c2,c1,c2,c2,c2,c2,c3,c3,c3,O, T],  # y20 robe
    [T, T, O, c1,c2,c2,c2,c2,c2,c2,c3,c3,c3,O, T, T],  # y21 robe lower
    [T, T, O, c1,c2,c2,c2,c2,c2,c2,c3,c3,c3,O, T, T],  # y22 robe hem
    [T, T, T, O, c2,c2,c3,c3,c3,c3,c3,c3,O, T, T, T],  # y23 robe bottom
    [T, T, T, T, O, c3,c3,c3,c3,c3,c3,O, T, T, T, T],  # y24 robe tip
    [T, T, T, T, T, O, s2,O, O, s2,O, T, T, T, T, T],  # y25 ankles
    [T, T, T, T, T, O,sn0,sn1,sn1,sn0,O, T, T, T, T],  # y26 sandals
    [T, T, T, T, T, T, O, O, O, O, T, T, T, T, T, T],  # y27 sandal bottom
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
    Wider stride than Zhaoyun to match stocky build.
    """
    import copy
    frame = copy.deepcopy(stand)

    # Find the first non-empty row (top of sprite)
    first_row = 0
    for i, row in enumerate(frame):
        if any(c != T for c in row):
            first_row = i
            break

    # Head bob: shift rows first_row..11 down by 1px
    body_start = 12
    head_rows = frame[first_row:body_start]
    for i in range(first_row, body_start):
        frame[i] = [T] * 16
    for i, row in enumerate(head_rows):
        if first_row + i + 1 < body_start + 1:
            frame[first_row + i + 1] = row

    # Leg animation: wider stride for stocky monk (y23-y27)
    if direction in ('front', 'back'):
        if step_side == 'left':
            frame[23] = [T,T,T,O,c2,c2,c3,c3,c3,c2,c3,c3,O,T,T,T]
            frame[24] = [T,T,T,O,c3,c3,c3,T,T,c3,c3,c3,O,T,T,T]
            frame[25] = [T,T,T,O,sn0,O,T,T,T,T,T,O,sn0,O,T,T]
            frame[26] = [T,T,T,O,sn0,sn1,O,T,T,T,O,sn0,sn1,O,T,T]
            frame[27] = [T,T,T,T,O,O,T,T,T,T,T,O,O,T,T,T]
        else:
            frame[23] = [T,T,T,O,c2,c2,c3,c3,c3,c2,c3,c3,O,T,T,T]
            frame[24] = [T,T,O,c3,c3,c3,T,T,T,T,c3,c3,c3,O,T,T]
            frame[25] = [T,O,sn0,O,T,T,T,T,T,T,T,O,sn0,O,T,T]
            frame[26] = [T,O,sn0,sn1,O,T,T,T,T,T,O,sn0,sn1,O,T,T]
            frame[27] = [T,T,O,O,T,T,T,T,T,T,T,O,O,T,T,T]
    elif direction == 'right':
        if step_side == 'left':
            frame[23] = [T,T,T,T,O,c2,c3,c3,c3,O,T,T,T,T,T,T]
            frame[24] = [T,T,T,O,c3,c3,c3,O,T,T,T,T,T,T,T,T]
            frame[25] = [T,T,T,O,sn0,O,T,T,O,sn0,O,T,T,T,T,T]
            frame[26] = [T,T,T,O,sn0,sn1,O,T,O,sn0,sn1,O,T,T,T,T]
            frame[27] = [T,T,T,T,O,O,T,T,T,O,O,T,T,T,T,T]
        else:
            frame[23] = [T,T,T,T,O,c2,c3,c3,c3,O,T,T,T,T,T,T]
            frame[24] = [T,T,T,T,T,T,O,c3,c3,c3,O,T,T,T,T,T]
            frame[25] = [T,T,T,T,T,O,sn0,O,T,O,sn0,O,T,T,T,T]
            frame[26] = [T,T,T,T,O,sn0,sn1,O,T,O,sn0,sn1,O,T,T,T]
            frame[27] = [T,T,T,T,T,O,O,T,T,T,O,O,T,T,T,T]
    elif direction == 'left':
        if step_side == 'left':
            frame[23] = [T,T,T,T,T,T,O,c3,c3,c2,O,T,T,T,T,T]
            frame[24] = [T,T,T,T,T,T,O,c3,c3,c3,O,T,T,T,T,T]
            frame[25] = [T,T,T,T,T,O,sn0,O,T,O,sn0,O,T,T,T,T]
            frame[26] = [T,T,T,T,O,sn0,sn1,O,T,O,sn0,sn1,O,T,T,T]
            frame[27] = [T,T,T,T,T,O,O,T,T,T,O,O,T,T,T,T]
        else:
            frame[23] = [T,T,T,T,T,T,O,c3,c3,c2,O,T,T,T,T,T]
            frame[24] = [T,T,T,T,O,c3,c3,c3,O,T,T,T,T,T,T,T]
            frame[25] = [T,T,T,O,sn0,O,T,T,O,sn0,O,T,T,T,T,T]
            frame[26] = [T,T,T,O,sn0,sn1,O,T,O,sn0,sn1,O,T,T,T,T]
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
    Bald monk, round face, kind squinting eyes, kasaya robes, prayer beads.
    Serene/calm expression.
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

    # --- Bald head dome ---
    # Wider, rounder head than Zhaoyun
    fill_rect(22, 2, 41, 4, s1)     # top dome
    fill_rect(19, 5, 44, 8, s1)     # upper dome
    fill_rect(18, 9, 45, 12, s1)    # mid dome

    # Highlight on bald dome (top-left light)
    fill_rect(22, 2, 32, 4, hd)     # bright sheen
    fill_rect(22, 2, 28, 3, HD_HI)  # brightest spot
    fill_rect(19, 5, 30, 7, s0)     # left highlight
    fill_rect(36, 5, 44, 8, s2)     # right shadow
    fill_rect(40, 9, 45, 12, s2)    # right shadow lower

    # Head outline
    hline(22, 41, 1, O)
    for y in range(2, 5):
        p(21, y, O); p(42, y, O)
    for y in range(5, 9):
        p(18, y, O); p(45, y, O)
    for y in range(9, 13):
        p(17, y, O); p(46, y, O)

    # --- Face (wider, rounder than Zhaoyun) ---
    fill_rect(18, 13, 45, 32, s1)
    # Forehead highlight
    fill_rect(18, 13, 32, 16, s0)
    # Right face shadow
    fill_rect(40, 13, 45, 32, s2)
    # Cheek roundness (wider face)
    fill_rect(18, 20, 20, 28, s2)   # left cheek shadow
    fill_rect(43, 20, 45, 28, s3)   # right cheek deep shadow
    # Chin area (round)
    fill_rect(22, 30, 41, 32, s2)
    hline(24, 39, 32, s3)

    # Face outline continues
    for y in range(13, 33):
        p(17, y, O); p(46, y, O)
    hline(19, 44, 33, O)
    p(18, 32, O); p(45, 32, O)

    # --- Eyes (small, kind, slightly squinting - 2 row style) ---
    # Left eye: lash line + iris row, no separate eyebrow
    p(24, 17, ed); p(25, 17, ed); p(26, 17, ed); p(27, 17, ed)
    p(24, 18, eh); p(25, 18, ei); p(26, 18, ei); p(27, 18, ed)
    # Right eye
    p(36, 17, ed); p(37, 17, ed); p(38, 17, ed); p(39, 17, ed)
    p(36, 18, ed); p(37, 18, ei); p(38, 18, ei); p(39, 18, eh)

    # --- Nose (wider, rounder) ---
    p(31, 22, s2); p(32, 22, s2)
    p(30, 23, s3); p(31, 23, s3); p(32, 23, s2)

    # --- Mouth (slight serene smile) ---
    hline(29, 34, 26, s3)
    hline(30, 33, 27, s2)

    # --- Neck (thicker for stocky build) ---
    fill_rect(25, 33, 38, 37, s1)
    fill_rect(25, 33, 32, 35, s0)
    fill_rect(35, 33, 38, 37, s2)

    # --- Collar (inner robe V-neck) ---
    fill_rect(18, 38, 45, 40, ir1)
    hline(18, 28, 38, ir0)
    hline(38, 45, 38, ir2)
    # V-collar lines
    for i in range(3):
        p(30 - i, 38 + i, s2)
        p(33 + i, 38 + i, s2)

    # --- Kasaya robe body ---
    fill_rect(12, 41, 51, 58, c1)
    fill_rect(12, 41, 22, 58, c0)   # left highlight
    fill_rect(44, 41, 51, 58, c2)   # right shadow

    # Prayer beads (diagonal across chest)
    for i in range(8):
        bx = 22 + i * 2
        by = 42 + i
        if bx < 52 and by < 58:
            p(bx, by, bd0)
            p(bx + 1, by, bd1)

    # Robe folds
    for y in range(48, 58):
        p(28, y, c2)
        p(36, y, c2)

    # Bottom robe
    fill_rect(12, 58, 51, 63, c2)
    fill_rect(12, 58, 22, 63, c1)
    fill_rect(44, 58, 51, 63, c3)

    # Robe outline
    for y in range(38, 63):
        p(11, y, O)
        p(52, y, O)
    hline(11, 52, 63, O)


def generate_portrait_happy(img, ox, oy):
    """Happy/laughing expression - closed crescent eyes, wide open mouth laugh.
    Foyin is known for hearty laughter (大笑).
    """
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)

    # Clear default eyes
    for x in range(24, 28):
        p(x, 17, s1); p(x, 18, s1)
    for x in range(36, 40):
        p(x, 17, s1); p(x, 18, s1)

    # Happy crescent eyes ^_^ (squinting even more)
    p(24, 18, M); p(25, 17, M); p(26, 17, M); p(27, 18, M)
    p(36, 18, M); p(37, 17, M); p(38, 17, M); p(39, 18, M)

    # Clear default mouth
    hline(29, 34, 26, s1)
    hline(29, 34, 27, s1)

    # Wide laughing mouth (open)
    hline(28, 35, 25, ed)
    hline(28, 35, 26, ed)
    hline(29, 34, 27, ed)
    # Teeth/tongue hint
    hline(29, 34, 25, s0)
    hline(29, 34, 26, (180, 80, 70, 255))  # tongue hint

    # Laugh lines at cheeks
    p(22, 19, s2); p(41, 19, s2)
    p(22, 20, s2); p(41, 20, s2)


def generate_portrait_pensive(img, ox, oy):
    """Pensive/contemplative expression - half-closed eyes, slight frown.
    Foyin in deep meditation/thought (沉思).
    """
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)

    # Clear default eyes
    for x in range(24, 28):
        p(x, 17, s1); p(x, 18, s1)
    for x in range(36, 40):
        p(x, 17, s1); p(x, 18, s1)

    # Half-closed meditative eyes (just a line)
    hline(24, 27, 18, ed)
    hline(36, 39, 18, ed)
    # Slight lid shadow above
    hline(24, 27, 17, s2)
    hline(36, 39, 17, s2)

    # Clear default mouth
    hline(29, 34, 26, s1)
    hline(29, 34, 27, s1)

    # Neutral/slight frown (contemplative)
    hline(30, 33, 26, s3)
    p(29, 27, s3); p(34, 27, s3)


def generate_portrait_surprised(img, ox, oy):
    """Surprised expression - wide eyes, open mouth.
    Foyin reacting to something unexpected (惊讶).
    """
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)

    # Clear default eyes
    for x in range(24, 28):
        p(x, 17, s1); p(x, 18, s1)
    for x in range(36, 40):
        p(x, 17, s1); p(x, 18, s1)

    # Wide surprised eyes (bigger than default, 3 rows)
    # Left eye
    p(24, 16, ed); p(25, 16, ed); p(26, 16, ed); p(27, 16, ed)
    p(24, 17, eh); p(25, 17, ei); p(26, 17, ei); p(27, 17, ed)
    p(24, 18, ed); p(25, 18, ed); p(26, 18, ed); p(27, 18, ed)
    # Right eye
    p(36, 16, ed); p(37, 16, ed); p(38, 16, ed); p(39, 16, ed)
    p(36, 17, ed); p(37, 17, ei); p(38, 17, ei); p(39, 17, eh)
    p(36, 18, ed); p(37, 18, ed); p(38, 18, ed); p(39, 18, ed)

    # Clear default mouth
    hline(29, 34, 26, s1)
    hline(29, 34, 27, s1)

    # Open O-shaped mouth
    p(30, 25, ed); p(31, 25, ed); p(32, 25, ed); p(33, 25, ed)
    p(30, 26, ed); p(31, 26, s3); p(32, 26, s3); p(33, 26, ed)
    p(30, 27, ed); p(31, 27, ed); p(32, 27, ed); p(33, 27, ed)


def generate_portrait_sheet():
    """Generate 128x128 portrait sheet (2x2 grid of 64x64).
    Top-left: default (serene)
    Top-right: happy (laughing)
    Bottom-left: pensive (contemplative)
    Bottom-right: surprised
    """
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

    generate_portrait_default(img, 0, 0)       # top-left
    generate_portrait_happy(img, 64, 0)         # top-right
    generate_portrait_pensive(img, 0, 64)       # bottom-left
    generate_portrait_surprised(img, 64, 64)    # bottom-right

    return img


# === MAIN ===
if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    char_path = os.path.join(base_dir, "assets", "Characters", "Foyin.png")
    port_path = os.path.join(base_dir, "assets", "Portraits", "Foyin.png")

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

    # Check portrait quadrants are not identical
    for qname, qx, qy in [("Default", 0, 0), ("Happy", 64, 0),
                            ("Pensive", 0, 64), ("Surprised", 64, 64)]:
        px_count = 0
        for y in range(64):
            for x in range(64):
                if verify_port.getpixel((qx + x, qy + y))[3] > 0:
                    px_count += 1
        print(f"  Portrait {qname}: {px_count} non-transparent pixels {'OK' if px_count > 100 else 'TOO FEW!'}")
