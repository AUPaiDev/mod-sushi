#!/usr/bin/env python3
"""Generate improved SuShi (苏轼) sprite sheet and portrait for Stardew Valley mod.

Su Shi: Northern Song dynasty literary giant, male.
- Blue scholar robe (蓝色文人长袍)
- Black scholar cap / Dongpo turban (东坡巾)
- Beard (胡须)
- Bamboo walking staff (竹杖)
- Taller, broader build than Zhaoyun (male proportions)
"""

from PIL import Image

# === COLOR PALETTE (with hue shifting, light from top-left) ===
T = (0, 0, 0, 0)  # transparent

# Outline colors (colored, not pure black)
OL_DARK = (20, 18, 30, 255)    # deep blue-black, main outline
OL_MED  = (35, 32, 42, 255)    # medium outline for inner details
OL_HAT  = (18, 16, 28, 255)    # very dark for hat outline

# Skin (warm, top-left lighting — male, slightly darker than Zhaoyun)
SK_HI  = (248, 216, 192, 255)  # highlight
SK_BASE = (235, 198, 168, 255) # base
SK_SH  = (210, 170, 138, 255)  # shadow
SK_DSH = (185, 140, 112, 255)  # deep shadow

# Hat / hair (black scholar cap — Dongpo turban)
HT_HI  = (50, 48, 62, 255)    # highlight — slight blue sheen
HT_BASE = (28, 25, 38, 255)   # base — very dark
HT_SH  = (18, 15, 25, 255)    # shadow

# Blue scholar robe (main clothing)
CL_HI  = (155, 195, 235, 255) # highlight — light sky blue
CL_BASE = (110, 155, 205, 255)# base — medium blue
CL_SH  = (75, 110, 165, 255)  # shadow — deeper blue
CL_DSH = (50, 78, 130, 255)   # deep shadow — navy

# Inner robe / collar accent (white-cream)
IC_HI  = (245, 240, 232, 255) # highlight
IC_BASE = (228, 220, 208, 255)# base
IC_SH  = (205, 195, 182, 255) # shadow

# Belt / sash (dark brown-gold)
SA_HI  = (165, 135, 85, 255)  # gold-brown highlight
SA_BASE = (135, 108, 65, 255) # base
SA_SH  = (105, 82, 48, 255)   # shadow

# Beard (dark brown)
BD_HI  = (72, 60, 48, 255)    # highlight
BD_BASE = (52, 42, 35, 255)   # base
BD_SH  = (38, 30, 25, 255)    # shadow

# Eye colors
EYE_DARK = (25, 20, 22, 255)
EYE_IRIS = (65, 45, 35, 255)  # dark brown iris
EYE_HI   = (255, 255, 255, 255)

# Bamboo staff (green-brown)
BM_HI  = (115, 148, 62, 255)
BM_BASE = (88, 118, 42, 255)
BM_SH  = (62, 85, 28, 255)

# Boots (dark leather)
BT_HI  = (65, 55, 48, 255)
BT_BASE = (45, 38, 32, 255)
BT_SH  = (32, 26, 22, 255)

# === SHORTHAND ALIASES ===
O = OL_DARK
M = OL_MED
Hh = OL_HAT   # hat outline (avoid clash with 'H' for hair in zhaoyun)

s0 = SK_HI
s1 = SK_BASE
s2 = SK_SH
s3 = SK_DSH

ht0 = HT_HI
ht1 = HT_BASE
ht2 = HT_SH

c0 = CL_HI
c1 = CL_BASE
c2 = CL_SH
c3 = CL_DSH

ic0 = IC_HI
ic1 = IC_BASE
ic2 = IC_SH

sa0 = SA_HI
sa1 = SA_BASE
sa2 = SA_SH

bd0 = BD_HI
bd1 = BD_BASE
bd2 = BD_SH

ed = EYE_DARK
ei = EYE_IRIS
eh = EYE_HI

bm0 = BM_HI
bm1 = BM_BASE
bm2 = BM_SH

