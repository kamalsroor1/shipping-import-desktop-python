"""
Design Tokens — Import Management System
Source: docs/DESIGN_RULES.md (Section 3 & 4 & 5)
Single source of truth for all colors, fonts, and spacing.
NEVER hardcode hex values outside this file.
"""

# ── Color System (DESIGN_RULES.md Section 3) ─────────────────────────

# Primary — #34495e
COLOR_PRIMARY             = "#34495e"
COLOR_PRIMARY_HOVER       = "#3d566e"
COLOR_PRIMARY_PRESSED     = "#2c3e50"
COLOR_PRIMARY_DISABLED    = "#95a5a6"
COLOR_ON_PRIMARY          = "#ffffff"

# Dark — #2c3e50
COLOR_DARK                = "#2c3e50"
COLOR_DARK_HOVER          = "#34495e"
COLOR_ON_DARK             = "#ecf0f1"
COLOR_DARK_BORDER         = "#1a252f"

# Background — #ecf0f1
COLOR_BACKGROUND          = "#ecf0f1"
COLOR_SURFACE             = "#ffffff"         # Cards, inputs
COLOR_SURFACE_ALT         = "#f5f6fa"         # Alt table rows
COLOR_SURFACE_HOVER       = "#dfe6e9"         # Hover on background

# Success — #27ae60
COLOR_SUCCESS             = "#27ae60"
COLOR_SUCCESS_HOVER       = "#2ecc71"
COLOR_SUCCESS_PRESSED     = "#1e8449"
COLOR_SUCCESS_BG          = "#d5f5e3"
COLOR_SUCCESS_TEXT        = "#1a5e35"

# Danger — #c0392b
COLOR_DANGER              = "#c0392b"
COLOR_DANGER_HOVER        = "#e74c3c"
COLOR_DANGER_PRESSED      = "#96281b"
COLOR_DANGER_BG           = "#fde8e6"
COLOR_DANGER_TEXT         = "#7b241c"

# Info — #2980b9
COLOR_INFO                = "#2980b9"
COLOR_INFO_HOVER          = "#3498db"
COLOR_INFO_PRESSED        = "#1a5276"
COLOR_INFO_BG             = "#d6eaf8"
COLOR_INFO_TEXT           = "#1a4a72"

# Accent — #16a085
COLOR_ACCENT              = "#16a085"
COLOR_ACCENT_HOVER        = "#1abc9c"
COLOR_ACCENT_PRESSED      = "#0e6655"
COLOR_ACCENT_FOCUS        = "#16a085"

# Warning
COLOR_WARNING             = "#e67e22"
COLOR_WARNING_BG          = "#fef9e7"
COLOR_WARNING_TEXT        = "#784212"

# Text
COLOR_TEXT_PRIMARY        = "#2c3e50"
COLOR_TEXT_SECONDARY      = "#7f8c8d"
COLOR_TEXT_MUTED          = "#bdc3c7"
COLOR_TEXT_ON_DARK        = "#ecf0f1"
COLOR_TEXT_DISABLED       = "#bdc3c7"
COLOR_TEXT_PLACEHOLDER    = "#bdc3c7"

# Borders
COLOR_BORDER              = "#bdc3c7"
COLOR_BORDER_SUBTLE       = "#dfe6e9"
COLOR_BORDER_FOCUS        = "#16a085"
COLOR_BORDER_ERROR        = "#c0392b"

# ── Typography (DESIGN_RULES.md Section 4) ────────────────────────────

FONT_ARABIC   = "Cairo"
FONT_ENGLISH  = "Inter"
FONT_FALLBACK = "Segoe UI"

# Scale: (size_px, weight)
TYPO_WINDOW_TITLE  = (20, 700)   # Application name
TYPO_PAGE_TITLE    = (18, 700)   # Top of each screen
TYPO_SECTION_TITLE = (15, 600)   # GroupBox, card titles
TYPO_BODY          = (13, 400)   # Normal body text
TYPO_BODY_MEDIUM   = (13, 500)   # Emphasized body
TYPO_SMALL         = (11, 400)   # Helper, metadata
TYPO_TABLE         = (12, 400)   # Table cell content
TYPO_BUTTON        = (13, 600)   # Button labels
TYPO_LABEL         = (12, 600)   # Form labels
TYPO_ERROR         = (12, 500)   # Inline errors
TYPO_SUCCESS_MSG   = (12, 500)   # Inline success

# ── Spacing — 8px base grid (DESIGN_RULES.md Section 5) ──────────────

SPACING_XS  = 4    # Icon gaps, chip padding
SPACING_SM  = 8    # Button vertical padding, tight items
SPACING_MD  = 16   # Button horizontal padding, card spacing
SPACING_LG  = 24   # Section padding, content margin
SPACING_XL  = 32   # Large separators
SPACING_XXL = 48   # Major layout divisions

# ── Layout Dimensions ─────────────────────────────────────────────────

DIM_SIDEBAR_WIDTH    = 240   # px — expanded
DIM_SIDEBAR_COLLAPSE = 56    # px — icon-only
DIM_TOPBAR_HEIGHT    = 52    # px
DIM_INFOBAR_HEIGHT   = 32    # px
DIM_STATUSBAR_HEIGHT = 28    # px
DIM_BUTTON_HEIGHT    = 36    # px — standard
DIM_BUTTON_SM        = 28    # px — compact
DIM_INPUT_HEIGHT     = 36    # px
DIM_TABLE_ROW        = 40    # px — standard
DIM_TABLE_ROW_COMPACT= 32    # px — compact
DIM_TABLE_HEADER     = 38    # px

# ── Border Radius ─────────────────────────────────────────────────────

RADIUS_SM     = 3    # Inputs, chips
RADIUS_DEFAULT= 4    # Buttons, most components
RADIUS_MD     = 6    # Cards, containers
RADIUS_FULL   = 9999 # Pills, badges
