#!/usr/bin/env python3
"""Add class API reference tables to component pages (after the usage section)."""

import os, re

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

# ── API table CSS ──────────────────────────────────────────────────────
API_CSS = """
        .api { margin-top: var(--space-10); }
        .api__heading { font-size: var(--text-sm); font-weight: var(--weight-semibold); margin-bottom: var(--space-4); }
        .api__table { width: 100%; border-collapse: collapse; font-size: var(--text-sm); }
        .api__table th { text-align: left; font-size: var(--text-2xs); font-weight: var(--weight-semibold); text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-tertiary); padding: var(--space-2) var(--space-4); border-bottom: 1px solid var(--border-decorative); }
        .api__table td { padding: var(--space-2) var(--space-4); border-bottom: 1px solid var(--border-decorative); vertical-align: top; }
        .api__table code { font-family: var(--font-mono); font-size: var(--text-xs); background: var(--bg-inset); padding: 1px 6px; border-radius: 4px; white-space: nowrap; }
        .api__table td:last-child { color: var(--text-secondary); }
        .api__table tbody tr:hover { background: var(--accent-dim); }
"""

# ── Class API data ─────────────────────────────────────────────────────
# Each: (filename, table_title, rows: [(class, element, description)])

APIS = {

"components/button.html": ("Button Classes", [
    (".rs-btn",            "&lt;button&gt;, &lt;a&gt;", "Base button — required on all buttons"),
    (".rs-btn--primary",   "",     "Filled accent background, white text"),
    (".rs-btn--secondary", "",     "Glass background with border"),
    (".rs-btn--ghost",     "",     "Transparent background, accent text"),
    (".rs-btn--danger",    "",     "Red filled background"),
    (".rs-btn--sm",        "",     "Small size (36px height, 12px text)"),
    (".rs-btn--lg",        "",     "Large size (52px height, 16px text)"),
    (".rs-btn--block",     "",     "Full width (100%)"),
    (".rs-btn__icon",      "&lt;svg&gt;", "16×16 icon inside button"),
    ("disabled",           "attr", "Disabled state — 45% opacity, no pointer events"),
]),

"components/input.html": ("Input Classes", [
    (".rs-field",                 "&lt;div&gt;",   "Field wrapper — stacks label, input, hint/error with 8px gap"),
    (".rs-field__label",          "&lt;label&gt;", "Label text (14px, medium weight)"),
    (".rs-field__label--required", "",              "Appends red asterisk after label"),
    (".rs-field__hint",           "&lt;span&gt;",  "Help text below input (12px, tertiary)"),
    (".rs-field__error",          "&lt;span&gt;",  "Error message (12px, danger colour)"),
    (".rs-field--error",          ".rs-field",      "Error state — red border + focus ring"),
    (".rs-field--success",        ".rs-field",      "Success state — green border"),
    (".rs-input",                 "&lt;input&gt;",  "Text input (44px min-height, 10px radius)"),
    (".rs-input--mono",           "",                "JetBrains Mono font for weight entry"),
    ("disabled",                  "attr",            "Disabled — 50% opacity, inset background"),
]),

"components/textarea.html": ("Textarea Classes", [
    (".rs-input",    "&lt;textarea&gt;", "Base input styles — apply to textarea"),
    (".rs-textarea", "&lt;textarea&gt;", "Adds min-height (100px) and vertical resize"),
]),

"components/select.html": ("Select Classes", [
    (".rs-input",  "&lt;select&gt;", "Base input styles — apply to select"),
    (".rs-select", "&lt;select&gt;", "Replaces native arrow with custom chevron, adds right padding"),
]),

"components/checkbox.html": ("Checkbox Classes", [
    (".rs-checkbox",         "&lt;label&gt;", "Wrapper — flex row with 12px gap, 44px min-height"),
    (".rs-checkbox__input",  "&lt;input type=\"checkbox\"&gt;", "20×20 custom checkbox (hides native, shows checkmark when checked)"),
    (".rs-checkbox__label",  "&lt;span&gt;", "Label text (14px)"),
]),

"components/radio.html": ("Radio Classes", [
    (".rs-radio",              "&lt;label&gt;",              "Wrapper — flex row with 12px gap, 44px min-height"),
    (".rs-radio__input",       "&lt;input type=\"radio\"&gt;", "20×20 custom radio (dot indicator when checked)"),
    (".rs-radio__label",       "&lt;span&gt;",              "Label text (14px)"),
    (".rs-radio-group",        "&lt;div&gt;",               "Horizontal layout — flex-wrap with 16px column gap"),
    (".rs-radio-group--vertical", "&lt;div&gt;",            "Vertical layout — stacked column"),
]),

"components/toggle.html": ("Toggle Classes", [
    (".rs-toggle",         "&lt;label&gt;",   "Wrapper — inline-flex, 44px min-height"),
    (".rs-toggle__input",  "&lt;input type=\"checkbox\"&gt;", "Hidden input — drives :checked state (sr-only)"),
    (".rs-toggle__track",  "&lt;span&gt;",    "44×24 track with 16px thumb that slides on check"),
    (".rs-toggle__label",  "&lt;span&gt;",    "Label text (14px)"),
]),

"components/range.html": ("Range Classes", [
    (".rs-range", "&lt;input type=\"range\"&gt;", "Styled range slider — 6px track, 22px accent thumb"),
]),

"components/badge.html": ("Badge Classes", [
    (".rs-badge",           "&lt;span&gt;",  "Base badge — inline-flex, 12px text, semibold"),
    (".rs-badge--success",  "",               "Green (on track, goal met)"),
    (".rs-badge--danger",   "",               "Red (off track, error)"),
    (".rs-badge--info",     "",               "Blue (synced, informational)"),
    (".rs-badge--warning",  "",               "Amber (stalled, caution)"),
    (".rs-badge--neutral",  "",               "Grey (no data)"),
    (".rs-badge__icon",     "&lt;svg&gt;",   "12×12 icon before text"),
]),

"components/chip.html": ("Chip Classes", [
    (".rs-chip",          "&lt;button&gt;", "Filter chip — pill shape, 36px height, border"),
    (".rs-chip--active",  "",                "Selected state — accent background + border"),
]),

"components/alert.html": ("Alert Classes", [
    (".rs-alert",           "&lt;div&gt;",  "Base alert — flex row with icon, padded, rounded"),
    (".rs-alert--success",  "",              "Green — success/goal-reached"),
    (".rs-alert--danger",   "",              "Red — error/failure"),
    (".rs-alert--info",     "",              "Blue — tip/information"),
    (".rs-alert--warning",  "",              "Amber — caution/data gap"),
    (".rs-alert__icon",     "&lt;svg&gt;",  "20×20 icon (left column)"),
    (".rs-alert__content",  "&lt;div&gt;",  "Flex-1 container for title + description"),
    (".rs-alert__title",    "&lt;div&gt;",  "Bold title line"),
]),

"components/toast.html": ("Toast Classes", [
    (".rs-toast",       "&lt;div&gt;",  "Toast — inline-flex, elevated background, large shadow"),
    (".rs-toast__icon", "&lt;svg&gt;",  "18×18 icon (colour via stroke attribute)"),
]),

"components/progress.html": ("Progress Classes", [
    (".rs-progress",           "&lt;div&gt;", "Track — 8px height, inset background, full radius"),
    (".rs-progress--success",  "",              "Green bar"),
    (".rs-progress--info",     "",              "Blue bar"),
    (".rs-progress--warning",  "",              "Amber bar"),
    (".rs-progress--danger",   "",              "Red bar"),
    (".rs-progress__bar",      "&lt;div&gt;", "Fill — set width via style or JS. Animates on change (0.5s)"),
]),

"components/tabs.html": ("Tabs Classes", [
    (".rs-tabs",                     "&lt;div&gt;",    "Container — inline-flex, inset background, pill shape"),
    (".rs-tabs__tab",                "&lt;button&gt;", "Individual tab — 36px height, 12px text"),
    ('.rs-tabs__tab[aria-selected="true"]', "",         "Active state — glass background, primary text, shadow"),
]),

"components/table.html": ("Table Classes", [
    (".rs-table",       "&lt;table&gt;", "Base table — full width, collapsed borders"),
    (".rs-table__mono", "&lt;td&gt;",    "Monospace cell for numeric data (weight, deltas)"),
]),

"components/modal.html": ("Modal Classes", [
    (".rs-modal",          "&lt;div&gt;",    "Backdrop overlay — fixed, centered, z-index 150"),
    (".rs-modal__dialog",  "&lt;div&gt;",    "Dialog box — 480px max, elevated background, large shadow"),
    (".rs-modal__title",   "&lt;h2&gt;",     "Heading (20px, bold)"),
    (".rs-modal__desc",    "&lt;p&gt;",      "Description text (14px, secondary)"),
    (".rs-modal__actions", "&lt;div&gt;",    "Button row — flex, end-aligned, 12px gap"),
    (".rs-modal__close",   "&lt;button&gt;", "Close button — absolute top-right, 36×36 hit area"),
    ("hidden",             "attr",            "Hides the modal (display: none)"),
]),

"components/empty-state.html": ("Empty State Classes", [
    (".rs-empty",        "&lt;div&gt;", "Wrapper — centred text, vertical padding"),
    (".rs-empty__icon",  "&lt;svg&gt;", "64×64 icon (50% opacity, tertiary colour)"),
    (".rs-empty__title", "&lt;h3&gt;",  "Heading (18px, semibold)"),
    (".rs-empty__desc",  "&lt;p&gt;",   "Description (14px, secondary, 320px max-width)"),
]),

}

