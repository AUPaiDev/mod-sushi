#!/usr/bin/env python3
"""Generate Zhaoyun (朝云) sprite sheet and portrait for Stardew Valley mod.

Completely rewritten to match official Stardew Valley NPC art style:
- Prominent eyes with white eyewhites + dark iris (the signature SDV look)
- Proper 16x32 proportions: large head, slim body, correct zone layout
- Hue-shifted palette with top-left lighting
- Song dynasty pink clothing with layered collar/sash/skirt
- Long black hair with golden ornament

Zone layout (16x32):
  y0-1:   hair top / ornament
  y2-3:   hair dome
  y4-9:   face (6px tall) -- eyes at y5-y6
  y10-11:  chin / neck / hair drape
  y12-19:  torso (collar, sash, waist)
  y20-24:  skirt / lower body
  y25-27:  shoes
  y28-31:  empty
"""

from PIL import Image
import copy
import os
import shutil

# ============================================================
# COLOR PALETTE  (hue-shifted, top-left light source)
# ============================================================
T = (0, 0, 0, 0)  # transparent

# -- Outline (dark brown, NOT pure black) --
OL  = (50, 30, 35, 255)     # main body/clothing outline
OLH = (35, 22, 40, 255)     # hair outline (cooler, blue-tinted)

# -- Skin (warm peach, 4-stop gradient) --
SK0 = (255, 232, 210, 255)  # highlight (top-left lit)
SK1 = (245, 214, 186, 255)  # base
SK2 = (222, 185, 155, 255)  # shadow
SK3 = (198, 158, 130, 255)  # deep shadow (chin, neck)

# -- Hair (blue-black, 3-stop) --
HR0 = (62, 55, 78, 255)     # highlight (blue sheen)
HR1 = (35, 28, 48, 255)     # base
HR2 = (22, 16, 32, 255)     # shadow

# -- Eyes --
EW  = (255, 255, 255, 255)  # eye white (PURE white for max contrast)
EI  = (45, 25, 30, 255)     # iris / pupil (very dark brown-red)
EL  = (30, 18, 22, 255)     # eyelash line (near black)

# -- Pink clothing (Song dynasty ruqun) --
CL0 = (250, 222, 228, 255)  # highlight (white-pink)
CL1 = (238, 180, 195, 255)  # base (rose)
CL2 = (208, 140, 162, 255)  # shadow (deeper rose)
CL3 = (172, 105, 132, 255)  # deep shadow (plum)

# -- Inner collar (white-cream, visible at V-neck) --
IC0 = (252, 248, 242, 255)  # highlight
IC1 = (238, 230, 218, 255)  # base
IC2 = (218, 208, 195, 255)  # shadow

# -- Sash / belt (golden) --
SA0 = (245, 218, 95, 255)   # highlight
SA1 = (210, 182, 68, 255)   # base
SA2 = (172, 145, 48, 255)   # shadow

# -- Hair ornament (gold) --
HO0 = (252, 228, 108, 255)  # highlight
HO1 = (225, 195, 78, 255)   # base
HO2 = (188, 158, 55, 255)   # shadow

# -- Lips --
LIP = (218, 155, 148, 255)

# -- Shoes --
SH0 = (145, 95, 115, 255)   # base
SH1 = (115, 70, 90, 255)    # shadow

# ============================================================
# SHORTHAND ALIASES
# ============================================================
O   = OL
H   = OLH
s0, s1, s2, s3 = SK0, SK1, SK2, SK3
h0, h1, h2 = HR0, HR1, HR2
ew, ei, el = EW, EI, EL
c0, c1, c2, c3 = CL0, CL1, CL2, CL3
ic0, ic1, ic2 = IC0, IC1, IC2
sa0, sa1, sa2 = SA0, SA1, SA2
ho0, ho1, ho2 = HO0, HO1, HO2
lp  = LIP
sh0, sh1 = SH0, SH1