bt0 = BT_HI
bt1 = BT_BASE
bt2 = BT_SH

# === CHARACTER SPRITE (16x32 per frame) ===
# Su Shi: male, taller/broader than Zhaoyun
# Scholar cap (东坡巾), blue robe, beard, bamboo staff on right side
# Eyes: 2-row (lash line + iris/highlight), no separate eyebrow row
# Light source: top-left

# Front-facing standing frame (facing down/south)
FRONT_STAND = [
    #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
    [T,  T,  T,  T,  T,  Hh, Hh, Hh, Hh, Hh, Hh, T,  T,  T,  T,  T ],  # y0  hat top
    [T,  T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1, Hh, T,  T,  T,  T ],  # y1  hat body
    [T,  T,  T,  Hh,ht0,ht0,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T ],  # y2  hat body
    [T,  T,  Hh,ht0,ht0,ht1,ht1,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T ],  # y3  hat brim
    [T,  T,  T,  Hh,ht1, s0, s0, s1, s1, s1, s2,ht2, Hh, T,  T,  T ],  # y4  forehead
    [T,  T,  T,  Hh,ht1, s0, s1, s1, s1, s1, s2,ht2, Hh, T,  T,  T ],  # y5  upper face
    [T,  T,  T,  Hh, s0, s0, ed, s1, s1, ed, s1, s2, Hh, T,  T,  T ],  # y6  eye top (lash)
    [T,  T,  T,  Hh, s0, eh, ei, s1, s1, ei, ed, s2, Hh, T,  T,  T ],  # y7  eye bottom (iris)
    [T,  T,  T,  Hh, s1, s1, s1, s2, s1, s1, s1, s2, Hh, T,  T,  T ],  # y8  nose
    [T,  T,  T,  Hh, s1, s1, s1, s1, s1, s1, s1, s3, Hh, T,  T,  T ],  # y9  upper lip area
    [T,  T,  T,  Hh, s2,bd0,bd1, s2, s2,bd1,bd0, s3, Hh, T,  T,  T ],  # y10 beard
    [T,  T,  T,  Hh, s2,bd1,bd2,bd1,bd1,bd2,bd1, s3, Hh, T,  T,  T ],  # y11 beard lower
    [T,  T,  T,  O,  s2, s2,bd2,bd2,bd2,bd2, s2, s3, O,  T,  T,  T ],  # y12 chin + beard tip
    [T,  T,  O, ic0,ic0,ic1, s2, s2, s2,ic1,ic1,ic2, O,  T,  T,  T ],  # y13 collar
    [T,  O,  O, c0, c0, c1,ic0,ic1,ic1, c1, c1, c2, O,  O,  T,  T ],  # y14 upper body + V collar
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c1, c2, c2, O,  T,  T ],  # y15 chest
    [T,  O,  c0, c0, c1,sa0,sa1,sa1,sa1,sa0, c1, c2, c2, O,  T,  T ],  # y16 sash
    [T,  O,  c0, c0, c1,sa1,sa2,sa2,sa2,sa1, c1, c2, c2, O,  T,  T ],  # y17 sash lower
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c1, c2, c2, O,  T,  T ],  # y18 waist
    [T,  O,  c0, c1, c1, c1, c1, c2, c2, c1, c1, c2, c3, O,  T,  T ],  # y19 hip
    [T,  O,  c0, c1, c1, c1, c2, c1, c1, c2, c1, c2, c3, O,  T,  T ],  # y20 robe fold
    [T,  O,  c0, c1, c1, c2, c2, c2, c2, c2, c2, c3, c3, O,  T,  T ],  # y21 robe
    [T,  T,  O,  c1, c1, c2, c2, c2, c2, c2, c2, c3, O,  T,  T,  T ],  # y22 robe lower
    [T,  T,  O,  c1, c2, c2, c3, c3, c3, c2, c3, c3, O,  T,  T,  T ],  # y23 robe hem
    [T,  T,  T,  O,  c2, c3, c3, O,  O,  c3, c3, O,  T,  T,  T,  T ],  # y24 ankles
    [T,  T,  T,  O, bt0,bt1, O,  T,  T,  O, bt0,bt1, O,  T,  T,  T ],  # y25 boots
    [T,  T,  T,  O, bt0,bt1,bt2, O,  O, bt1,bt0,bt2, O,  T,  T,  T ],  # y26 boots
    [T,  T,  T,  T,  O,  O,  O,  T,  T,  O,  O,  O,  T,  T,  T,  T ],  # y27 boot soles
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y28
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y29
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y30
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y31
]