# Also add accessibility notes per component
A11Y = {
"components/button.html": [
    "All buttons meet 44px minimum tap target (WCAG 2.5.8)",
    "Focus ring uses <code>:focus-visible</code> — visible on keyboard, hidden on click",
    "Use <code>&lt;button&gt;</code> for actions, <code>&lt;a&gt;</code> with <code>.rs-btn</code> for navigation",
    "Disabled buttons use <code>pointer-events: none</code> and <code>opacity: 0.45</code>",
],
"components/input.html": [
    "Always pair <code>.rs-input</code> with a <code>&lt;label&gt;</code> via matching <code>for</code>/<code>id</code>",
    "Error messages should use <code>aria-describedby</code> linking to the <code>.rs-field__error</code> element",
    "Required fields: add both <code>.rs-field__label--required</code> (visual) and <code>required</code> attribute (semantic)",
],
"components/checkbox.html": [
    "The <code>&lt;label&gt;</code> wrapper makes the entire row clickable",
    "Group related checkboxes in <code>&lt;fieldset&gt;</code> with <code>&lt;legend&gt;</code>",
],
"components/radio.html": [
    "Always wrap radio groups in <code>&lt;fieldset&gt;</code> with <code>&lt;legend&gt;</code>",
    "Shared <code>name</code> attribute ensures only one selection per group",
],
"components/toggle.html": [
    "The hidden <code>&lt;input&gt;</code> remains in the tab order and announces state to screen readers",
    "Use <code>aria-label</code> if <code>.rs-toggle__label</code> is omitted",
],
"components/tabs.html": [
    "Add <code>role=\"tablist\"</code> to <code>.rs-tabs</code> and <code>role=\"tab\"</code> to each <code>.rs-tabs__tab</code>",
    "Set <code>aria-selected=\"true\"</code> on the active tab, <code>false</code> on others",
    "Import <code>tabs.js</code> for arrow-key navigation (Left/Right/Home/End)",
    "Link tabs to panels with <code>aria-controls</code> and <code>id</code>",
],
"components/modal.html": [
    "Add <code>role=\"dialog\"</code>, <code>aria-modal=\"true\"</code>, and <code>aria-labelledby</code> pointing to the title",
    "Import <code>modal.js</code> for focus trapping — Tab cycles within the dialog",
    "Escape key and backdrop click close the modal",
    "Focus returns to the trigger element on close",
],
"components/progress.html": [
    "Add <code>role=\"progressbar\"</code>, <code>aria-valuenow</code>, <code>aria-valuemin</code>, and <code>aria-valuemax</code>",
],
"components/toast.html": [
    "Wrap toast container in <code>aria-live=\"polite\"</code> so screen readers announce new toasts",
    "Toasts should auto-dismiss after 3–5 seconds",
],
}