# ============================================================
# FRONT-FACING STANDING  (facing south / down)
# ============================================================
# Head 10px wide (x3..x12), body 10px, skirt flares to 12px
# Eyes at y5-y6: 2px white per eye, very prominent
# Hair drapes on sides x3-x4 and x11-x12
FRONT_STAND = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    [T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T],  # y0  ornament tip
    [T, T, T, T, T, H,ho0,ho1,ho1,ho0, H, T, T, T, T, T],  # y1  golden ornament
    [T, T, T, T, H, h0, h1, h1, h1, h1, h0, H, T, T, T, T],  # y2  hair dome
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y3  hair wider
    [T, T, T, H, h1, s0, s0, s1, s1, s0, s0, h2, H, T, T, T],  # y4  forehead
    [T, T, T, H, h1, el, el, s0, s1, el, el, h2, H, T, T, T],  # y5  eyelash line (dark)
    [T, T, T, H, h1, ew, ei, s1, s1, ei, ew, h2, H, T, T, T],  # y6  eye whites + iris
    [T, T, T, H, h1, s0, s1, s2, s1, s1, s1, h2, H, T, T, T],  # y7  cheeks
    [T, T, T, H, s1, s1, s1, s2, s1, s1, s1, s2, H, T, T, T],  # y8  nose
    [T, T, T, H, s1, s1, lp, lp, lp, s1, s1, s3, H, T, T, T],  # y9  mouth
    [T, T, T, H, h1, s2, s1, s1, s1, s1, s2, h2, H, T, T, T],  # y10 chin + hair sides
    [T, T, T, H, h1, h1, s2, s3, s3, s2, h1, h2, H, T, T, T],  # y11 neck + hair drape
    [T, T, H, h1, O,ic0,ic1, s3, s3,ic1,ic0, O, h2, H, T, T],  # y12 collar V-neck + hair
    [T, T, H, h1, c0, c1,ic0,ic1,ic1, c1, c1, c2, h2, H, T, T],  # y13 upper chest + hair
    [T, T, H, h0, c0, c1, c1, c1, c1, c1, c1, c2, h2, H, T, T],  # y14 chest
    [T, O, H, h0, c0,sa0,sa1,sa1,sa1,sa0, c1, c2, h2, H, O, T],  # y15 sash upper
    [T, O, H, h0, c0,sa1,sa2,sa2,sa2,sa1, c1, c2, h2, H, O, T],  # y16 sash lower
    [T, O, H, h0, c0, c1, c1, c1, c1, c1, c1, c2, h2, H, O, T],  # y17 waist
    [T, O, H, h1, c0, c1, c1, c2, c2, c1, c1, c2, h2, H, O, T],  # y18 hip + fold
    [T, O, H, h1, c0, c1, c1, c1, c1, c1, c2, c2, h2, H, O, T],  # y19 upper skirt
    [T, T, H, h1, c1, c1, c2, c1, c1, c2, c2, c3, h2, H, T, T],  # y20 skirt fold
    [T, T, H, h1, c1, c1, c2, c2, c2, c2, c2, c3, h2, H, T, T],  # y21 skirt
    [T, T, T, O, c0, c1, c2, c3, c3, c2, c3, c3, O, T, T, T],  # y22 skirt lower
    [T, T, T, T, O, c2, c3, c3, c3, c3, c3, O, T, T, T, T],  # y23 skirt hem
    [T, T, T, T, T, O, c3, O, O, c3, O, T, T, T, T, T],  # y24 ankles
    [T, T, T, T, T, O,sh0,sh1,sh1,sh0, O, T, T, T, T, T],  # y25 shoes
    [T, T, T, T, T, T, O, O, O, O, T, T, T, T, T, T],  # y26 shoe soles
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y27
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y28
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y29
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y30
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y31
]