# Right-facing standing frame — wider body (13px), staff visible behind
RIGHT_STAND = [
    #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
    [T,  T,  T,  T,  T,  Hh, Hh, Hh, Hh, Hh, T,  T,  T,  T,  T,  T ],  # y0  hat top
    [T,  T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1, Hh, T,  T,  T,  T,  T ],  # y1  hat
    [T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T,  T ],  # y2  hat
    [T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T ],  # y3  hat brim
    [T,  T,  T,  Hh,ht1, s0, s1, s1, s1, s1,ht2, Hh, T,  T,  T,  T ],  # y4  forehead
    [T,  T,  T,  Hh, s0, s0, s1, s1, s1, s1, s2, Hh, T,  T,  T,  T ],  # y5  face
    [T,  T,  T,  Hh, s0, s1, s1, ed, s1, s1, s2, Hh, T,  T,  T,  T ],  # y6  eye top
    [T,  T,  T,  Hh, s0, s1, s1, ei, eh, s1, s2, Hh, T,  T,  T,  T ],  # y7  eye bottom
    [T,  T,  T,  Hh, s1, s1, s1, s1, s2, s2, s2, Hh, T,  T,  T,  T ],  # y8  nose
    [T,  T,  T,  Hh, s1, s1, s1, s1, s1, s2, s3, Hh, T,  T,  T,  T ],  # y9  mouth area
    [T,  T,  T,  Hh, s2,bd0,bd1,bd1, s2, s2, s3, Hh, T,  T,  T,  T ],  # y10 beard
    [T,  T,  T,  Hh, s2,bd1,bd2,bd1, s2, s3, s3, Hh, T,  T,  T,  T ],  # y11 beard
    [T,  T,  T,  O,  s2, s2,bd2, s2, s2, s3, O,  T,  T,  T,  T,  T ],  # y12 chin
    [T,  T,  O, ic0,ic1, s2, s2,ic1,ic1, c1, c2, O,  T,  T,  T,  T ],  # y13 collar
    [T,  O,  c0, c0, c1, c1,ic0, c1, c1, c1, c2, c2, O,  T,  T,  T ],  # y14 body
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c2, c2, O,  T,  T,  T ],  # y15 chest
    [T,  O,  c0, c0, c1,sa0,sa1,sa1, c1, c1, c2, c2, O,  T,  T,  T ],  # y16 sash
    [T,  O,  c0, c0, c1,sa1,sa2,sa2, c1, c1, c2, c2, O,  T,  T,  T ],  # y17 sash
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c2, c2, O,  T,  T,  T ],  # y18 waist
    [T,  O,  c0, c1, c1, c1, c1, c2, c1, c1, c2, c3, O,  T,  T,  T ],  # y19 hip
    [T,  O,  c0, c1, c1, c2, c1, c1, c2, c2, c2, c3, O,  T,  T,  T ],  # y20 robe
    [T,  O,  c1, c1, c2, c2, c2, c2, c2, c2, c3, c3, O,  T,  T,  T ],  # y21 robe
    [T,  T,  O,  c1, c2, c2, c2, c2, c2, c3, c3, O,  T,  T,  T,  T ],  # y22 robe lower
    [T,  T,  T,  O,  c2, c3, c3, c3, c3, c3, O,  T,  T,  T,  T,  T ],  # y23 robe hem
    [T,  T,  T,  T,  O,  c3, c3, c3, c3, O,  T,  T,  T,  T,  T,  T ],  # y24 ankles
    [T,  T,  T,  T,  O, bt0, O,  T,  O, bt0, O,  T,  T,  T,  T,  T ],  # y25 boots
    [T,  T,  T,  T,  O, bt0,bt1, O, bt0,bt1, O,  T,  T,  T,  T,  T ],  # y26 boots
    [T,  T,  T,  T,  T,  O,  O,  T,  O,  O,  T,  T,  T,  T,  T,  T ],  # y27 soles
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y28
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y29
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y30
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y31
]

