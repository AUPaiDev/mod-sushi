#!/usr/bin/env python3
"""Generate Foyin (佛印) sprite sheet and portrait for Stardew Valley mod.

Foyin is a Northern Song dynasty Buddhist monk, Su Shi's close friend.
Key visual traits: BALD head (no hair at all), saffron/ochre kasaya robes,
stocky/round build (widest of the three NPCs), kind face with squinting eyes.

Sprite layout: 64x128 (4 directions x 4 frames, each 16x32)
Portrait layout: 128x128 (2x2 grid of 64x64)

Art style targets Stardew Valley official NPC proportions:
  y0-1:   head top
  y2-3:   upper head / dome
  y4-9:   face (6px tall, 10px wide) -- face is ~1/3 of sprite
  y10-11: neck / collar
  y12-19: torso
  y20-24: lower body / robe hem
  y25-27: shoes
  y28-31: empty

CRITICAL: Eyes are THE defining feature of Stardew NPCs.
  - Must have clear white (EW) pixels visible
  - Pupil (ED) must contrast strongly against white
  - Eyes at y5-y6 for front view
"""

from PIL import Image

# === COLOR PALETTE (hue-shifted, top-left light source) ===
T = (0, 0, 0, 0)  # transparent

# Outline (warm dark brown, NOT pure black)
OL = (50, 32, 18, 255)     # main outline
OM = (68, 48, 30, 255)     # medium outline for inner detail

# Skin (warm golden, slightly tanned monk)
S0 = (252, 225, 190, 255)  # highlight
S1 = (238, 202, 162, 255)  # base
S2 = (212, 172, 132, 255)  # shadow
S3 = (188, 145, 108, 255)  # deep shadow

# Bald head sheen
HD = (255, 240, 215, 255)  # bright dome highlight

# Kasaya robe (earthy ochre/saffron -- NOT bright orange)
K0 = (225, 188, 98, 255)   # highlight - warm gold
K1 = (198, 158, 65, 255)   # base - ochre
K2 = (165, 125, 48, 255)   # shadow - deeper ochre
K3 = (132, 98, 35, 255)    # deep shadow - brown

# Kasaya diagonal drape accent (slightly different shade)
KD = (185, 142, 55, 255)   # drape line (between K1 and K2)

# Inner robe / collar (dark earth brown)
I0 = (155, 112, 58, 255)   # inner highlight
I1 = (128, 88, 45, 255)    # inner base
I2 = (105, 68, 32, 255)    # inner shadow

# Belt / sash (dark brown rope)
BL = (92, 65, 35, 255)     # belt highlight
BD = (68, 48, 25, 255)     # belt dark

# Prayer beads (dark wood)
P0 = (88, 58, 32, 255)     # bead highlight
P1 = (62, 40, 20, 255)     # bead dark

# Eyes (kind, slightly squinting -- HIGH CONTRAST is key)
ED = (32, 20, 15, 255)     # dark pupil (very dark)
EI = (72, 48, 28, 255)     # warm brown iris
EW = (255, 255, 250, 255)  # bright white (must pop!)

# Cloth shoes (dark)
SH = (78, 55, 35, 255)     # shoe base
SD = (55, 38, 22, 255)     # shoe dark

# Mouth / expression
MT = (172, 122, 92, 255)   # subtle mouth line

# === CHARACTER SPRITE DATA (16x32 per frame) ===
# Foyin: BALD monk, stocky build (widest NPC), kasaya robes
# Head 10px wide (cols 3-12), body up to 14px wide (cols 1-14)
# Eyes at y5-y6: MUST have visible white pixels for Stardew style