def build_api_table(title, rows):
    lines = []
    lines.append('            <div class="api">')
    lines.append(f'                <h3 class="api__heading">{title}</h3>')
    lines.append('                <table class="api__table">')
    lines.append('                    <thead><tr><th>Class / Attr</th><th>Element</th><th>Description</th></tr></thead>')
    lines.append('                    <tbody>')
    for cls, el, desc in rows:
        lines.append(f'                    <tr><td><code>{cls}</code></td><td>{el}</td><td>{desc}</td></tr>')
    lines.append('                    </tbody>')
    lines.append('                </table>')
    lines.append('            </div>')
    return "\n".join(lines)


def build_a11y_section(notes):
    lines = []
    lines.append('            <div class="api" style="margin-top: var(--space-8);">')
    lines.append('                <h3 class="api__heading">Accessibility</h3>')
    lines.append('                <ul style="list-style: none; padding: 0; margin: 0;">')
    for note in notes:
        lines.append(f'                    <li style="font-size: var(--text-sm); color: var(--text-secondary); padding: var(--space-2) 0; border-bottom: 1px solid var(--border-decorative); display: flex; gap: var(--space-3); align-items: baseline;"><span style="color: var(--color-success); flex-shrink: 0;">✓</span> <span>{note}</span></li>')
    lines.append('                </ul>')
    lines.append('            </div>')
    return "\n".join(lines)


print("Adding API reference tables and a11y notes...\n")

for rel_path, (title, rows) in APIS.items():
    filepath = os.path.join(SITE, rel_path)
    if not os.path.exists(filepath):
        print(f"  ✗ NOT FOUND: {rel_path}")
        continue

    with open(filepath) as f:
        html = f.read()

    # Skip if already has API table
    if 'class="api"' in html:
        print(f"  ○ Already has API: {rel_path}")
        continue

    # Add API CSS
    html = html.replace("    </style>", API_CSS + "    </style>", 1)

    # Build sections
    api_html = build_api_table(title, rows)
    a11y_html = ""
    if rel_path in A11Y:
        a11y_html = "\n" + build_a11y_section(A11Y[rel_path])

    # Insert before closing </main>
    injection = api_html + a11y_html
    html = html.replace("        </main>", injection + "\n        </main>", 1)

    with open(filepath, "w") as f:
        f.write(html)

    a11y_count = len(A11Y.get(rel_path, []))
    print(f"  ✓ {rel_path} — {len(rows)} classes" + (f", {a11y_count} a11y notes" if a11y_count else ""))

print("\n✅ Done!")