# ============================================================
# RIGHT-FACING STANDING  (facing east / right)
# ============================================================
# Profile view: one eye visible, hair behind on left side
# Head ~9px wide, body ~10px
RIGHT_STAND = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    [T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T],  # y0  ornament tip
    [T, T, T, T, T, H,ho0,ho1,ho0, H, T, T, T, T, T, T],  # y1  ornament
    [T, T, T, T, H, h0, h1, h1, h1, h1, H, T, T, T, T, T],  # y2  hair dome
    [T, T, T, H, h1, h1, h1, h1, h1, h1, h1, H, T, T, T, T],  # y3  hair
    [T, T, T, H, h1, h1, s0, s1, s1, s1, s1, H, T, T, T, T],  # y4  forehead
    [T, T, T, H, h1, s0, s1, s1, el, el, s2, H, T, T, T, T],  # y5  eye lash (one eye)
    [T, T, T, H, h1, s0, s1, s1, ew, ei, s2, H, T, T, T, T],  # y6  eye white+iris
    [T, T, T, H, h1, s1, s1, s1, s1, s2, s2, H, T, T, T, T],  # y7  cheek
    [T, T, T, H, h1, s1, s1, s1, s2, s2, s2, H, T, T, T, T],  # y8  nose (profile bump)
    [T, T, T, H, h1, s1, s1, lp, lp, s2, s3, H, T, T, T, T],  # y9  mouth
    [T, T, T, H, h1, s2, s1, s1, s1, s2, h1, H, T, T, T, T],  # y10 chin
    [T, T, T, H, h1, h1, s2, s3, s3, h1, h1, H, T, T, T, T],  # y11 neck + hair
    [T, T, H, h1, O,ic0,ic1, s3,ic1, c1, O, h2, H, T, T, T],  # y12 collar + hair
    [T, T, H, h1, c0, c1,ic0, c1, c1, c1, c2, c2, H, T, T, T],  # y13 upper body + hair
    [T, O, H, h0, c0, c1, c1, c1, c1, c1, c1, c2, H, O, T, T],  # y14 chest
    [T, O, H, h0, c0,sa0,sa1,sa1, c1, c1, c1, c2, H, O, T, T],  # y15 sash
    [T, O, H, h0, c0,sa1,sa2,sa2, c1, c1, c2, c2, H, O, T, T],  # y16 sash lower
    [T, O, H, h0, c0, c1, c1, c1, c1, c1, c2, c2, H, O, T, T],  # y17 waist
    [T, O, H, h1, c0, c1, c1, c2, c1, c1, c2, c2, H, O, T, T],  # y18 hip
    [T, O, H, h1, c0, c1, c1, c1, c1, c2, c2, c3, H, O, T, T],  # y19 skirt
    [T, T, H, h1, c1, c1, c2, c2, c1, c2, c3, c3, H, T, T, T],  # y20 skirt fold
    [T, T, H, h1, c1, c2, c2, c1, c2, c2, c3, c3, H, T, T, T],  # y21 skirt
    [T, T, T, O, c1, c2, c2, c2, c2, c3, c3, O, T, T, T, T],  # y22 skirt lower
    [T, T, T, T, O, c2, c3, c3, c3, c3, O, T, T, T, T, T],  # y23 skirt hem
    [T, T, T, T, T, O, c3, O, O, c3, O, T, T, T, T, T],  # y24 ankles
    [T, T, T, T, T, T, O,sh0,sh1,sh0, O, T, T, T, T, T],  # y25 shoes
    [T, T, T, T, T, T, T, O, O, O, T, T, T, T, T, T],  # y26 shoe soles
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y27
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y28
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y29
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y30
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y31
]