# ---- FRONT STANDING (facing south / down) ----
FRONT_STAND = [
    #0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
    [T,   T,   T,   T,   T,   OL,  OL,  OL,  OL,  OL,  T,   T,   T,   T,   T,   T  ],  # y0  dome top
    [T,   T,   T,   T,   OL,  HD,  HD,  S0,  S0,  HD,  OL,  T,   T,   T,   T,   T  ],  # y1  dome sheen
    [T,   T,   T,   OL,  HD,  S0,  S0,  S1,  S1,  S0,  S1,  OL,  T,   T,   T,   T  ],  # y2  upper dome
    [T,   T,   T,   OL,  S0,  S0,  S1,  S1,  S1,  S1,  S1,  S2,  OL,  T,   T,   T  ],  # y3  lower dome
    [T,   T,   T,   OL,  S0,  S1,  S1,  S1,  S1,  S1,  S1,  S2,  OL,  T,   T,   T  ],  # y4  forehead
    [T,   T,   T,   OL,  S0,  EW,  ED,  S1,  S1,  EW,  ED,  S2,  OL,  T,   T,   T  ],  # y5  eyes: W.D _ W.D (squint)
    [T,   T,   T,   OL,  S0,  EI,  S1,  S1,  S1,  EI,  S1,  S2,  OL,  T,   T,   T  ],  # y6  under-eye iris
    [T,   T,   T,   OL,  S1,  S1,  S1,  S2,  S1,  S1,  S1,  S2,  OL,  T,   T,   T  ],  # y7  nose
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S1,  S1,  S3,  OL,  T,   T,   T  ],  # y8  cheeks
    [T,   T,   T,   OL,  S1,  S2,  S1,  MT,  MT,  S1,  S2,  S3,  OL,  T,   T,   T  ],  # y9  mouth + chin
    [T,   T,   T,   T,   OL,  S2,  S1,  S1,  S1,  S1,  S2,  OL,  T,   T,   T,   T  ],  # y10 jaw
    [T,   T,   T,   T,   T,   OL,  S2,  S2,  S2,  S2,  OL,  T,   T,   T,   T,   T  ],  # y11 neck
    [T,   T,   OL,  I0,  I1,  I1,  S2,  S2,  S2,  I1,  I1,  I2,  OL,  T,   T,   T  ],  # y12 collar
    [T,   OL,  I0,  K0,  K1,  I0,  I1,  I1,  I0,  K1,  K1,  K2,  I2,  OL,  T,   T  ],  # y13 V-collar + chest
    [T,   OL,  K0,  K0,  K1,  KD,  K1,  K1,  K1,  K1,  KD,  K1,  K2,  K3,  OL,  T  ],  # y14 chest + drape
    [OL,  K0,  K0,  K1,  K1,  K1,  KD,  K1,  K1,  KD,  K1,  K1,  K2,  K3,  K3,  OL ],  # y15 torso + diagonal
    [OL,  K0,  K0,  K1,  BL,  BD,  BL,  BD,  BL,  BD,  BL,  BD,  K2,  K3,  K3,  OL ],  # y16 belt
    [OL,  K0,  K0,  K1,  K1,  K1,  K1,  KD,  KD,  K1,  K1,  K1,  K2,  K3,  K3,  OL ],  # y17 belly + drape
    [OL,  K0,  K1,  K1,  K1,  K2,  K1,  K1,  K1,  K2,  K1,  K1,  K2,  K3,  K3,  OL ],  # y18 fold
    [T,   OL,  K0,  K1,  K1,  K1,  K1,  K2,  K2,  K1,  K1,  K1,  K2,  K3,  OL,  T  ],  # y19 lower robe
    [T,   OL,  K0,  K1,  K1,  K2,  K2,  K1,  K1,  K2,  K2,  K1,  K2,  K3,  OL,  T  ],  # y20 robe
    [T,   T,   OL,  K1,  K1,  K2,  K1,  K2,  K2,  K1,  K2,  K2,  K3,  OL,  T,   T  ],  # y21 robe lower
    [T,   T,   OL,  K1,  K2,  K2,  K2,  K2,  K2,  K2,  K2,  K2,  K3,  OL,  T,   T  ],  # y22 robe hem
    [T,   T,   T,   OL,  K2,  K2,  K3,  K3,  K3,  K3,  K2,  K3,  OL,  T,   T,   T  ],  # y23 robe bottom
    [T,   T,   T,   T,   OL,  K3,  K3,  K3,  K3,  K3,  K3,  OL,  T,   T,   T,   T  ],  # y24 robe tip
    [T,   T,   T,   T,   T,   OL,  S2,  OL,  OL,  S2,  OL,  T,   T,   T,   T,   T  ],  # y25 ankles
    [T,   T,   T,   T,   T,   OL,  SH,  SD,  SD,  SH,  OL,  T,   T,   T,   T,   T  ],  # y26 shoes
    [T,   T,   T,   T,   T,   T,   OL,  OL,  OL,  OL,  T,   T,   T,   T,   T,   T  ],  # y27 soles
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y28
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y29
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y30
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y31
]

