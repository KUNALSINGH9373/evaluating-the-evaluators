#!/usr/bin/env python3
"""One palette for every figure. Import from here; never hard-code a colour in a chart script.

Specified by the author 2026-08-18 for tier, severity, action level and proportionality. The
remaining dimensions are derived below on the same semantic logic, so a colour means the same
thing wherever it appears:

    red   #D95D4F   nothing happened / the weakest outcome
    amber #F0B323   partial, interim, incomplete
    orange#E59A34   recognised but no action
    green #2FA36B   full, proportionate, strongest outcome
    blue  #4FA7DC   descriptive, no valence
    grey  #D9D9D9   not assessed / not applicable
"""

# ---- the four specified scales --------------------------------------------------------
RED    = "#D95D4F"   # significant risk · none · accountability gap
AMBER  = "#F0B323"   # partial · under-response
ORANGE = "#E59A34"   # acknowledged
GREEN  = "#2FA36B"   # substantive · proportionate
BLUE   = "#4FA7DC"   # low risk · neutral descriptive
GREY   = "#D9D9D9"   # not assessed / not applicable

# Finding category (tier). Pale fills as specified; INK gives each a readable border and
# label colour, because a pale fill alone is illegible as a bar at poster distance.
TIER_FILL = {"A": "#FCE4E4", "B": "#FFF6DC", "C": "#EAF2FC"}
TIER_INK  = {"A": "#C0453A", "B": "#B4841A", "C": "#3D7FA6"}
TIER_LABEL = {"A": "Accountability-relevant finding",
              "B": "Concerning finding, no accountable party",
              "C": "Not an empirical model finding"}

# Risk classification
SEV = {"C1": RED, "C2": BLUE, "": GREY}
SEV_LABEL = {"C1": "Significant risk", "C2": "Low risk", "": "Not assessed"}

# Company response
ACTION = {"None": RED, "Acknowledged": ORANGE, "Partial": AMBER, "Substantive": GREEN, "": GREY}

# Proportionality
PROP = {"Accountability gap (no action)": RED, "Under-response (gap)": AMBER,
        "Proportionate": GREEN, "": GREY}

# ---- derived, on the same logic -------------------------------------------------------
# Policy uptake: same escalation as company response — nothing / partial / full.
POLICY = {"No policy uptake identified": RED,
          "Non-binding policy-related uptake": AMBER,
          "Binding policy action": GREEN, "": GREY}

# Attribution: credited / acted silently / nothing to attribute. The last is genuinely
# "not assessed" — attribution is only scored where a response exists — so it takes grey.
ATTRIB = {"Explicit attribution": GREEN, "No explicit attribution": AMBER,
          "No response located": GREY, "": GREY}

# Evaluator scope: descriptive, no valence. Two tints of the neutral blue.
SCOPE = {"government-AISI": "#2E7CA8", "third-party-evaluator": BLUE, "": GREY}

# Access type: descriptive ordinal, palest to deepest, with grey for the non-answers.
ACCESS = {"Pre-deployment": "#9BCBEA", "Post-deployment": "#4FA7DC", "Mixed": "#2E7CA8",
          "Aggregate": "#1F5A7A", "N/A": GREY, "": GREY}

# Institution type, for the tree. Four sibling categories with no valence, so they need to be
# BRIGHT and clearly separable — four tints of one blue are unreadable side by side. All four are
# cool hues deliberately kept off red / amber / green, which are reserved for outcome semantics:
# an institution type must never look like a proportionality verdict.
INSTTYPE = {"Government": "#1565C0",             # blue
            "Non-Profit (AIEF)": "#00A0A8",      # teal
            "For-Profit": "#7A4FC0",             # violet
            "Non-Profit (Independent)": "#C2478E"}  # magenta