# Back-facing standing frame — hat visible, robe back, no face
BACK_STAND = [
    #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
    [T,  T,  T,  T,  T,  Hh, Hh, Hh, Hh, Hh, Hh, T,  T,  T,  T,  T ],  # y0  hat top
    [T,  T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1, Hh, T,  T,  T,  T ],  # y1  hat
    [T,  T,  T,  Hh,ht0,ht0,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T ],  # y2  hat
    [T,  T,  Hh,ht0,ht0,ht1,ht1,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T ],  # y3  hat brim
    [T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T ],  # y4  back of head
    [T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T ],  # y5  back of head
    [T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T ],  # y6  back of head
    [T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T ],  # y7  back of head
    [T,  T,  T,  Hh,ht0,ht1,ht1,ht1,ht1,ht1,ht1,ht2, Hh, T,  T,  T ],  # y8  back of head
    [T,  T,  T,  Hh, s0, s1, s1, s1, s1, s1, s1, s2, Hh, T,  T,  T ],  # y9  neck back
    [T,  T,  T,  Hh, s1, s1, s1, s1, s1, s1, s1, s2, Hh, T,  T,  T ],  # y10 neck
    [T,  T,  T,  Hh, s2, s2, s2, s2, s2, s2, s2, s3, Hh, T,  T,  T ],  # y11 neck base
    [T,  T,  T,  O, ic0,ic1, s2, s2, s2,ic1,ic2, O,  O,  T,  T,  T ],  # y12 collar back
    [T,  T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c2, O,  T,  T,  T ],  # y13 upper back
    [T,  O,  c0, c0, c0, c1, c1, c1, c1, c1, c1, c2, c2, O,  T,  T ],  # y14 back
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c1, c2, c2, O,  T,  T ],  # y15 back
    [T,  O,  c0, c0, c1,sa0,sa1,sa1,sa1,sa0, c1, c2, c2, O,  T,  T ],  # y16 sash
    [T,  O,  c0, c0, c1,sa1,sa2,sa2,sa2,sa1, c1, c2, c2, O,  T,  T ],  # y17 sash
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c1, c2, c2, O,  T,  T ],  # y18 waist
    [T,  O,  c0, c1, c1, c1, c1, c2, c2, c1, c1, c2, c3, O,  T,  T ],  # y19 hip
    [T,  O,  c0, c1, c1, c1, c2, c1, c1, c2, c1, c2, c3, O,  T,  T ],  # y20 robe
    [T,  O,  c0, c1, c1, c2, c2, c2, c2, c2, c2, c3, c3, O,  T,  T ],  # y21 robe
    [T,  T,  O,  c1, c1, c2, c2, c2, c2, c2, c2, c3, O,  T,  T,  T ],  # y22 robe lower
    [T,  T,  O,  c1, c2, c2, c3, c3, c3, c2, c3, c3, O,  T,  T,  T ],  # y23 robe hem
    [T,  T,  T,  O,  c2, c3, c3, O,  O,  c3, c3, O,  T,  T,  T,  T ],  # y24 ankles
    [T,  T,  T,  O, bt0,bt1, O,  T,  T,  O, bt0,bt1, O,  T,  T,  T ],  # y25 boots
    [T,  T,  T,  O, bt0,bt1,bt2, O,  O, bt1,bt0,bt2, O,  T,  T,  T ],  # y26 boots
    [T,  T,  T,  T,  O,  O,  O,  T,  T,  O,  O,  O,  T,  T,  T,  T ],  # y27 soles
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y28
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y29
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y30
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y31
]

