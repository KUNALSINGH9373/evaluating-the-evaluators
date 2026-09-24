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
# `Aggregate` was retired 2026-08-31 — it described the report's format, not model access.
ACCESS = {"Pre-deployment": "#9BCBEA", "Post-deployment": "#4FA7DC", "Mixed": "#2E7CA8",
          "N/A": GREY, "": GREY}

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
              "Joint UK AISI + OpenAI (company-published)": "Joint UK AISI + OpenAI",
              # 44 characters, and the longest label on the institution tree by a wide margin:
              # it alone forced the figure ~4in wider than every other bar needed.
              "International Network of AI Safety Institutes": "International Network of AISIs",
              "US Center for AI Standards and Innovation (US CAISI)": "US CAISI",
              "UK AI Safety Institute (UK AISI)": "UK AISI",
              "AI Verification and Evaluation Research Institute (AVERI)": "AVERI",
              "UL Research Institutes (DSRI)": "UL DSRI",
              "Singapore AI Safety Institute (SGAISI) / IMDA": "Singapore AISI / IMDA"}


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


def on_colour(bg, light="#FFFFFF", dark=None):
    """Readable text colour for a given fill, by relative luminance.

    The figure set hard-coded white for every label sitting inside a coloured shape, which held
    while the fills were saturated. The MATS blue family runs from #1B3A4F to #D6EEFF, so white
    on the pale end is close to invisible; the label has to follow the fill."""
    def _L(hexc):
        h = hexc.lstrip("#")
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    dark = dark or "#14202A"
    if not AUTO_CONTRAST:
        # The default figure set was reviewed and signed off with white labels throughout. The
        # rule only switches on where it is needed — the MATS blues run pale enough that white
        # on blue-400 drops to 2.5:1 — so this never restyles the approved set behind its back.
        return light
    Lb = _L(bg)
    ratio = lambda c: ((max(Lb, _L(c)) + 0.05) / (min(Lb, _L(c)) + 0.05))
    # Pick by measured contrast, not by a luminance threshold. A midtone like MATS blue-400
    # (#7AAACC) sits below any sensible threshold yet gives white only 2.5:1, against 6.6:1 for
    # the dark ink — a threshold picks the unreadable one and a comparison cannot.
    return light if ratio(light) >= ratio(dark) else dark


def primary_domain(value):
    """The canonical domain a Domain entry belongs to.

    The workbook's Domain field carries free-text qualifiers after an em-dash or in brackets —
    one entry runs to 176 characters. Plotting the raw strings gave the domain chart 25
    categories, most of them a single finding, with labels wider than the bars. Folding on the
    first separator is the same mechanical rule the institution tree uses for compound
    Institution Type values: take the head, keep the detail in the workbook."""
    import re as _re
    return _re.split(r"\s+[\u2014\u2013-]\s+|\s*\(", value)[0].strip()


def domain_counts(rows, field="Domain"):
    """Folded domain counts, counting each domain at most once per finding."""
    import collections as _c
    out = _c.Counter()
    for r in rows:
        seen = set()
        for part in (x.strip() for x in r.get(field, "").split(";")):
            if not part:
                continue
            k = primary_domain(part)
            if k and k not in seen:
                out[k] += 1
                seen.add(k)
    return out


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
              "N/A": GREY, "": GREY}
    INSTTYPE = {"Government": "#1F6FB2", "Non-Profit (AIEF)": "#1E9E63",
                "Non-Profit (Independent)": "#5B9BD5", "For-Profit": "#E8A80C"}
    NEUTRAL = [BLUE, ORANGE, "#00A6A6", "#7B4FBF", GREEN, "#D4267D", AMBER, "#4FADEE", "#7CB518", RED]

# Labels drawn inside a coloured shape pick their own colour by measured contrast. On by
# default for the MATS palette, whose pale blues break white text; off elsewhere, so the
# reviewed figure set keeps the appearance it was signed off with.
AUTO_CONTRAST = _os.environ.get(
    "AISIEVAL_AUTO_CONTRAST",
    "on" if _os.environ.get("AISIEVAL_PALETTE") == "mats" else "off").lower() != "off"

