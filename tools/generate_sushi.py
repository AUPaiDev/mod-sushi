#!/usr/bin/env python3
"""Generate SuShi (苏轼) sprite sheet and portrait for Stardew Valley mod.

Su Shi: Northern Song dynasty literary giant, male.
- Dongpo turban (东坡巾) — flat-topped rectangular scholar cap, his most iconic feature
- Blue scholar robe (蓝色文人长袍) with white inner collar
- Short beard (1-2px hint at chin)
- Warm skin tone, medium-lean build

Stardew Valley official proportions (16x32 canvas):
  y0-3:   hat / hair top
  y4-9:   face (6px tall, ~8-10px wide) — eyes at y6-y7 are THE key feature
  y10-11: neck / collar
  y12-19: torso
  y20-24: lower body
  y25-27: boots
  y28-31: empty
"""

from PIL import Image

# === COLOR PALETTE (hue-shifted, light from top-left) ===
T = (0, 0, 0, 0)  # transparent

# Outline — deep brown, NOT pure black (Stardew convention)
OL = (38, 28, 18, 255)     # main outline
OM = (52, 38, 28, 255)     # medium / inner detail outline

# Skin — warm, male, top-left lighting
S0 = (250, 218, 190, 255)  # highlight (top-left lit)
S1 = (238, 200, 168, 255)  # base
S2 = (212, 172, 140, 255)  # shadow
S3 = (188, 145, 115, 255)  # deep shadow

# Dongpo turban — blue-black with subtle sheen
HT0 = (52, 50, 68, 255)    # highlight — faint blue sheen
HT1 = (30, 28, 42, 255)    # base — very dark
HT2 = (20, 18, 30, 255)    # shadow

# Hair (visible at sides of face under turban)
HR0 = (42, 38, 55, 255)    # highlight
HR1 = (25, 22, 35, 255)    # base
HR2 = (18, 15, 25, 255)    # shadow

# Blue scholar robe
C0 = (148, 188, 228, 255)  # highlight — sky blue
C1 = (108, 152, 202, 255)  # base — medium blue
C2 = (72, 112, 168, 255)   # shadow — deeper blue
C3 = (48, 78, 132, 255)    # deep shadow — navy

# Inner collar — cream white
IC0 = (248, 242, 232, 255) # highlight
IC1 = (232, 222, 210, 255) # base
IC2 = (208, 198, 185, 255) # shadow

# Sash / belt — dark brown-gold
SA0 = (162, 132, 82, 255)  # highlight
SA1 = (132, 105, 62, 255)  # base
SA2 = (102, 80, 45, 255)   # shadow

# Beard — dark brown, subtle
BD = (55, 42, 32, 255)     # single beard color (subtle hint)

# Eyes — maximum contrast for Stardew iconic look
EW = (255, 255, 255, 255)  # eye white — pure white
EI = (62, 42, 32, 255)     # iris — dark brown
ED = (22, 18, 15, 255)     # pupil / lash — near black

# Boots — dark leather
BT0 = (62, 52, 42, 255)    # highlight
BT1 = (42, 35, 28, 255)    # base
BT2 = (28, 22, 18, 255)    # shadow

# ── shorthand aliases (single-letter where possible) ──
O  = OL
M  = OM
s0, s1, s2, s3 = S0, S1, S2, S3
h0, h1, h2 = HT0, HT1, HT2
hr0, hr1, hr2 = HR0, HR1, HR2
c0, c1, c2, c3 = C0, C1, C2, C3
ic0, ic1, ic2 = IC0, IC1, IC2
sa0, sa1, sa2 = SA0, SA1, SA2
bd = BD
ew, ei, ed = EW, EI, ED
bt0, bt1, bt2 = BT0, BT1, BT2

# ═══════════════════════════════════════════════════════════════════
# CHARACTER SPRITE  (16 x 32 per frame, 4 frames x 4 directions)
# ═══════════════════════════════════════════════════════════════════
# Dongpo turban: flat-topped rectangle, ~10px wide, 4px tall
# Eyes at y6-y7: 2px dark lash + white/iris below — most prominent feature
# Beard: 1px hint at chin only
# Body: ~10px shoulder width, blue robe, white V-collar, dark sash