# Left-facing: mirror of right-facing
def mirror_frame(frame):
    return [list(reversed(row)) for row in frame]

LEFT_STAND = mirror_frame(RIGHT_STAND)

def make_walk_frame(stand, step_side, direction):
    """Generate a walk frame from standing frame.
    Head bobs down 1px, feet shift to show stepping.
    Wider stride than default for visible animation.
    """
    import copy
    frame = copy.deepcopy(stand)

    # Find the first non-empty row (top of sprite)
    first_row = 0
    for i, row in enumerate(frame):
        if any(c != T for c in row):
            first_row = i
            break

    # Head bob: shift rows first_row..12 down by 1px
    body_start = 13
    head_rows = frame[first_row:body_start]
    for i in range(first_row, body_start):
        frame[i] = [T] * 16
    for i, row in enumerate(head_rows):
        if first_row + i + 1 < body_start + 1:
            frame[first_row + i + 1] = row

    # Leg animation: modify robe hem + feet (y23-y27) for wide stride
    if direction in ('front', 'back'):
        if step_side == 'left':
            frame[23] = [T,T,O,c1,c2,c2,c3,c3,c3,c2,c3,c3,O,T,T,T]
            frame[24] = [T,O,c2,c3,c3,T,T,T,T,T,c3,c3,c3,O,T,T]
            frame[25] = [T,O,bt0,O,T,T,T,T,T,T,T,O,bt0,O,T,T]
            frame[26] = [T,O,bt0,bt1,O,T,T,T,T,T,O,bt0,bt1,O,T,T]
            frame[27] = [T,T,O,O,T,T,T,T,T,T,T,O,O,T,T,T]
        else:
            frame[23] = [T,T,O,c1,c2,c2,c3,c3,c3,c2,c3,c3,O,T,T,T]
            frame[24] = [T,O,c2,c3,c3,c3,T,T,T,T,c3,c3,O,T,T,T]
            frame[25] = [T,T,O,bt0,O,T,T,T,T,T,O,bt0,O,T,T,T]
            frame[26] = [T,O,bt0,bt1,O,T,T,T,T,O,bt0,bt1,O,T,T,T]
            frame[27] = [T,T,O,O,T,T,T,T,T,T,O,O,T,T,T,T]
    elif direction == 'right':
        if step_side == 'left':
            frame[23] = [T,T,T,O,c2,c3,c3,c3,c3,c3,O,T,T,T,T,T]
            frame[24] = [T,T,T,O,c3,c3,c3,O,T,T,T,T,T,T,T,T]
            frame[25] = [T,T,O,bt0,O,T,T,O,bt0,O,T,T,T,T,T,T]
            frame[26] = [T,T,O,bt0,bt1,O,T,O,bt0,bt1,O,T,T,T,T,T]
            frame[27] = [T,T,T,O,O,T,T,T,O,O,T,T,T,T,T,T]
        else:
            frame[23] = [T,T,T,O,c2,c3,c3,c3,c3,c3,O,T,T,T,T,T]
            frame[24] = [T,T,T,T,T,O,c3,c3,c3,c3,O,T,T,T,T,T]
            frame[25] = [T,T,T,T,O,bt0,O,T,O,bt0,O,T,T,T,T,T]
            frame[26] = [T,T,T,O,bt0,bt1,O,T,O,bt0,bt1,O,T,T,T,T]
            frame[27] = [T,T,T,T,O,O,T,T,T,O,O,T,T,T,T,T]
    elif direction == 'left':
        if step_side == 'left':
            frame[23] = [T,T,T,T,T,O,c3,c3,c3,c3,c2,O,T,T,T,T]
            frame[24] = [T,T,T,T,T,T,O,c3,c3,c3,c3,O,T,T,T,T]
            frame[25] = [T,T,T,T,T,O,bt0,O,T,O,bt0,O,T,T,T,T]
            frame[26] = [T,T,T,T,O,bt0,bt1,O,T,O,bt0,bt1,O,T,T,T]
            frame[27] = [T,T,T,T,T,O,O,T,T,T,O,O,T,T,T,T]
        else:
            frame[23] = [T,T,T,T,T,O,c3,c3,c3,c3,c2,O,T,T,T,T]
            frame[24] = [T,T,T,T,O,c3,c3,c3,O,T,T,T,T,T,T,T]
            frame[25] = [T,T,T,O,bt0,O,T,T,O,bt0,O,T,T,T,T,T]
            frame[26] = [T,T,T,O,bt0,bt1,O,T,O,bt0,bt1,O,T,T,T,T]
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
    Su Shi: male, scholar cap, beard, blue robe, dignified expression.
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

    # --- Scholar cap (东坡巾) ---
    # Wide, flat-topped cap with slight wings
    fill_rect(18, 1, 45, 3, ht1)    # cap top
    fill_rect(16, 4, 47, 8, ht1)    # cap body
    fill_rect(18, 1, 30, 6, ht0)    # highlight left
    fill_rect(40, 4, 47, 8, ht2)    # shadow right
    # Cap wings (decorative flaps on sides)
    fill_rect(12, 5, 15, 7, ht1)    # left wing
    fill_rect(48, 5, 51, 7, ht2)    # right wing
    # Cap outline
    hline(18, 45, 0, Hh)
    for y in range(1, 4):
        p(17, y, Hh); p(46, y, Hh)
    for y in range(4, 9):
        p(15, y, Hh); p(48, y, Hh)
    # Wing outlines
    for y in range(5, 8):
        p(11, y, Hh); p(52, y, Hh)
    hline(12, 15, 4, Hh); hline(48, 51, 4, Hh)
    hline(12, 15, 8, Hh); hline(48, 51, 8, Hh)

    # --- Face (wider, male proportions) ---
    fill_rect(18, 9, 45, 32, s1)     # base face
    fill_rect(18, 9, 30, 14, s0)     # forehead highlight (top-left light)
    fill_rect(38, 9, 45, 32, s2)     # right face shadow
    fill_rect(20, 30, 43, 32, s2)    # chin shadow
    hline(22, 41, 32, s3)            # deep chin shadow

    # --- Eyes (2-row: lash line + iris, no separate brow row) ---
    # Left eye
    p(22, 17, ed); p(23, 17, ed); p(24, 17, ed); p(25, 17, ed)
    p(22, 18, eh); p(23, 18, ei); p(24, 18, ei); p(25, 18, ed)
    # Right eye
    p(37, 17, ed); p(38, 17, ed); p(39, 17, ed); p(40, 17, ed)
    p(37, 18, ed); p(38, 18, ei); p(39, 18, ei); p(40, 18, eh)

    # --- Nose ---
    p(31, 22, s2); p(32, 22, s3)
    p(31, 23, s3)

    # --- Mouth (subtle, dignified) ---
    hline(29, 34, 25, s3)

    # --- Beard ---
    fill_rect(22, 27, 41, 29, bd0)   # upper beard
    fill_rect(24, 30, 39, 32, bd1)   # lower beard
    fill_rect(26, 33, 37, 35, bd2)   # beard tip
    # Beard highlight (left side, light source)
    fill_rect(22, 27, 28, 29, bd0)
    fill_rect(35, 27, 41, 29, bd1)   # shadow side

    # --- Neck ---
    fill_rect(27, 33, 36, 37, s1)
    fill_rect(27, 33, 31, 35, s0)
    fill_rect(34, 33, 36, 37, s2)

    # --- Clothing (blue scholar robe) ---
    # Inner collar (V-neck, white)
    fill_rect(18, 38, 45, 40, ic1)
    hline(18, 28, 38, ic0)
    hline(38, 45, 38, ic2)
    # V-collar lines
    for i in range(3):
        p(29 - i, 38 + i, s2)
        p(34 + i, 38 + i, s2)

    # Robe body
    fill_rect(12, 41, 51, 58, c1)
    fill_rect(12, 41, 22, 58, c0)    # highlight left
    fill_rect(44, 41, 51, 58, c2)    # shadow right

    # Sash/belt
    fill_rect(22, 45, 41, 48, sa1)
    hline(22, 32, 45, sa0)           # highlight
    hline(34, 41, 47, sa2)           # shadow
    hline(22, 41, 48, sa2)           # bottom edge

    # Robe folds
    for y in range(50, 58):
        p(28, y, c2)
        p(36, y, c2)

    # Bottom robe
    fill_rect(12, 58, 51, 63, c2)
    fill_rect(12, 58, 22, 63, c1)
    fill_rect(44, 58, 51, 63, c3)

    # Clothing outline
    for y in range(38, 63):
        p(11, y, O)
        p(52, y, O)
    hline(11, 52, 63, O)