# ============================================================
# BACK-FACING STANDING  (facing north / up)
# ============================================================
# Hair visible down the back, no face, ornament on top
# Hair center strip with clothing on sides
BACK_STAND = [
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    [T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T],  # y0  ornament tip
    [T, T, T, T, T, H,ho0,ho1,ho1,ho0, H, T, T, T, T, T],  # y1  ornament
    [T, T, T, T, H, h0, h1, h1, h1, h1, h0, H, T, T, T, T],  # y2  hair dome
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y3  hair
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y4  back of head
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y5  back of head
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y6  back of head
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y7  back of head
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y8  back of head
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y9  back of head
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y10 back of head
    [T, T, T, H, h0, h1, h1, h1, h1, h1, h1, h2, H, T, T, T],  # y11 neck back
    [T, T, H, h0, c0, c0, h0, h1, h1, h1, c1, c2, h2, H, T, T],  # y12 collar back + hair
    [T, T, H, c0, c0, c1, h0, h1, h1, h1, c1, c2, c2, H, T, T],  # y13 upper back + hair
    [T, O, H, c0, c0, c1, h0, h1, h1, h1, c1, c2, c2, H, O, T],  # y14 back
    [T, O, H, c0, c0,sa0, h0, h1, h1,sa1, c1, c2, c2, H, O, T],  # y15 sash + hair
    [T, O, H, c0, c0,sa1, h0, h1, h1,sa2, c1, c2, c2, H, O, T],  # y16 sash lower
    [T, O, H, c0, c0, c1, h0, h1, h1, h1, c1, c2, c2, H, O, T],  # y17 waist
    [T, O, H, c0, c0, c1, h0, h1, h1, h1, c1, c2, c2, H, O, T],  # y18 hip
    [T, O, H, c0, c1, c1, h0, h1, h1, h2, c2, c2, c3, H, O, T],  # y19 skirt
    [T, T, H, c0, c1, c1, h0, h1, h1, h2, c2, c3, c3, H, T, T],  # y20 skirt fold
    [T, T, H, c1, c1, c2, h0, h1, h1, h2, c2, c3, c3, H, T, T],  # y21 skirt
    [T, T, T, O, c1, c2, c2, h1, h1, c3, c3, c3, O, T, T, T],  # y22 skirt lower
    [T, T, T, T, O, c2, c3, c3, c3, c3, c3, O, T, T, T, T],  # y23 skirt hem
    [T, T, T, T, T, O, c3, O, O, c3, O, T, T, T, T, T],  # y24 ankles
    [T, T, T, T, T, O,sh0,sh1,sh1,sh0, O, T, T, T, T, T],  # y25 shoes
    [T, T, T, T, T, T, O, O, O, O, T, T, T, T, T, T],  # y26 shoe soles
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y27
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y28
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y29
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y30
    [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # y31
]

# ============================================================
# LEFT-FACING = mirror of RIGHT-FACING
# ============================================================
def mirror_frame(frame):
    """Horizontally flip a 16x32 frame."""
    return [list(reversed(row)) for row in frame]

LEFT_STAND = mirror_frame(RIGHT_STAND)


# ============================================================
# WALK ANIMATION
# ============================================================
def make_walk_frame(stand, step_side, direction):
    """Generate a walk frame from standing frame.

    Animation: head bobs down 1px, feet separate to show stride.
    """
    frame = copy.deepcopy(stand)

    # Find first non-empty row
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
        target = first_row + i + 1
        if target <= body_start:
            frame[target] = row

    # Leg animation: modify skirt hem + feet area (y22-y26)
    if direction in ('front', 'back'):
        if step_side == 'left':
            frame[22] = [T,T,T,H,c1,c2,c2,c3,c3,c2,c3,c3,H,T,T,T]
            frame[23] = [T,T,T,O,c2,c3,c3,T,T,c3,c3,c3,O,T,T,T]
            frame[24] = [T,T,T,O,sh0,O,T,T,T,T,O,sh0,O,T,T,T]
            frame[25] = [T,T,T,O,sh0,sh1,O,T,T,O,sh0,sh1,O,T,T,T]
            frame[26] = [T,T,T,T,O,O,T,T,T,T,O,O,T,T,T,T]
        else:
            frame[22] = [T,T,T,H,c1,c2,c2,c3,c3,c2,c3,c3,H,T,T,T]
            frame[23] = [T,T,O,c2,c3,c3,T,T,T,T,c3,c3,c3,O,T,T]
            frame[24] = [T,T,O,sh0,O,T,T,T,T,T,T,O,sh0,O,T,T]
            frame[25] = [T,T,O,sh0,sh1,O,T,T,T,O,sh0,sh1,O,T,T,T]
            frame[26] = [T,T,T,O,O,T,T,T,T,T,O,O,T,T,T,T]
    elif direction == 'right':
        if step_side == 'left':
            frame[22] = [T,T,T,T,H,c2,c3,c3,c3,c3,H,T,T,T,T,T]
            frame[23] = [T,T,T,O,c3,c3,O,T,T,O,c3,O,T,T,T,T]
            frame[24] = [T,T,T,O,sh0,O,T,T,T,O,sh0,O,T,T,T,T]
            frame[25] = [T,T,T,O,sh0,sh1,O,T,O,sh0,sh1,O,T,T,T,T]
            frame[26] = [T,T,T,T,O,O,T,T,T,O,O,T,T,T,T,T]
        else:
            frame[22] = [T,T,T,T,H,c2,c3,c3,c3,c3,H,T,T,T,T,T]
            frame[23] = [T,T,T,T,O,c3,c3,O,T,c3,c3,O,T,T,T,T]
            frame[24] = [T,T,T,T,T,O,sh0,O,T,O,sh0,O,T,T,T,T]
            frame[25] = [T,T,T,T,O,sh0,sh1,O,O,sh0,sh1,O,T,T,T,T]
            frame[26] = [T,T,T,T,T,O,O,T,T,O,O,T,T,T,T,T]
    elif direction == 'left':
        if step_side == 'left':
            frame[22] = [T,T,T,T,T,H,c3,c3,c3,c3,c2,H,T,T,T,T]
            frame[23] = [T,T,T,T,O,c3,O,T,T,O,c3,c3,O,T,T,T]
            frame[24] = [T,T,T,T,O,sh0,O,T,T,T,O,sh0,O,T,T,T]
            frame[25] = [T,T,T,O,sh0,sh1,O,T,T,O,sh0,sh1,O,T,T,T]
            frame[26] = [T,T,T,T,O,O,T,T,T,T,O,O,T,T,T,T]
        else:
            frame[22] = [T,T,T,T,T,H,c3,c3,c3,c3,c2,H,T,T,T,T]
            frame[23] = [T,T,T,T,O,c3,c3,T,O,c3,c3,O,T,T,T,T]
            frame[24] = [T,T,T,T,O,sh0,O,T,O,sh0,O,T,T,T,T,T]
            frame[25] = [T,T,T,O,sh0,sh1,O,O,sh0,sh1,O,T,T,T,T,T]
            frame[26] = [T,T,T,T,O,O,T,T,O,O,T,T,T,T,T,T]

    return frame

# ============================================================
# RENDERING HELPERS
# ============================================================
def paint_frame(img, frame_data, offset_x, offset_y):
    """Paint a 16x32 frame onto the image at the given offset."""
    for y, row in enumerate(frame_data):
        for x, color in enumerate(row):
            if color != T:
                img.putpixel((offset_x + x, offset_y + y), color)


def generate_character_sheet():
    """Generate the 64x128 character sprite sheet.

    Layout: 4 rows (front, right, back, left) x 4 columns (stand, walk1, stand, walk2)
    Each frame is 16x32.
    """
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

# ============================================================
# PORTRAIT  (128x128 sheet = 2x2 grid of 64x64)
# ============================================================
def _portrait_helpers(img, ox, oy):
    """Return pixel-drawing helper closures for a 64x64 portrait quadrant."""
    def p(x, y, c):
        if 0 <= x < 64 and 0 <= y < 64:
            img.putpixel((ox + x, oy + y), c)

    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)

    def fill_rect(x1, y1, x2, y2, c):
        for yy in range(y1, y2 + 1):
            hline(x1, x2, yy, c)

    return p, hline, fill_rect