# ── Front-facing standing (south) ──
FRONT_STAND = [
    #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
    [T,  T,  T,  T,  O,  O,  O,  O,  O,  O,  O,  O,  T,  T,  T,  T ],  # y0  turban top outline (flat!)
    [T,  T,  T,  O, h0, h0, h1, h1, h1, h1, h1, h2,  O,  T,  T,  T ],  # y1  turban body
    [T,  T,  T,  O, h0, h1, h1, h1, h1, h1, h1, h2,  O,  T,  T,  T ],  # y2  turban body
    [T,  T,  O, h0, h0, h1, h1, h1, h1, h1, h1, h2, h2,  O,  T,  T ],  # y3  turban brim (wider)
    [T,  T,  T,  O,hr0, s0, s0, s1, s1, s1, s2,hr2,  O,  T,  T,  T ],  # y4  forehead + hair sides
    [T,  T,  T,  O, s0, s0, s1, s1, s1, s1, s1, s2,  O,  T,  T,  T ],  # y5  upper face
    [T,  T,  T,  O, s0, ed, ed, s1, s1, ed, ed, s2,  O,  T,  T,  T ],  # y6  ★ eye lash line (2px each)
    [T,  T,  T,  O, s0, ew, ei, s1, s1, ei, ew, s2,  O,  T,  T,  T ],  # y7  ★ eye iris + white
    [T,  T,  T,  O, s1, s1, s1, s2, s1, s1, s1, s2,  O,  T,  T,  T ],  # y8  nose (1px shadow)
    [T,  T,  T,  O, s1, s1, s2, s1, s1, s2, s1, s3,  O,  T,  T,  T ],  # y9  mouth area
    [T,  T,  T,  O, s2, s2, bd, s2, s2, bd, s2, s3,  O,  T,  T,  T ],  # y10 chin + beard hint (2px)
    [T,  T,  T,  T,  O, s2, s2, s2, s2, s2, s2,  O,  T,  T,  T,  T ],  # y11 neck
    [T,  T,  T,  O,ic0,ic1, s2, s2, s2,ic1,ic2,  O,  T,  T,  T,  T ],  # y12 collar
    [T,  T,  O, c0, c0,ic0,ic1,ic1,ic1,ic0, c1, c2,  O,  T,  T,  T ],  # y13 upper body + V collar
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c1, c2, c2,  O,  T,  T ],  # y14 chest (shoulders ~10px)
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c1, c2, c2,  O,  T,  T ],  # y15 chest
    [T,  O,  c0, c1,sa0,sa0,sa1,sa1,sa1,sa0,sa0, c2, c2,  O,  T,  T ],  # y16 sash
    [T,  O,  c0, c1,sa1,sa2,sa2,sa2,sa2,sa2,sa1, c2, c2,  O,  T,  T ],  # y17 sash lower
    [T,  O,  c0, c1, c1, c1, c1, c1, c1, c1, c1, c2, c3,  O,  T,  T ],  # y18 waist
    [T,  O,  c0, c1, c1, c1, c2, c1, c1, c2, c1, c2, c3,  O,  T,  T ],  # y19 hip fold
    [T,  O,  c0, c1, c1, c2, c1, c2, c2, c1, c2, c2, c3,  O,  T,  T ],  # y20 robe fold
    [T,  T,  O,  c1, c1, c2, c2, c2, c2, c2, c2, c3,  O,  T,  T,  T ],  # y21 robe
    [T,  T,  O,  c1, c2, c2, c2, c2, c2, c2, c2, c3,  O,  T,  T,  T ],  # y22 robe lower
    [T,  T,  T,  O,  c2, c2, c3, c3, c3, c2, c3,  O,  T,  T,  T,  T ],  # y23 robe hem
    [T,  T,  T,  O,  c3, c3,  O,  T,  T,  O,  c3, c3,  O,  T,  T,  T ],  # y24 ankles
    [T,  T,  T,  O,bt0,bt1,  O,  T,  T,  O,bt0,bt1,  O,  T,  T,  T ],  # y25 boots
    [T,  T,  T,  O,bt0,bt1,bt2,  O,  O,bt1,bt0,bt2,  O,  T,  T,  T ],  # y26 boots
    [T,  T,  T,  T,  O,  O,  O,  T,  T,  O,  O,  O,  T,  T,  T,  T ],  # y27 soles
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y28
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y29
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y30
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y31
]