# ---- RIGHT STANDING (facing east) ----
# Profile: bald dome, one eye visible (white+pupil), kasaya drape
RIGHT_STAND = [
    #0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y0
    [T,   T,   T,   T,   T,   OL,  OL,  OL,  OL,  OL,  T,   T,   T,   T,   T,   T  ],  # y1  dome top
    [T,   T,   T,   T,   OL,  HD,  S0,  S0,  S1,  S1,  OL,  T,   T,   T,   T,   T  ],  # y2  dome
    [T,   T,   T,   OL,  S0,  S0,  S1,  S1,  S1,  S1,  S2,  OL,  T,   T,   T,   T  ],  # y3  head
    [T,   T,   T,   OL,  S0,  S1,  S1,  S1,  S1,  S1,  S2,  OL,  T,   T,   T,   T  ],  # y4  forehead
    [T,   T,   T,   OL,  S0,  S1,  S1,  EW,  ED,  S1,  S2,  OL,  T,   T,   T,   T  ],  # y5  eye: W.D (squint)
    [T,   T,   T,   OL,  S1,  S1,  S1,  EI,  S1,  S1,  S2,  OL,  T,   T,   T,   T  ],  # y6  under-eye
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S2,  S2,  S2,  OL,  T,   T,   T,   T  ],  # y7  nose
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S2,  S3,  OL,  T,   T,   T,   T  ],  # y8  cheek
    [T,   T,   T,   OL,  S1,  S2,  S1,  MT,  S1,  S2,  S3,  OL,  T,   T,   T,   T  ],  # y9  chin
    [T,   T,   T,   T,   OL,  S2,  S1,  S1,  S2,  S2,  OL,  T,   T,   T,   T,   T  ],  # y10 jaw
    [T,   T,   T,   T,   T,   OL,  S2,  S2,  S2,  OL,  T,   T,   T,   T,   T,   T  ],  # y11 neck
    [T,   T,   OL,  I0,  I1,  I1,  S2,  S2,  I1,  I1,  I2,  OL,  T,   T,   T,   T  ],  # y12 collar
    [T,   OL,  K0,  K0,  K1,  K1,  I0,  K1,  K1,  K1,  K2,  K2,  OL,  T,   T,   T  ],  # y13 upper body
    [T,   OL,  K0,  K1,  K1,  KD,  K1,  K1,  K1,  K1,  K2,  K2,  OL,  T,   T,   T  ],  # y14 chest + drape
    [OL,  K0,  K0,  K1,  K1,  K1,  KD,  K1,  K1,  K1,  K2,  K3,  K3,  OL,  T,   T  ],  # y15 torso
    [OL,  K0,  K0,  K1,  BL,  BD,  BL,  BD,  K1,  K1,  K2,  K3,  K3,  OL,  T,   T  ],  # y16 belt
    [OL,  K0,  K1,  K1,  K1,  K1,  K1,  KD,  K1,  K2,  K2,  K3,  K3,  OL,  T,   T  ],  # y17 belly
    [OL,  K0,  K1,  K1,  K1,  K2,  K1,  K1,  KD,  K2,  K2,  K3,  K3,  OL,  T,   T  ],  # y18 fold
    [T,   OL,  K0,  K1,  K1,  K1,  K1,  K2,  K2,  K2,  K3,  K3,  OL,  T,   T,   T  ],  # y19 lower robe
    [T,   OL,  K1,  K1,  K2,  K2,  K1,  K2,  K2,  K3,  K3,  K3,  OL,  T,   T,   T  ],  # y20 robe
    [T,   T,   OL,  K1,  K2,  K2,  K2,  K2,  K3,  K3,  K3,  OL,  T,   T,   T,   T  ],  # y21 robe lower
    [T,   T,   T,   OL,  K2,  K2,  K2,  K3,  K3,  K3,  OL,  T,   T,   T,   T,   T  ],  # y22 robe hem
    [T,   T,   T,   T,   OL,  K2,  K3,  K3,  K3,  OL,  T,   T,   T,   T,   T,   T  ],  # y23 robe bottom
    [T,   T,   T,   T,   T,   OL,  K3,  K3,  K3,  OL,  T,   T,   T,   T,   T,   T  ],  # y24 robe tip
    [T,   T,   T,   T,   T,   OL,  S2,  OL,  OL,  SH,  OL,  T,   T,   T,   T,   T  ],  # y25 ankles
    [T,   T,   T,   T,   T,   T,   OL,  SH,  SD,  SH,  OL,  T,   T,   T,   T,   T  ],  # y26 shoes
    [T,   T,   T,   T,   T,   T,   T,   OL,  OL,  OL,  T,   T,   T,   T,   T,   T  ],  # y27 soles
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y28
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y29
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y30
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y31
]