def generate_portrait_happy(img, ox, oy):
    """Happy expression — closed eyes (^_^), wider smile, joyful poet."""
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    # Clear default eyes
    for x in range(22, 26):
        p(x, 17, s1); p(x, 18, s1)
    for x in range(37, 41):
        p(x, 17, s1); p(x, 18, s1)
    # Happy curved eyes ^_^
    p(22, 18, M); p(23, 17, M); p(24, 17, M); p(25, 18, M)
    p(37, 18, M); p(38, 17, M); p(39, 17, M); p(40, 18, M)
    # Wider smile (replace subtle mouth)
    for x in range(28, 36):
        p(x, 25, s1)  # clear old
    for x in range(29, 35):
        p(x, 25, s3)
    p(28, 25, s3); p(35, 25, s3)
    for x in range(29, 35):
        p(x, 26, s3)


def generate_portrait_pensive(img, ox, oy):
    """Pensive/contemplative expression — slightly lowered gaze, thoughtful.
    苏轼沉思时的表情，如吟诗作赋时。
    """
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    # Half-closed eyes (lower lids raised)
    for x in range(22, 26):
        p(x, 17, s1)
    for x in range(37, 41):
        p(x, 17, s1)
    # Narrowed eyes — just the lower row
    p(22, 18, ed); p(23, 18, ei); p(24, 18, ei); p(25, 18, ed)
    p(37, 18, ed); p(38, 18, ei); p(39, 18, ei); p(40, 18, ed)
    # Slight frown line between brows (thinking)
    p(30, 16, M); p(31, 16, M); p(32, 16, M)