# ── Right-facing standing (east) ──
# Profile: turban side, one eye visible, robe side
RIGHT_STAND = [
    #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
    [T,  T,  T,  T,  T,  O,  O,  O,  O,  O,  O,  T,  T,  T,  T,  T ],  # y0  turban top
    [T,  T,  T,  T,  O, h0, h1, h1, h1, h1, h2,  O,  T,  T,  T,  T ],  # y1  turban
    [T,  T,  T,  O, h0, h1, h1, h1, h1, h1, h1, h2,  O,  T,  T,  T ],  # y2  turban
    [T,  T,  O, h0, h1, h1, h1, h1, h1, h1, h1, h2,  O,  T,  T,  T ],  # y3  turban brim
    [T,  T,  T,  O,hr0, s0, s1, s1, s1, s1, s2,  O,  T,  T,  T,  T ],  # y4  forehead
    [T,  T,  T,  O, s0, s0, s1, s1, s1, s1, s2,  O,  T,  T,  T,  T ],  # y5  upper face
    [T,  T,  T,  O, s0, s1, s1, ed, ed, s1, s2,  O,  T,  T,  T,  T ],  # y6  eye lash (profile)
    [T,  T,  T,  O, s0, s1, s1, ew, ei, s1, s2,  O,  T,  T,  T,  T ],  # y7  eye iris (profile)
    [T,  T,  T,  O, s1, s1, s1, s1, s2, s2, s2,  O,  T,  T,  T,  T ],  # y8  nose (profile bump)
    [T,  T,  T,  O, s1, s1, s1, s1, s1, s2, s3,  O,  T,  T,  T,  T ],  # y9  mouth
    [T,  T,  T,  O, s2, s2, bd, s2, s2, s3, s3,  O,  T,  T,  T,  T ],  # y10 chin + beard
    [T,  T,  T,  T,  O, s2, s2, s2, s2, s3,  O,  T,  T,  T,  T,  T ],  # y11 neck
    [T,  T,  T,  O,ic0,ic1, s2,ic1,ic1, c1,  O,  T,  T,  T,  T,  T ],  # y12 collar
    [T,  T,  O, c0, c0, c1,ic0, c1, c1, c1, c2,  O,  T,  T,  T,  T ],  # y13 upper body
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c2, c2,  O,  T,  T,  T ],  # y14 chest
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c2, c2,  O,  T,  T,  T ],  # y15 chest
    [T,  O,  c0, c1,sa0,sa1,sa1,sa1, c1, c1, c2, c2,  O,  T,  T,  T ],  # y16 sash
    [T,  O,  c0, c1,sa1,sa2,sa2,sa2, c1, c1, c2, c2,  O,  T,  T,  T ],  # y17 sash
    [T,  O,  c0, c1, c1, c1, c1, c1, c1, c1, c2, c2,  O,  T,  T,  T ],  # y18 waist
    [T,  O,  c0, c1, c1, c1, c2, c1, c1, c2, c2, c3,  O,  T,  T,  T ],  # y19 hip
    [T,  O,  c0, c1, c1, c2, c1, c2, c2, c2, c2, c3,  O,  T,  T,  T ],  # y20 robe
    [T,  T,  O,  c1, c1, c2, c2, c2, c2, c2, c3,  O,  T,  T,  T,  T ],  # y21 robe
    [T,  T,  O,  c1, c2, c2, c2, c2, c2, c3, c3,  O,  T,  T,  T,  T ],  # y22 robe lower
    [T,  T,  T,  O,  c2, c3, c3, c3, c3, c3,  O,  T,  T,  T,  T,  T ],  # y23 robe hem
    [T,  T,  T,  T,  O,  c3, c3,  O,  O, c3,  O,  T,  T,  T,  T,  T ],  # y24 ankles
    [T,  T,  T,  T,  O,bt0,  O,  T,  T,  O,bt0,  O,  T,  T,  T,  T ],  # y25 boots
    [T,  T,  T,  T,  O,bt0,bt1,  O,  O,bt0,bt1,  O,  T,  T,  T,  T ],  # y26 boots
    [T,  T,  T,  T,  T,  O,  O,  T,  T,  O,  O,  T,  T,  T,  T,  T ],  # y27 soles
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y28
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y29
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y30
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y31
]