# ---- BACK STANDING (facing north / up) ----
BACK_STAND = [
    #0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
    [T,   T,   T,   T,   T,   OL,  OL,  OL,  OL,  OL,  T,   T,   T,   T,   T,   T  ],  # y0  dome top
    [T,   T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S2,  OL,  T,   T,   T,   T,   T  ],  # y1  back dome
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S2,  S2,  OL,  T,   T,   T,   T  ],  # y2  dome
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S1,  S2,  S2,  OL,  T,   T,   T  ],  # y3  head
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S1,  S2,  S2,  OL,  T,   T,   T  ],  # y4  head
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S1,  S2,  S2,  OL,  T,   T,   T  ],  # y5  head
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S1,  S2,  S2,  OL,  T,   T,   T  ],  # y6  head
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S1,  S2,  S2,  OL,  T,   T,   T  ],  # y7  head
    [T,   T,   T,   OL,  S1,  S1,  S1,  S1,  S1,  S1,  S2,  S2,  OL,  T,   T,   T  ],  # y8  head
    [T,   T,   T,   OL,  S1,  S2,  S1,  S1,  S1,  S1,  S2,  S3,  OL,  T,   T,   T  ],  # y9  head back
    [T,   T,   T,   T,   OL,  S2,  S2,  S2,  S2,  S2,  S3,  OL,  T,   T,   T,   T  ],  # y10 neck
    [T,   T,   T,   T,   T,   OL,  S2,  S2,  S2,  S2,  OL,  T,   T,   T,   T,   T  ],  # y11 neck
    [T,   T,   OL,  I0,  I1,  I1,  S2,  S2,  S2,  I1,  I1,  I2,  OL,  T,   T,   T  ],  # y12 collar
    [T,   OL,  K0,  K0,  K1,  K1,  I0,  I1,  I0,  K1,  K1,  K2,  K3,  OL,  T,   T  ],  # y13 upper back
    [T,   OL,  K0,  K0,  K1,  K1,  K1,  K1,  K1,  K1,  K1,  K2,  K3,  OL,  T,   T  ],  # y14 back
    [OL,  K0,  K0,  K1,  K1,  K1,  K1,  K1,  K1,  K1,  K1,  K2,  K3,  K3,  OL,  T  ],  # y15 wide back
    [OL,  K0,  K0,  K1,  BL,  BD,  BL,  BD,  BL,  BD,  BL,  BD,  K3,  K3,  K3,  OL ],  # y16 belt
    [OL,  K0,  K0,  K1,  K1,  K1,  K1,  K1,  K1,  K1,  K1,  K2,  K3,  K3,  K3,  OL ],  # y17 belly
    [OL,  K0,  K1,  K1,  K1,  K2,  K1,  K1,  K1,  K2,  K1,  K2,  K3,  K3,  K3,  OL ],  # y18 fold
    [T,   OL,  K0,  K1,  K1,  K1,  K2,  K2,  K2,  K1,  K2,  K2,  K3,  K3,  OL,  T  ],  # y19 lower robe
    [T,   OL,  K1,  K1,  K2,  K2,  K1,  K2,  K2,  K2,  K2,  K3,  K3,  K3,  OL,  T  ],  # y20 robe
    [T,   T,   OL,  K1,  K2,  K2,  K2,  K2,  K2,  K2,  K3,  K3,  K3,  OL,  T,   T  ],  # y21 robe lower
    [T,   T,   OL,  K1,  K2,  K2,  K2,  K2,  K2,  K2,  K3,  K3,  K3,  OL,  T,   T  ],  # y22 robe hem
    [T,   T,   T,   OL,  K2,  K2,  K3,  K3,  K3,  K3,  K3,  K3,  OL,  T,   T,   T  ],  # y23 robe bottom
    [T,   T,   T,   T,   OL,  K3,  K3,  K3,  K3,  K3,  K3,  OL,  T,   T,   T,   T  ],  # y24 robe tip
    [T,   T,   T,   T,   T,   OL,  S2,  OL,  OL,  S2,  OL,  T,   T,   T,   T,   T  ],  # y25 ankles
    [T,   T,   T,   T,   T,   OL,  SH,  SD,  SD,  SH,  OL,  T,   T,   T,   T,   T  ],  # y26 shoes
    [T,   T,   T,   T,   T,   T,   OL,  OL,  OL,  OL,  T,   T,   T,   T,   T,   T  ],  # y27 soles
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y28
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y29
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y30
    [T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T,   T  ],  # y31
]