# Output directory, so both palettes can be built without overwriting each other.
CHARTS_OUT = _os.environ.get(
    "AISIEVAL_CHARTS_OUT",
    _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "charts"))


# ---- MATS palette, for the ICLR figure set --------------------------------------------
# AISIEVAL_PALETTE=mats rebuilds every figure in the MATS design tokens. The greys, blues,
# green-300 and reds below are read verbatim from the CSS custom properties published at
# matsprogram.org (--50..--900, --blue-50..--blue-800, --green-300, --red-50..--red-700).
# MATS publishes no amber or orange, and the outcome scale needs three steps between red and
# green, so AMBER and ORANGE are DERIVED here at the same desaturation as the rest of the set.
# So are the four institution-type hues: MATS ships one green and one blue family, which
# cannot carry four sibling categories that must also stay clear of the outcome semantics.
if _os.environ.get("AISIEVAL_PALETTE") == "mats":
    M = {  # verbatim MATS tokens
        "50": "#F8F9FA", "100": "#F2F4F5", "200": "#EEEFF0", "300": "#D9DBDD",
        "400": "#AAAFB3", "500": "#8D9194", "600": "#626669", "700": "#484B4C",
        "800": "#323638", "900": "#1E2021",
        "blue50": "#EDF6FC", "blue100": "#EBF6FF", "blue200": "#D6EEFF",
        "blue400": "#7AAACC", "blue600": "#366180", "blue800": "#1B3A4F",
        "green300": "#55B5A1",
        "red50": "#F7EDF0", "red500": "#B01928", "red600": "#801323", "red700": "#630C19",
    }
    RED    = M["red500"]
    AMBER  = "#B5821F"          # derived
    ORANGE = "#CE9A4A"          # derived
    GREEN  = "#2E8676"          # green-300 darkened for contrast against white at bar size
    BLUE   = M["blue600"]
    GREY   = M["300"]

    TIER_FILL = {"A": M["red50"], "B": "#FAF4E8", "C": M["blue50"]}
    TIER_INK  = {"A": M["red600"], "B": AMBER, "C": M["blue800"]}
    SEV    = {"C1": RED, "C2": BLUE, "": GREY}
    ACTION = {"None": RED, "Acknowledged": ORANGE, "Partial": AMBER,
              "Substantive": GREEN, "": GREY}
    PROP   = {"Accountability gap (no action)": RED, "Under-response (gap)": AMBER,
              "Proportionate": GREEN, "": GREY}
    POLICY = {"No policy uptake identified": RED,
              "Non-binding policy-related uptake": AMBER,
              "Binding policy action": GREEN, "": GREY}
    ATTRIB = {"Explicit attribution": GREEN, "No explicit attribution": AMBER,
              "No response located": GREY, "": GREY}
    SCOPE  = {"government-AISI": M["blue800"], "third-party-evaluator": M["blue400"], "": GREY}
    ACCESS = {"Pre-deployment": M["blue200"], "Post-deployment": M["blue400"],
              "Mixed": M["blue600"], "N/A": GREY, "": GREY}
    INSTTYPE = {"Government": M["blue800"], "Non-Profit (AIEF)": "#3E8C9E",
                "Non-Profit (Independent)": "#8C5A7A", "For-Profit": M["blue400"]}
    NEUTRAL = [M["blue800"], M["blue600"], M["blue400"], "#3E8C9E", M["700"],
               M["400"], M["blue200"], "#8C5A7A", M["500"], M["blue100"]]
    INK, INK_2, MUTED = M["900"], M["800"], M["600"]
    GRID, WIRE = M["200"], M["400"]
    SEQ = "mats_blues"


# ---- output profile: format, in-figure notes, type size -------------------------------
# The ICLR set needs vector output with live text, no in-figure captions (they belong in the
# LaTeX \caption), and larger type. All three are env-driven so one code path builds both sets.
FMT = _os.environ.get("AISIEVAL_CHART_FORMAT", "png").lower()
NOTES = _os.environ.get("AISIEVAL_CHART_NOTES", "on").lower() != "off"
# A conference figure carries its title in the LaTeX \\caption, not baked into the artwork, where
# it cannot be restyled, cannot be searched as part of the caption, and prints twice on the page.
TITLES = _os.environ.get("AISIEVAL_CHART_TITLES", "on").lower() != "off"
FONT_SCALE = float(_os.environ.get("AISIEVAL_CHART_FONTSCALE", "1.0"))
_PAD_ENV = _os.environ.get("AISIEVAL_CHART_PAD")