# ── Back-facing standing (north) ──
# Turban from behind, robe back, no face
BACK_STAND = [
    #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
    [T,  T,  T,  T,  O,  O,  O,  O,  O,  O,  O,  O,  T,  T,  T,  T ],  # y0  turban top
    [T,  T,  T,  O, h0, h0, h1, h1, h1, h1, h1, h2,  O,  T,  T,  T ],  # y1  turban
    [T,  T,  T,  O, h0, h1, h1, h1, h1, h1, h1, h2,  O,  T,  T,  T ],  # y2  turban
    [T,  T,  O, h0, h0, h1, h1, h1, h1, h1, h1, h2, h2,  O,  T,  T ],  # y3  turban brim
    [T,  T,  T,  O,hr0,hr1,hr1,hr1,hr1,hr1,hr1,hr2,  O,  T,  T,  T ],  # y4  back of head (hair)
    [T,  T,  T,  O,hr0,hr1,hr1,hr1,hr1,hr1,hr1,hr2,  O,  T,  T,  T ],  # y5  back of head
    [T,  T,  T,  O,hr0,hr1,hr1,hr1,hr1,hr1,hr1,hr2,  O,  T,  T,  T ],  # y6  back of head
    [T,  T,  T,  O,hr0,hr1,hr1,hr1,hr1,hr1,hr1,hr2,  O,  T,  T,  T ],  # y7  back of head
    [T,  T,  T,  O,hr0,hr1,hr1,hr1,hr1,hr1,hr1,hr2,  O,  T,  T,  T ],  # y8  back of head
    [T,  T,  T,  O, s0, s1, s1, s1, s1, s1, s1, s2,  O,  T,  T,  T ],  # y9  neck back
    [T,  T,  T,  O, s1, s1, s1, s1, s1, s1, s1, s2,  O,  T,  T,  T ],  # y10 neck
    [T,  T,  T,  T,  O, s2, s2, s2, s2, s2, s2,  O,  T,  T,  T,  T ],  # y11 neck base
    [T,  T,  T,  O,ic0,ic1, s2, s2, s2,ic1,ic2,  O,  T,  T,  T,  T ],  # y12 collar back
    [T,  T,  O, c0, c0, c1, c1, c1, c1, c1, c1, c2,  O,  T,  T,  T ],  # y13 upper back
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c1, c2, c2,  O,  T,  T ],  # y14 back
    [T,  O,  c0, c0, c1, c1, c1, c1, c1, c1, c1, c2, c2,  O,  T,  T ],  # y15 back
    [T,  O,  c0, c1,sa0,sa0,sa1,sa1,sa1,sa0,sa0, c2, c2,  O,  T,  T ],  # y16 sash
    [T,  O,  c0, c1,sa1,sa2,sa2,sa2,sa2,sa2,sa1, c2, c2,  O,  T,  T ],  # y17 sash
    [T,  O,  c0, c1, c1, c1, c1, c1, c1, c1, c1, c2, c3,  O,  T,  T ],  # y18 waist
    [T,  O,  c0, c1, c1, c1, c2, c1, c1, c2, c1, c2, c3,  O,  T,  T ],  # y19 hip
    [T,  O,  c0, c1, c1, c2, c1, c2, c2, c1, c2, c2, c3,  O,  T,  T ],  # y20 robe
    [T,  T,  O,  c1, c1, c2, c2, c2, c2, c2, c2, c3,  O,  T,  T,  T ],  # y21 robe
    [T,  T,  O,  c1, c2, c2, c2, c2, c2, c2, c2, c3,  O,  T,  T,  T ],  # y22 robe lower
    [T,  T,  T,  O,  c2, c2, c3, c3, c3, c2, c3,  O,  T,  T,  T,  T ],  # y23 robe hem
    [T,  T,  T,  O,  c3, c3,  O,  T,  T,  O,  c3, c3,  O,  T,  T,  T ],  # y24 ankles
    [T,  T,  T,  O,bt0,bt1,  O,  T,  T,  O,bt0,bt1,  O,  T,  T,  T ],  # y25 boots
    [T,  T,  T,  O,bt0,bt1,bt2,  O,  O,bt1,bt0,bt2,  O,  T,  T,  T ],  # y26 boots
    [T,  T,  T,  T,  O,  O,  O,  T,  T,  O,  O,  O,  T,  T,  T,  T ],  # y27 soles
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y28
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y29
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y30
    [T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T,  T ],  # y31
]