def generate_portrait_surprised(img, ox, oy):
    """Surprised expression — wide eyes, open mouth."""
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        img.putpixel((ox + x, oy + y), c)
    # Wider eyes (add extra highlight)
    p(22, 17, ed); p(23, 17, ed); p(24, 17, ed); p(25, 17, ed); p(26, 17, ed)
    p(22, 18, eh); p(23, 18, ei); p(24, 18, eh); p(25, 18, ei); p(26, 18, ed)
    p(36, 17, ed); p(37, 17, ed); p(38, 17, ed); p(39, 17, ed); p(40, 17, ed)
    p(36, 18, ed); p(37, 18, ei); p(38, 18, eh); p(39, 18, ei); p(40, 18, eh)
    # Open mouth (O shape)
    for x in range(29, 35):
        p(x, 25, s1)  # clear
    p(30, 25, ed); p(31, 25, ed); p(32, 25, ed); p(33, 25, ed)
    p(30, 26, ed); p(31, 26, s3); p(32, 26, s3); p(33, 26, ed)
    p(30, 27, ed); p(31, 27, ed); p(32, 27, ed); p(33, 27, ed)


def generate_portrait_sheet():
    """Generate 128x128 portrait sheet (2x2 grid of 64x64).
    Top-left: default, Top-right: happy
    Bottom-left: pensive, Bottom-right: surprised
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
    import shutil

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    char_path = os.path.join(base_dir, "assets", "Characters", "SuShi.png")
    port_path = os.path.join(base_dir, "assets", "Portraits", "SuShi.png")

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
    for qi, (qx, qy, name) in enumerate([
        (0, 0, "Default"), (64, 0, "Happy"),
        (0, 64, "Pensive"), (64, 64, "Surprised")
    ]):
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