# Institution short forms. Full names wrap onto two lines in ranked lists and collide with the
# row above; the full name stays in the workbook and the published dataset.
SHORT_INST = {"Princeton Holistic Agent Leaderboard (HAL)": "Princeton HAL",
              "Collective Intelligence Project (Weval)": "Weval (CIP)",
              "Shanghai AI Laboratory (AI45 Lab)": "Shanghai AI Lab",
              "Cisco (Robust Intelligence / Foundation AI)": "Cisco",
              "Center for AI Safety (CAIS)": "CAIS",
              "Joint UK + US + Singapore AISIs (International Network)": "Joint UK + US + SG AISIs",
              "Joint UK AISI + OpenAI (company-published)": "Joint UK AISI + OpenAI"}


def short_inst(name):
    return SHORT_INST.get(name, name)


def tint(hex_colour, white=0.84):
    """Blend a colour toward white. Used to give a child node its parent's hue at low weight."""
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    f = lambda v: int(round(v + (255 - v) * white))
    return f"#{f(r):02X}{f(g):02X}{f(b):02X}"


def shade(hex_colour, black=0.30):
    """Darken a colour. Used for text that must stay legible on its own tint."""
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    f = lambda v: int(round(v * (1 - black)))
    return f"#{f(r):02X}{f(g):02X}{f(b):02X}"

# Neutral categorical ramp for dimensions with no valence (domains, years, institutions).
# Blue-led so it never competes with the red/amber/green outcome semantics.
NEUTRAL = ["#2E7CA8", "#4FA7DC", "#9BCBEA", "#1F5A7A", "#7FB9DD", "#155066",
           "#A9D3EC", "#3D8FBF", "#CBE4F4", "#0F3F52"]

# Sequential ramp for heatmaps: magnitude only, never valence.
SEQ = "Blues"

# Ink and furniture
INK, INK_2, MUTED, GRID, WIRE = "#111111", "#333333", "#666666", "#EEEEEE", "#9AA7B2"


def ramp(n):
    """n distinguishable neutral colours, cycling the ramp if needed."""
    return [NEUTRAL[i % len(NEUTRAL)] for i in range(n)]


def colours_for(d, keys):
    """Colours for keys in a fixed order, falling back to grey for anything unmapped."""
    return [d.get(k, GREY) for k in keys]


# ---- legacy palette, so the pre-2026-08-18 figure set can still be reproduced ----------
# Set AISIEVAL_PALETTE=legacy to rebuild the original colours from the same code.
import os as _os
if _os.environ.get("AISIEVAL_PALETTE") == "legacy":
    RED, AMBER, ORANGE, GREEN = "#E03131", "#E8A80C", "#D2570A", "#00A36C"
    BLUE, GREY = "#0A6EBD", "#B0B7BF"
    TIER_INK = {"A": "#E8453C", "B": "#F5A623", "C": "#2D9CDB"}
    SEV = {"C1": ORANGE, "C2": "#4FADEE", "": GREY}
    ACTION = {"None": ORANGE, "Acknowledged": AMBER, "Partial": "#7CB518",
              "Substantive": GREEN, "": GREY}
    PROP = {"Accountability gap (no action)": ORANGE, "Under-response (gap)": AMBER,
            "Proportionate": GREEN, "": GREY}
    POLICY = {"No policy uptake identified": GREY, "Non-binding policy-related uptake": "#4FADEE",
              "Binding policy action": BLUE, "": GREY}
    ATTRIB = {"Explicit attribution": GREEN, "No explicit attribution": AMBER,
              "No response located": GREY, "": GREY}
    SCOPE = {"government-AISI": BLUE, "third-party-evaluator": "#4FADEE", "": GREY}
    ACCESS = {"Pre-deployment": BLUE, "Post-deployment": "#4FADEE", "Mixed": "#7B4FBF",
              "Aggregate": "#00A6A6", "N/A": GREY, "": GREY}
    INSTTYPE = {"Government": "#1F6FB2", "Non-Profit (AIEF)": "#1E9E63",
                "Non-Profit (Independent)": "#5B9BD5", "For-Profit": "#E8A80C"}
    NEUTRAL = [BLUE, ORANGE, "#00A6A6", "#7B4FBF", GREEN, "#D4267D", AMBER, "#4FADEE", "#7CB518", RED]

# Output directory, so both palettes can be built without overwriting each other.
CHARTS_OUT = _os.environ.get(
    "AISIEVAL_CHARTS_OUT",
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "charts"))