# ── Left-facing = mirror of right ──
def mirror_frame(frame):
    return [list(reversed(row)) for row in frame]

LEFT_STAND = mirror_frame(RIGHT_STAND)

# ═══════════════════════════════════════════════════════════════════
# WALK ANIMATION
# ═══════════════════════════════════════════════════════════════════
# Walk frames: head bobs down 1px, feet split apart for stride.

def make_walk_frame(stand, step_side, direction):
    """Generate a walk frame from standing frame.
    Head bobs down 1px, feet shift to show stepping.
    """
    import copy
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
        if target < body_start + 1:
            frame[target] = row

    # Leg animation: modify robe hem + feet (y23-y27)
    if direction in ('front', 'back'):
        if step_side == 'left':
            frame[23] = [T,T,T,O,c2,c2,c3,c3,c3,c2,c3,O,T,T,T,T]
            frame[24] = [T,T,O,c3,c3,T,T,T,T,T,c3,c3,O,T,T,T]
            frame[25] = [T,T,O,bt0,O,T,T,T,T,T,O,bt0,O,T,T,T]
            frame[26] = [T,O,bt0,bt1,O,T,T,T,T,T,O,bt0,bt1,O,T,T]
            frame[27] = [T,T,O,O,T,T,T,T,T,T,T,O,O,T,T,T]
        else:
            frame[23] = [T,T,T,O,c2,c2,c3,c3,c3,c2,c3,O,T,T,T,T]
            frame[24] = [T,T,O,c3,c3,c3,T,T,T,T,c3,c3,O,T,T,T]
            frame[25] = [T,T,T,O,bt0,O,T,T,T,O,bt0,O,T,T,T,T]
            frame[26] = [T,T,O,bt0,bt1,O,T,T,O,bt0,bt1,O,T,T,T,T]
            frame[27] = [T,T,T,O,O,T,T,T,T,O,O,T,T,T,T,T]
    elif direction == 'right':
        if step_side == 'left':
            frame[23] = [T,T,T,O,c2,c3,c3,c3,c3,c3,O,T,T,T,T,T]
            frame[24] = [T,T,T,O,c3,c3,O,T,T,T,T,T,T,T,T,T]
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
            frame[24] = [T,T,T,T,O,c3,c3,O,T,T,T,T,T,T,T,T]
            frame[25] = [T,T,T,O,bt0,O,T,T,O,bt0,O,T,T,T,T,T]
            frame[26] = [T,T,T,O,bt0,bt1,O,T,O,bt0,bt1,O,T,T,T,T]
            frame[27] = [T,T,T,T,O,O,T,T,T,O,O,T,T,T,T,T]

    return frame


# ═══════════════════════════════════════════════════════════════════
# SPRITE SHEET ASSEMBLY
# ═══════════════════════════════════════════════════════════════════

def paint_frame(img, frame_data, offset_x, offset_y):
    """Paint a 16x32 frame onto the image."""
    for y, row in enumerate(frame_data):
        for x, color in enumerate(row):
            if color != T:
                img.putpixel((offset_x + x, offset_y + y), color)


def generate_character_sheet():
    """Generate the 64x128 character sprite sheet (4 directions x 4 frames)."""
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

# ═══════════════════════════════════════════════════════════════════
# PORTRAIT  (128x128 sheet = 2x2 grid of 64x64 portraits)
# ═══════════════════════════════════════════════════════════════════
# At 64x64 we can render much more detail: wider eyes with 3px whites,
# detailed turban, visible beard texture, robe folds.