def generate_portrait_default(img, ox, oy):
    """Default expression portrait (64x64).

    Large face with prominent SDV-style eyes, long flowing hair,
    golden ornament, Song dynasty pink clothing with V-collar.
    """
    p, hline, fill_rect = _portrait_helpers(img, ox, oy)

    # --- Hair (long, flowing past shoulders) ---
    # Hair dome top
    fill_rect(20, 2, 43, 3, h1)
    fill_rect(18, 4, 45, 7, h1)
    # Hair highlight (left side, top-left light)
    fill_rect(20, 2, 30, 6, h0)
    # Hair sides flowing down (long hair to y52)
    fill_rect(14, 8, 19, 50, h1)    # left hair
    fill_rect(44, 8, 49, 50, h2)    # right hair
    # Hair highlight on left side
    fill_rect(14, 8, 16, 38, h0)
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
    fill_rect(20, 8, 43, 30, s1)     # base
    fill_rect(20, 8, 32, 14, s0)     # forehead highlight
    fill_rect(38, 8, 43, 30, s2)     # right shadow
    fill_rect(22, 28, 41, 30, s2)    # chin shadow
    hline(24, 39, 30, s3)            # deep chin line

    # --- Eyes (THE key feature -- large, prominent) ---
    # Each eye: 4px wide, 2 rows tall
    # Top row: dark eyelash line
    # Bottom row: white eyewhite + dark iris
    # Left eye (x22-x25)
    hline(22, 25, 16, el)                          # lash line
    p(22, 17, ew); p(23, 17, ew); p(24, 17, ei); p(25, 17, el)  # white+iris
    # Right eye (x37-x40)
    hline(37, 40, 16, el)                          # lash line
    p(37, 17, el); p(38, 17, ei); p(39, 17, ew); p(40, 17, ew)  # iris+white

    # --- Eyebrows (subtle, above eyes) ---
    hline(22, 26, 14, OL)
    hline(36, 40, 14, OL)

    # --- Nose ---
    p(31, 21, s2); p(32, 21, s3)
    p(31, 22, s3)

    # --- Mouth ---
    hline(29, 34, 24, lp)
    hline(30, 33, 25, LIP)

    # --- Neck ---
    fill_rect(27, 31, 36, 35, s1)
    fill_rect(27, 31, 32, 33, s0)
    fill_rect(34, 31, 36, 35, s2)

    # --- Clothing (Song dynasty ruqun) ---
    # Inner collar V-neck
    fill_rect(20, 36, 43, 38, ic1)
    hline(20, 30, 36, ic0)
    hline(36, 43, 36, ic2)
    # V-collar lines
    for i in range(3):
        p(29 - i, 36 + i, s3)
        p(34 + i, 36 + i, s3)

    # Body / clothing
    fill_rect(14, 39, 49, 58, c1)
    fill_rect(14, 39, 24, 58, c0)    # highlight left
    fill_rect(42, 39, 49, 58, c2)    # shadow right

    # Sash / belt
    fill_rect(24, 43, 39, 46, sa1)
    hline(24, 32, 43, sa0)
    hline(33, 39, 45, sa2)
    hline(24, 39, 46, sa2)

    # Clothing folds
    for y in range(48, 58):
        p(28, y, c2)
        p(35, y, c2)

    # Bottom clothing
    fill_rect(14, 58, 49, 63, c2)
    fill_rect(14, 58, 24, 63, c1)
    fill_rect(42, 58, 49, 63, c3)

    # Clothing outline
    for y in range(36, 63):
        p(13, y, O)
        p(50, y, O)
    hline(13, 50, 63, O)