# Left-facing = mirror of right-facing
def mirror_frame(frame):
    return [list(reversed(row)) for row in frame]

LEFT_STAND = mirror_frame(RIGHT_STAND)

def make_walk_frame(stand, step_side, direction):
    """Generate a walk frame from standing frame.
    Head bobs down 1px, feet split apart to show stepping.
    """
    import copy
    frame = copy.deepcopy(stand)

    # Find the first non-empty row
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

    # Leg animation (y23-y27)
    if direction in ('front', 'back'):
        if step_side == 'left':
            frame[23] = [T,T,T,OL,K2,K2,K3,K3,K3,K2,K3,K3,OL,T,T,T]
            frame[24] = [T,T,OL,K3,K3,K3,T,T,T,T,K3,K3,K3,OL,T,T]
            frame[25] = [T,T,OL,SH,OL,T,T,T,T,T,T,OL,SH,OL,T,T]
            frame[26] = [T,T,OL,SH,SD,OL,T,T,T,T,OL,SH,SD,OL,T,T]
            frame[27] = [T,T,T,OL,OL,T,T,T,T,T,T,OL,OL,T,T,T]
        else:
            frame[23] = [T,T,T,OL,K2,K2,K3,K3,K3,K2,K3,K3,OL,T,T,T]
            frame[24] = [T,OL,K3,K3,K3,T,T,T,T,T,K3,K3,K3,OL,T,T]
            frame[25] = [T,OL,SH,OL,T,T,T,T,T,T,T,OL,SH,OL,T,T]
            frame[26] = [OL,SH,SD,OL,T,T,T,T,T,T,OL,SH,SD,OL,T,T]
            frame[27] = [T,OL,OL,T,T,T,T,T,T,T,T,OL,OL,T,T,T]
    elif direction == 'right':
        if step_side == 'left':
            frame[23] = [T,T,T,T,OL,K2,K3,K3,K3,OL,T,T,T,T,T,T]
            frame[24] = [T,T,T,OL,K3,K3,K3,OL,T,T,T,T,T,T,T,T]
            frame[25] = [T,T,T,OL,SH,OL,T,T,OL,SH,OL,T,T,T,T,T]
            frame[26] = [T,T,T,OL,SH,SD,OL,T,OL,SH,SD,OL,T,T,T,T]
            frame[27] = [T,T,T,T,OL,OL,T,T,T,OL,OL,T,T,T,T,T]
        else:
            frame[23] = [T,T,T,T,OL,K2,K3,K3,K3,OL,T,T,T,T,T,T]
            frame[24] = [T,T,T,T,T,T,OL,K3,K3,K3,OL,T,T,T,T,T]
            frame[25] = [T,T,T,T,T,OL,SH,OL,T,OL,SH,OL,T,T,T,T]
            frame[26] = [T,T,T,T,OL,SH,SD,OL,T,OL,SH,SD,OL,T,T,T]
            frame[27] = [T,T,T,T,T,OL,OL,T,T,T,OL,OL,T,T,T,T]
    elif direction == 'left':
        if step_side == 'left':
            frame[23] = [T,T,T,T,T,T,OL,K3,K3,K2,OL,T,T,T,T,T]
            frame[24] = [T,T,T,T,T,T,OL,K3,K3,K3,OL,T,T,T,T,T]
            frame[25] = [T,T,T,T,T,OL,SH,OL,T,OL,SH,OL,T,T,T,T]
            frame[26] = [T,T,T,T,OL,SH,SD,OL,T,OL,SH,SD,OL,T,T,T]
            frame[27] = [T,T,T,T,T,OL,OL,T,T,T,OL,OL,T,T,T,T]
        else:
            frame[23] = [T,T,T,T,T,T,OL,K3,K3,K2,OL,T,T,T,T,T]
            frame[24] = [T,T,T,T,OL,K3,K3,K3,OL,T,T,T,T,T,T,T]
            frame[25] = [T,T,T,OL,SH,OL,T,T,OL,SH,OL,T,T,T,T,T]
            frame[26] = [T,T,T,OL,SH,SD,OL,T,OL,SH,SD,OL,T,T,T,T]
            frame[27] = [T,T,T,T,OL,OL,T,T,T,OL,OL,T,T,T,T,T]

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
        paint_frame(img, stand_frame, 0, base_y)
        walk_l = make_walk_frame(stand_frame, 'left', dir_name)
        paint_frame(img, walk_l, 16, base_y)
        paint_frame(img, stand_frame, 32, base_y)
        walk_r = make_walk_frame(stand_frame, 'right', dir_name)
        paint_frame(img, walk_r, 48, base_y)

    return img