def generate_portrait_default(img, ox, oy):
    """Default expression — dignified, calm scholar."""
    def p(x, y, c):
        if 0 <= x < 64 and 0 <= y < 64:
            img.putpixel((ox + x, oy + y), c)

    def hline(x1, x2, y, c):
        for x in range(x1, x2 + 1):
            p(x, y, c)

    def fill_rect(x1, y1, x2, y2, c):
        for yy in range(y1, y2 + 1):
            hline(x1, x2, yy, c)

    # --- Dongpo turban (东坡巾) ---
    # Flat-topped rectangular cap, the most iconic feature
    # Main body: wide rectangle
    fill_rect(17, 1, 46, 3, h1)     # cap top
    fill_rect(15, 4, 48, 8, h1)     # cap body
    # Lighting: highlight left, shadow right
    fill_rect(17, 1, 30, 3, h0)     # top highlight
    fill_rect(15, 4, 28, 8, h0)     # body highlight
    fill_rect(40, 4, 48, 8, h2)     # body shadow
    # Flat top outline
    hline(17, 46, 0, O)             # top edge (flat!)
    for y in range(1, 4):
        p(16, y, O); p(47, y, O)
    for y in range(4, 9):
        p(14, y, O); p(49, y, O)
    hline(14, 16, 4, O)             # brim left
    hline(47, 49, 4, O)             # brim right
    hline(14, 49, 9, O)             # bottom edge of turban

    # --- Face ---
    fill_rect(17, 10, 46, 33, s1)   # base face
    fill_rect(17, 10, 30, 16, s0)   # forehead highlight (top-left)
    fill_rect(38, 10, 46, 33, s2)   # right face shadow
    fill_rect(20, 31, 43, 33, s2)   # chin shadow
    # Face outline
    for y in range(10, 34):
        p(16, y, O); p(47, y, O)

    # --- Eyes (THE key feature — large, prominent, Stardew iconic) ---
    # Left eye: 4px wide (1 dark border + 2 white + 1 iris)
    p(22, 18, ed); p(23, 18, ed); p(24, 18, ed); p(25, 18, ed)  # lash line
    p(22, 19, ed); p(23, 19, ew); p(24, 19, ew); p(25, 19, ei)  # white + iris
    p(22, 20, ed); p(23, 20, ew); p(24, 20, ei); p(25, 20, ed)  # white + iris lower
    # Right eye: 4px wide (mirror)
    p(37, 18, ed); p(38, 18, ed); p(39, 18, ed); p(40, 18, ed)  # lash line
    p(37, 19, ei); p(38, 19, ew); p(39, 19, ew); p(40, 19, ed)  # iris + white
    p(37, 20, ed); p(38, 20, ei); p(39, 20, ew); p(40, 20, ed)  # iris + white lower

    # --- Nose ---
    p(31, 23, s2); p(32, 23, s3)
    p(31, 24, s3)

    # --- Mouth (subtle, dignified) ---
    hline(29, 34, 27, s3)

    # --- Beard (subtle, 2-row hint) ---
    hline(24, 39, 30, bd)           # upper beard line
    hline(26, 37, 31, bd)           # lower beard line
    hline(28, 35, 32, bd)           # beard tip

    # --- Neck ---
    fill_rect(27, 34, 36, 38, s1)
    fill_rect(27, 34, 31, 36, s0)   # highlight
    fill_rect(34, 34, 36, 38, s2)   # shadow

    # --- Clothing (blue scholar robe) ---
    # Inner collar (V-neck, white/cream)
    fill_rect(17, 39, 46, 41, ic1)
    hline(17, 28, 39, ic0)          # highlight
    hline(38, 46, 39, ic2)          # shadow
    # V-collar lines
    for i in range(3):
        p(30 - i, 39 + i, s2)
        p(33 + i, 39 + i, s2)

    # Robe body
    fill_rect(11, 42, 52, 58, c1)
    fill_rect(11, 42, 22, 58, c0)   # highlight left
    fill_rect(44, 42, 52, 58, c2)   # shadow right

    # Sash / belt
    fill_rect(22, 46, 41, 49, sa1)
    hline(22, 32, 46, sa0)          # highlight
    hline(34, 41, 48, sa2)          # shadow
    hline(22, 41, 49, sa2)          # bottom edge

    # Robe folds
    for y in range(51, 58):
        p(28, y, c2)
        p(36, y, c2)

    # Bottom robe
    fill_rect(11, 58, 52, 63, c2)
    fill_rect(11, 58, 22, 63, c1)
    fill_rect(44, 58, 52, 63, c3)

    # Clothing outline
    for y in range(39, 63):
        p(10, y, O)
        p(53, y, O)
    hline(10, 53, 63, O)