def pad(default):
    """savefig pad_inches: the script's own value unless the profile overrides it.

    A single global default here silently re-cropped every figure in the reviewed set, because
    each script had picked its own margin. The override only applies when it is asked for."""
    return float(_PAD_ENV) if _PAD_ENV is not None else default


def out_path(name):
    """Absolute path for a figure, with the extension the active profile asks for."""
    stem = name.rsplit(".", 1)[0]
    return _os.path.join(CHARTS_OUT, f"{stem}.{FMT}")


def _install_profile():
    """Apply the profile to matplotlib itself, so no chart script has to know about it.

    Font scaling cannot go through rcParams: almost every size in this figure set is an
    explicit `fontsize=` argument, which rcParams never sees. The text-drawing entry points
    are wrapped instead — one place, active only when a scale is actually set."""
    import matplotlib
    if FMT in ("pdf", "eps", "ps", "svg"):
        # Type 42 embeds the TrueType outlines and keeps the text as text, so a reader can
        # search and select it inside the compiled PDF. Type 3, the default, often cannot be
        # extracted reliably. svg gets the same treatment via 'none' (no path conversion).
        matplotlib.rcParams["pdf.fonttype"] = 42
        matplotlib.rcParams["ps.fonttype"] = 42
        matplotlib.rcParams["svg.fonttype"] = "none"
    import matplotlib.axes, matplotlib.figure, matplotlib.text
    if not TITLES:
        _st = matplotlib.axes.Axes.set_title
        if not getattr(_st, "_aisieval_notitle", False):
            def set_title(self, label, *a, **kw):
                return _st(self, "", *a, **kw)
            set_title._aisieval_notitle = True
            matplotlib.axes.Axes.set_title = set_title
    if FONT_SCALE == 1.0:
        return
    for k in ("font.size", "axes.titlesize", "axes.labelsize",
              "xtick.labelsize", "ytick.labelsize", "legend.fontsize"):
        v = matplotlib.rcParams.get(k)
        if isinstance(v, (int, float)):
            matplotlib.rcParams[k] = v * FONT_SCALE

    def _scaled(fn):
        def wrapper(*a, **kw):
            fs = kw.get("fontsize", kw.get("size"))
            if isinstance(fs, (int, float)):
                kw.pop("size", None)
                kw["fontsize"] = fs * FONT_SCALE
            return fn(*a, **kw)
        return wrapper

    for cls, names in ((matplotlib.axes.Axes,
                        ("text", "annotate", "set_title", "set_xlabel", "set_ylabel",
                         "set_xticklabels", "set_yticklabels", "legend")),
                       (matplotlib.figure.Figure, ("text", "suptitle", "legend"))):
        for n in names:
            fn = getattr(cls, n, None)
            if fn is not None and not getattr(fn, "_aisieval_scaled", False):
                w = _scaled(fn)
                w._aisieval_scaled = True
                setattr(cls, n, w)

    _tp = matplotlib.axes.Axes.tick_params
    if not getattr(_tp, "_aisieval_scaled", False):
        def tick_params(self, *a, **kw):
            if isinstance(kw.get("labelsize"), (int, float)):
                kw["labelsize"] = kw["labelsize"] * FONT_SCALE
            return _tp(self, *a, **kw)
        tick_params._aisieval_scaled = True
        matplotlib.axes.Axes.tick_params = tick_params


_install_profile()

# A colormap in the MATS blue family, so heatmaps match the rest of the set.
if SEQ == "mats_blues":
    try:
        import matplotlib as _mpl
        from matplotlib.colors import LinearSegmentedColormap as _LSC
        _cm = _LSC.from_list("mats_blues", ["#FFFFFF", "#D6EEFF", "#7AAACC", "#366180", "#1B3A4F"])
        try:
            _mpl.colormaps.register(_cm, name="mats_blues", force=True)
        except Exception:
            _mpl.cm.register_cmap(name="mats_blues", cmap=_cm)
    except Exception:
        SEQ = "Blues"