# === PORTRAIT GENERATION (128x128 = 2x2 grid of 64x64) ===

def generate_portrait_default(img, ox, oy):
    """Default expression: serene, calm Buddhist monk.
    Bald dome with highlight, round face, kind eyes, kasaya, prayer beads.
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
    fill_rect(22, 2, 41, 4, S1)     # top dome
    fill_rect(19, 5, 44, 8, S1)     # upper dome
    fill_rect(18, 9, 45, 13, S1)    # mid dome into face

    # Dome highlight (top-left light)
    fill_rect(22, 2, 34, 3, HD)     # bright sheen
    fill_rect(22, 2, 28, 3, HD)     # brightest
    fill_rect(19, 4, 33, 7, S0)     # left highlight
    fill_rect(38, 5, 44, 8, S2)     # right shadow
    fill_rect(41, 9, 45, 13, S2)    # right shadow lower

    # Head outline
    hline(22, 41, 1, OL)
    for y in range(2, 5):
        p(21, y, OL); p(42, y, OL)
    for y in range(5, 9):
        p(18, y, OL); p(45, y, OL)
    for y in range(9, 14):
        p(17, y, OL); p(46, y, OL)

    # --- Face (wide, round) ---
    fill_rect(18, 14, 45, 33, S1)
    fill_rect(18, 14, 32, 17, S0)   # forehead highlight
    fill_rect(40, 14, 45, 33, S2)   # right face shadow
    fill_rect(18, 24, 20, 30, S2)   # left cheek shadow
    fill_rect(43, 24, 45, 30, S3)   # right cheek deep shadow
    fill_rect(22, 31, 41, 33, S2)   # chin roundness
    hline(24, 39, 33, S3)

    # Face outline continues
    for y in range(14, 34):
        p(17, y, OL); p(46, y, OL)
    hline(19, 44, 34, OL)
    p(18, 33, OL); p(45, 33, OL)

    # --- Eyes (kind, 3 rows for portrait -- PROMINENT) ---
    # Left eye: top lash, white+iris+pupil, bottom lash
    hline(24, 28, 18, ED)                                    # top lash
    p(24, 19, ED); p(25, 19, EW); p(26, 19, EW); p(27, 19, EI); p(28, 19, ED)  # white+iris
    hline(24, 28, 20, OM)                                    # bottom lash
    # Right eye
    hline(35, 39, 18, ED)                                    # top lash
    p(35, 19, ED); p(36, 19, EI); p(37, 19, EW); p(38, 19, EW); p(39, 19, ED)  # iris+white
    hline(35, 39, 20, OM)                                    # bottom lash

    # --- Nose (wide, round) ---
    p(31, 24, S2); p(32, 24, S2)
    p(30, 25, S3); p(31, 25, S3); p(32, 25, S2); p(33, 25, S3)

    # --- Mouth (serene slight smile) ---
    hline(29, 34, 28, S3)
    p(28, 28, S2); p(35, 28, S2)  # smile corners up
    hline(30, 33, 29, S2)

    # --- Neck (thick, stocky) ---
    fill_rect(26, 34, 37, 38, S1)
    fill_rect(26, 34, 32, 36, S0)
    fill_rect(35, 34, 37, 38, S2)

    # --- Collar (inner robe V-neck) ---
    fill_rect(14, 39, 49, 41, I1)
    hline(14, 28, 39, I0)
    hline(38, 49, 39, I2)
    for i in range(3):
        p(30 - i, 39 + i, S2)
        p(33 + i, 39 + i, S2)

    # --- Kasaya robe body ---
    fill_rect(10, 42, 53, 57, K1)
    fill_rect(10, 42, 24, 57, K0)   # left highlight
    fill_rect(44, 42, 53, 57, K2)   # right shadow

    # Diagonal drape line (left shoulder to right hip)
    for i in range(10):
        dx = 20 + i * 2
        dy = 42 + i
        if dx < 53 and dy < 57:
            p(dx, dy, KD); p(dx + 1, dy, KD)

    # Prayer beads (diagonal across chest)
    for i in range(7):
        bx = 22 + i * 3
        by = 43 + i
        if bx < 53 and by < 57:
            p(bx, by, P0); p(bx + 1, by, P1)

    # Belt line
    fill_rect(10, 49, 53, 50, BD)
    fill_rect(10, 49, 24, 50, BL)

    # Robe folds
    for y in range(51, 57):
        p(26, y, K2); p(37, y, K2)

    # Bottom robe
    fill_rect(10, 57, 53, 63, K2)
    fill_rect(10, 57, 24, 63, K1)
    fill_rect(44, 57, 53, 63, K3)

    # Robe outline
    for y in range(39, 63):
        p(9, y, OL); p(54, y, OL)
    hline(9, 54, 63, OL)


def generate_portrait_happy(img, ox, oy):
    """Happy/laughing -- Foyin's hearty belly laugh.
    Crescent eyes ^_^, wide open mouth, rosy cheeks.
    """
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)

    # Clear default eyes (3 rows)
    for x in range(24, 29):
        p(x, 18, S1); p(x, 19, S1); p(x, 20, S1)
    for x in range(35, 40):
        p(x, 18, S1); p(x, 19, S1); p(x, 20, S1)

    # Crescent eyes ^_^ (arched upward)
    p(24, 20, OM); p(25, 19, OM); p(26, 18, OM); p(27, 19, OM); p(28, 20, OM)
    p(35, 20, OM); p(36, 19, OM); p(37, 18, OM); p(38, 19, OM); p(39, 20, OM)

    # Rosy cheeks
    p(22, 22, (235, 175, 155, 255)); p(23, 22, (235, 175, 155, 255))
    p(40, 22, (235, 175, 155, 255)); p(41, 22, (235, 175, 155, 255))

    # Clear default mouth
    for y in range(28, 30):
        hline(28, 35, y, S1)

    # Wide laughing mouth (open, 3 rows)
    hline(27, 36, 27, ED)           # top lip
    p(27, 28, ED); hline(28, 35, 28, S0); p(36, 28, ED)  # teeth
    p(27, 29, ED); hline(28, 35, 29, (175, 82, 68, 255)); p(36, 29, ED)  # tongue
    hline(27, 36, 30, ED)           # bottom lip

    # Laugh lines
    p(22, 20, S2); p(22, 21, S2)
    p(41, 20, S2); p(41, 21, S2)


def generate_portrait_pensive(img, ox, oy):
    """Pensive/contemplative -- deep meditation.
    Nearly closed eyes (thin lines), neutral/slight frown.
    """
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)

    # Clear default eyes (3 rows)
    for x in range(24, 29):
        p(x, 18, S1); p(x, 19, S1); p(x, 20, S1)
    for x in range(35, 40):
        p(x, 18, S1); p(x, 19, S1); p(x, 20, S1)

    # Nearly closed meditative eyes (single line + shadow)
    hline(24, 28, 19, ED)
    hline(35, 39, 19, ED)
    hline(24, 28, 18, S2)   # lid shadow
    hline(35, 39, 18, S2)

    # Clear default mouth
    for y in range(28, 30):
        hline(28, 35, y, S1)

    # Neutral contemplative mouth (straight line, slight downturn)
    hline(30, 33, 28, S3)
    p(29, 29, S3); p(34, 29, S3)  # downturn corners


def generate_portrait_surprised(img, ox, oy):
    """Surprised -- wide round eyes, O-shaped mouth, raised brows.
    """
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)
    def fill_rect(x1, y1, x2, y2, c):
        for yy in range(y1, y2 + 1):
            hline(x1, x2, yy, c)

    # Clear default eyes (3 rows)
    for x in range(24, 29):
        p(x, 18, S1); p(x, 19, S1); p(x, 20, S1)
    for x in range(35, 40):
        p(x, 18, S1); p(x, 19, S1); p(x, 20, S1)

    # Raised eyebrows (2px above eyes)
    hline(24, 28, 16, OM); hline(24, 28, 17, S0)
    hline(35, 39, 16, OM); hline(35, 39, 17, S0)

    # Wide round eyes (4 rows -- bigger than default)
    # Left eye
    hline(24, 28, 18, ED)                                                # top
    p(24, 19, ED); p(25, 19, EW); p(26, 19, EW); p(27, 19, EI); p(28, 19, ED)
    p(24, 20, ED); p(25, 20, EW); p(26, 20, EI); p(27, 20, ED); p(28, 20, ED)
    hline(24, 28, 21, ED)                                                # bottom
    # Right eye
    hline(35, 39, 18, ED)
    p(35, 19, ED); p(36, 19, EI); p(37, 19, EW); p(38, 19, EW); p(39, 19, ED)
    p(35, 20, ED); p(36, 20, ED); p(37, 20, EI); p(38, 20, EW); p(39, 20, ED)
    hline(35, 39, 21, ED)

    # Clear default mouth
    for y in range(28, 30):
        hline(28, 35, y, S1)

    # Open O-shaped mouth (round, 3x3)
    hline(30, 33, 27, ED)
    p(30, 28, ED); p(31, 28, S3); p(32, 28, S3); p(33, 28, ED)
    p(30, 29, ED); p(31, 29, S3); p(32, 29, S3); p(33, 29, ED)
    hline(30, 33, 30, ED)


def generate_portrait_sheet():
    """Generate 128x128 portrait sheet (2x2 grid of 64x64).
    Top-left: default (serene)
    Top-right: happy (laughing)
    Bottom-left: pensive (contemplative)
    Bottom-right: surprised
    """
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

    generate_portrait_default(img, 0, 0)
    generate_portrait_happy(img, 64, 0)
    generate_portrait_pensive(img, 0, 64)
    generate_portrait_surprised(img, 64, 64)

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

    # Check portrait quadrants have content and differ
    quadrants = [("Default", 0, 0), ("Happy", 64, 0),
                 ("Pensive", 0, 64), ("Surprised", 64, 64)]
    quad_data = {}
    for qname, qx, qy in quadrants:
        px_count = 0
        pixels = []
        for y in range(64):
            for x in range(64):
                px = verify_port.getpixel((qx + x, qy + y))
                if px[3] > 0:
                    px_count += 1
                pixels.append(px)
        quad_data[qname] = pixels
        print(f"  Portrait {qname}: {px_count} non-transparent pixels {'OK' if px_count > 100 else 'TOO FEW!'}")

    # Check expressions differ from default
    for qname in ["Happy", "Pensive", "Surprised"]:
        diffs = sum(1 for a, b in zip(quad_data["Default"], quad_data[qname]) if a != b)
        print(f"  {qname} vs Default: {diffs} pixel diffs {'OK' if diffs > 20 else 'TOO SIMILAR!'}")