def generate_portrait_happy(img, ox, oy):
    """Happy expression — closed eyes (^_^), wider smile."""
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        if 0 <= x < 64 and 0 <= y < 64:
            img.putpixel((ox + x, oy + y), c)

    # Clear default eyes
    for x in range(22, 26):
        for y in range(18, 21):
            p(x, y, s1)
    for x in range(37, 41):
        for y in range(18, 21):
            p(x, y, s1)

    # Happy curved eyes ^_^
    p(22, 20, M); p(23, 19, M); p(24, 19, M); p(25, 20, M)
    p(37, 20, M); p(38, 19, M); p(39, 19, M); p(40, 20, M)

    # Wider smile
    for x in range(28, 36):
        p(x, 27, s3)
    for x in range(29, 35):
        p(x, 28, s3)


def generate_portrait_pensive(img, ox, oy):
    """Pensive/contemplative — half-closed eyes, thoughtful frown.
    苏轼沉思吟诗时的表情。
    """
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        if 0 <= x < 64 and 0 <= y < 64:
            img.putpixel((ox + x, oy + y), c)

    # Clear top row of eyes (half-closed)
    for x in range(22, 26):
        p(x, 18, s1)
    for x in range(37, 41):
        p(x, 18, s1)

    # Narrowed eyes — only bottom two rows remain, slightly squinted
    p(22, 19, ed); p(23, 19, ew); p(24, 19, ei); p(25, 19, ed)
    p(37, 19, ed); p(38, 19, ei); p(39, 19, ew); p(40, 19, ed)
    p(22, 20, s2); p(23, 20, ed); p(24, 20, ed); p(25, 20, s2)
    p(37, 20, s2); p(38, 20, ed); p(39, 20, ed); p(40, 20, s2)

    # Thinking frown between brows
    p(30, 17, M); p(31, 17, M); p(32, 17, M)


def generate_portrait_surprised(img, ox, oy):
    """Surprised expression — wide eyes, open mouth."""
    generate_portrait_default(img, ox, oy)
    def p(x, y, c):
        if 0 <= x < 64 and 0 <= y < 64:
            img.putpixel((ox + x, oy + y), c)

    # Wider eyes (add extra row above for raised brows)
    # Left eye — 5px wide
    p(21, 17, ed); p(22, 17, ed); p(23, 17, ed); p(24, 17, ed); p(25, 17, ed); p(26, 17, ed)
    p(21, 18, ed); p(22, 18, ed); p(23, 18, ed); p(24, 18, ed); p(25, 18, ed); p(26, 18, ed)
    p(21, 19, ed); p(22, 19, ew); p(23, 19, ew); p(24, 19, ew); p(25, 19, ei); p(26, 19, ed)
    p(21, 20, ed); p(22, 20, ew); p(23, 20, ew); p(24, 20, ei); p(25, 20, ed); p(26, 20, ed)
    # Right eye — 5px wide
    p(36, 17, ed); p(37, 17, ed); p(38, 17, ed); p(39, 17, ed); p(40, 17, ed); p(41, 17, ed)
    p(36, 18, ed); p(37, 18, ed); p(38, 18, ed); p(39, 18, ed); p(40, 18, ed); p(41, 18, ed)
    p(36, 19, ed); p(37, 19, ei); p(38, 19, ew); p(39, 19, ew); p(40, 19, ew); p(41, 19, ed)
    p(36, 20, ed); p(37, 20, ed); p(38, 20, ei); p(39, 20, ew); p(40, 20, ew); p(41, 20, ed)

    # Open mouth (O shape)
    for x in range(29, 35):
        p(x, 27, s1)  # clear default mouth
    p(30, 27, ed); p(31, 27, ed); p(32, 27, ed); p(33, 27, ed)
    p(30, 28, ed); p(31, 28, s3); p(32, 28, s3); p(33, 28, ed)
    p(30, 29, ed); p(31, 29, ed); p(32, 29, ed); p(33, 29, ed)


def generate_portrait_sheet():
    """Generate 128x128 portrait sheet (2x2 grid of 64x64).
    Top-left: default    Top-right: happy
    Bottom-left: pensive Bottom-right: surprised
    """
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

    generate_portrait_default(img, 0, 0)
    generate_portrait_happy(img, 64, 0)
    generate_portrait_pensive(img, 0, 64)
    generate_portrait_surprised(img, 64, 64)

    return img

# ═══════════════════════════════════════════════════════════════════
# MAIN — generate, save, verify
# ═══════════════════════════════════════════════════════════════════
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