def generate_portrait_happy(img, ox, oy):
    """Happy expression -- closed ^_^ eyes, wider smile."""
    generate_portrait_default(img, ox, oy)
    p, hline, fill_rect = _portrait_helpers(img, ox, oy)

    # Clear default eyes
    for x in range(22, 26):
        p(x, 16, s1); p(x, 17, s1)
    for x in range(37, 41):
        p(x, 16, s1); p(x, 17, s1)

    # Happy curved eyes ^_^
    p(22, 17, OL); p(23, 16, OL); p(24, 16, OL); p(25, 17, OL)
    p(37, 17, OL); p(38, 16, OL); p(39, 16, OL); p(40, 17, OL)

    # Wider smile
    hline(28, 35, 24, lp)
    hline(29, 34, 25, lp)


def generate_portrait_sad(img, ox, oy):
    """Sad expression -- angled brows, downturned mouth."""
    generate_portrait_default(img, ox, oy)
    p, hline, fill_rect = _portrait_helpers(img, ox, oy)

    # Sad eyebrows (angled down toward center)
    hline(22, 26, 14, s1)  # clear old brows
    hline(36, 40, 14, s1)
    p(23, 13, OL); p(24, 13, OL); p(25, 14, OL); p(26, 14, OL)
    p(39, 13, OL); p(38, 13, OL); p(37, 14, OL); p(36, 14, OL)

    # Downturned mouth
    hline(29, 34, 24, s1)  # clear old
    p(29, 25, lp); p(30, 25, lp); p(33, 25, lp); p(34, 25, lp)
    p(28, 24, lp); p(35, 24, lp)


def generate_portrait_surprised(img, ox, oy):
    """Surprised expression -- raised brows, wide eyes, open mouth."""
    generate_portrait_default(img, ox, oy)
    p, hline, fill_rect = _portrait_helpers(img, ox, oy)

    # Raised eyebrows (higher)
    hline(22, 26, 14, s1)  # clear old
    hline(36, 40, 14, s1)
    hline(22, 26, 13, OL)
    hline(36, 40, 13, OL)

    # Wider eyes (add extra white)
    # Left eye -- extra white pixel
    p(21, 16, el); p(26, 16, el)
    p(21, 17, ew); p(26, 17, el)
    # Right eye -- extra white pixel
    p(36, 16, el); p(41, 16, el)
    p(36, 17, el); p(41, 17, ew)

    # Open mouth (O shape)
    hline(29, 34, 24, s1)  # clear old
    p(30, 24, el); p(31, 24, el); p(32, 24, el); p(33, 24, el)
    p(30, 25, el); p(31, 25, lp); p(32, 25, lp); p(33, 25, el)
    p(30, 26, el); p(31, 26, el); p(32, 26, el); p(33, 26, el)


def generate_portrait_sheet():
    """Generate 128x128 portrait sheet (2x2 grid of 64x64).

    Top-left: default    Top-right: happy
    Bottom-left: sad     Bottom-right: surprised
    """
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

    generate_portrait_default(img, 0, 0)
    generate_portrait_happy(img, 64, 0)
    generate_portrait_sad(img, 0, 64)
    generate_portrait_surprised(img, 64, 64)

    return img

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    char_path = os.path.join(base_dir, "assets", "Characters", "Zhaoyun.png")
    port_path = os.path.join(base_dir, "assets", "Portraits", "Zhaoyun.png")

    # Backup originals
    for path in [char_path, port_path]:
        backup = path + ".bak"
        if os.path.exists(path) and not os.path.exists(backup):
            shutil.copy2(path, backup)
            print(f"Backed up: {backup}")

    # Generate character sprite
    char_img = generate_character_sheet()
    char_img.save(char_path)
    print(f"Character sprite saved: {char_path} ({char_img.size})")

    # Generate portrait
    port_img = generate_portrait_sheet()
    port_img.save(port_path)
    print(f"Portrait saved: {port_path} ({port_img.size})")

    # === Verification ===
    verify_char = Image.open(char_path)
    verify_port = Image.open(port_path)
    print(f"\nVerification:")
    print(f"  Character: {verify_char.size} mode={verify_char.mode}")
    print(f"  Portrait:  {verify_port.size} mode={verify_port.mode}")

    assert verify_char.size == (64, 128), f"Character size mismatch: {verify_char.size}"
    assert verify_port.size == (128, 128), f"Portrait size mismatch: {verify_port.size}"

    # Check walk animation has different frames per direction
    dirs = ["Front", "Right", "Back", "Left"]
    all_ok = True
    for row in range(4):
        frame0 = []
        frame1 = []
        for y in range(32):
            for x in range(16):
                frame0.append(verify_char.getpixel((x, row * 32 + y)))
                frame1.append(verify_char.getpixel((16 + x, row * 32 + y)))
        diffs = sum(1 for a, b in zip(frame0, frame1) if a != b)
        status = "OK" if diffs > 0 else "NO ANIMATION!"
        if diffs == 0:
            all_ok = False
        print(f"  {dirs[row]}: frame0 vs frame1 = {diffs} pixel diffs {status}")

    # Check portrait quadrants are not empty
    for qx, qy, name in [
        (0, 0, "Default"), (64, 0, "Happy"),
        (0, 64, "Sad"), (64, 64, "Surprised"),
    ]:
        non_empty = 0
        for y in range(64):
            for x in range(64):
                if verify_port.getpixel((qx + x, qy + y))[3] > 0:
                    non_empty += 1
        status = "OK" if non_empty > 100 else "TOO EMPTY!"
        if non_empty <= 100:
            all_ok = False
        print(f"  Portrait {name}: {non_empty} non-transparent pixels {status}")

    if all_ok:
        print("\nAll checks passed!")
    else:
        print("\nWARNING: Some checks failed!")
