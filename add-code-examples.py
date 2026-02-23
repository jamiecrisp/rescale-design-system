#!/usr/bin/env python3
"""Add code examples and usage guidance to component pages."""

import os, re, html as htmlmod

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

# ── Code example data ─────────────────────────────────────────────────
# Each entry: (filename, sections)
# sections = list of (title, description, code, notes)

EXAMPLES = {

"components/button.html": [
    ("Basic Usage", "All buttons use the <code>.rs-btn</code> base class plus a variant modifier.", """
<button class="rs-btn rs-btn--primary">Save changes</button>
<button class="rs-btn rs-btn--secondary">Cancel</button>
<button class="rs-btn rs-btn--ghost">Skip</button>
<button class="rs-btn rs-btn--danger">Delete entry</button>
""", None),
    ("Sizes", "Three sizes available. Default meets the 44px minimum tap target.", """
<button class="rs-btn rs-btn--primary rs-btn--sm">Small</button>
<button class="rs-btn rs-btn--primary">Default (44px)</button>
<button class="rs-btn rs-btn--primary rs-btn--lg">Large</button>
""", None),
    ("With Icon", "Place an SVG inside with <code>.rs-btn__icon</code>. Icon inherits the button colour via <code>currentColor</code>.", """
<button class="rs-btn rs-btn--primary">
    <svg class="rs-btn__icon" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2.5">
        <line x1="12" y1="5" x2="12" y2="19"/>
        <line x1="5" y1="12" x2="19" y2="12"/>
    </svg>
    Add entry
</button>
""", None),
    ("Full Width", "Add <code>.rs-btn--block</code> for 100% width.", """
<button class="rs-btn rs-btn--primary rs-btn--block">
    Continue
</button>
""", None),
    ("Disabled", "Add the <code>disabled</code> attribute. Pointer events are suppressed automatically.", """
<button class="rs-btn rs-btn--primary" disabled>
    Processing…
</button>
""", None),
    ("SCSS Import", "To include only the button in your build:", """
@use "@rescale/scss/settings" as *;
@use "@rescale/scss/components/button/button";
""", "SCSS"),
],

"components/input.html": [
    ("Basic Field", "Wrap inputs in <code>.rs-field</code> for consistent label/hint/error spacing.", """
<div class="rs-field">
    <label class="rs-field__label" for="weight">Today's weight</label>
    <input class="rs-input" id="weight" type="number"
           step="0.1" placeholder="82.0">
    <span class="rs-field__hint">In kilograms</span>
</div>
""", None),
    ("Required Field", "Add <code>.rs-field__label--required</code> to show a red asterisk.", """
<div class="rs-field">
    <label class="rs-field__label rs-field__label--required"
           for="name">Display name</label>
    <input class="rs-input" id="name" required>
</div>
""", None),
    ("Error State", "Add <code>.rs-field--error</code> to the wrapper. Pair with <code>.rs-field__error</code> for the message.", """
<div class="rs-field rs-field--error">
    <label class="rs-field__label" for="w2">Weight</label>
    <input class="rs-input" id="w2" value="abc">
    <span class="rs-field__error">
        <!-- optional icon SVG here -->
        Please enter a valid number
    </span>
</div>
""", None),
    ("Success State", "Use <code>.rs-field--success</code> on the wrapper.", """
<div class="rs-field rs-field--success">
    <label class="rs-field__label" for="w3">Weight</label>
    <input class="rs-input" id="w3" value="82.4">
</div>
""", None),
    ("Monospace Input", "Add <code>.rs-input--mono</code> for weight entry fields using JetBrains Mono.", """
<input class="rs-input rs-input--mono"
       type="number" step="0.1" value="82.4">
""", None),
],

"components/textarea.html": [
    ("Basic Usage", "Combine <code>.rs-input</code> and <code>.rs-textarea</code> on a <code>&lt;textarea&gt;</code> element.", """
<div class="rs-field">
    <label class="rs-field__label" for="notes">Notes</label>
    <textarea class="rs-input rs-textarea" id="notes"
              placeholder="How are you feeling today?"></textarea>
    <span class="rs-field__hint">Optional</span>
</div>
""", None),
],

"components/select.html": [
    ("Basic Usage", "Combine <code>.rs-input</code> and <code>.rs-select</code>. A custom chevron replaces the native dropdown arrow.", """
<div class="rs-field">
    <label class="rs-field__label" for="tz">Timezone</label>
    <select class="rs-input rs-select" id="tz">
        <option>Europe/London</option>
        <option>America/New_York</option>
        <option>Asia/Tokyo</option>
    </select>
</div>
""", None),
    ("When to Use", None, None, """⚠ <strong>Use sparingly.</strong> Prefer <code>.rs-radio</code> for ≤5 options. Reserve <code>&lt;select&gt;</code> for long lists (countries, timezones) where radio buttons would be overwhelming."""),
],

"components/checkbox.html": [
    ("Basic Usage", "Wrap <code>&lt;label&gt;</code> around the input and label text. The native checkbox is visually replaced.", """
<label class="rs-checkbox">
    <input type="checkbox" class="rs-checkbox__input" checked>
    <span class="rs-checkbox__label">Daily weigh-in reminder</span>
</label>
""", None),
    ("Fieldset Group", "Group related checkboxes in a <code>&lt;fieldset&gt;</code> with a <code>&lt;legend&gt;</code> for accessibility.", """
<fieldset style="border: none;">
    <legend class="rs-field__label">Notifications</legend>
    <label class="rs-checkbox">
        <input type="checkbox" class="rs-checkbox__input" checked>
        <span class="rs-checkbox__label">Daily reminder</span>
    </label>
    <label class="rs-checkbox">
        <input type="checkbox" class="rs-checkbox__input">
        <span class="rs-checkbox__label">Weekly summary</span>
    </label>
</fieldset>
""", None),
],

"components/radio.html": [
    ("Horizontal Group", "Use <code>.rs-radio-group</code> for inline layout — ideal for 2–4 short options.", """
<fieldset style="border: none;">
    <legend class="rs-field__label">Weight unit</legend>
    <div class="rs-radio-group">
        <label class="rs-radio">
            <input type="radio" name="unit"
                   class="rs-radio__input" checked>
            <span class="rs-radio__label">kg</span>
        </label>
        <label class="rs-radio">
            <input type="radio" name="unit"
                   class="rs-radio__input">
            <span class="rs-radio__label">lbs</span>
        </label>
        <label class="rs-radio">
            <input type="radio" name="unit"
                   class="rs-radio__input">
            <span class="rs-radio__label">st &amp; lbs</span>
        </label>
    </div>
</fieldset>
""", None),
    ("Vertical Group", "Use <code>.rs-radio-group--vertical</code> for longer labels or more options.", """
<div class="rs-radio-group--vertical">
    <label class="rs-radio">
        <input type="radio" name="range"
               class="rs-radio__input" checked>
        <span class="rs-radio__label">Last 7 days</span>
    </label>
    <label class="rs-radio">
        <input type="radio" name="range"
               class="rs-radio__input">
        <span class="rs-radio__label">Last 30 days</span>
    </label>
</div>
""", None),
],

"components/toggle.html": [
    ("Basic Usage", "The hidden input drives state. <code>.rs-toggle__track</code> renders the visual switch.", """
<label class="rs-toggle">
    <input type="checkbox" class="rs-toggle__input" checked>
    <span class="rs-toggle__track"></span>
    <span class="rs-toggle__label">Google Fit sync</span>
</label>
""", None),
    ("Without Label", "For settings rows where the label is separate, use <code>aria-label</code> on the input.", """
<label class="rs-toggle">
    <input type="checkbox" class="rs-toggle__input"
           aria-label="Dark mode">
    <span class="rs-toggle__track"></span>
</label>
""", None),
],

"components/range.html": [
    ("Basic Usage", "Apply <code>.rs-range</code> to a native <code>&lt;input type=\"range\"&gt;</code>.", """
<div class="rs-field">
    <label class="rs-field__label" for="goal">
        Goal weight:
        <span class="rs-text--mono" id="val">80.0</span> kg
    </label>
    <input class="rs-range" type="range" id="goal"
           min="60" max="120" step="0.5" value="80"
           oninput="document.getElementById('val')
             .textContent = parseFloat(this.value).toFixed(1)">
</div>
""", None),
],

"components/badge.html": [
    ("Variants", "Five semantic colours. All use <code>.rs-badge</code> plus a variant modifier.", """
<span class="rs-badge rs-badge--success">On track</span>
<span class="rs-badge rs-badge--danger">Off track</span>
<span class="rs-badge rs-badge--info">Synced</span>
<span class="rs-badge rs-badge--warning">Stalled</span>
<span class="rs-badge rs-badge--neutral">No data</span>
""", None),
    ("With Icon", "Add an SVG with <code>.rs-badge__icon</code>.", """
<span class="rs-badge rs-badge--success">
    <svg class="rs-badge__icon" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="20 6 9 17 4 12"/>
    </svg>
    −0.3 kg
</span>
""", None),
],

"components/chip.html": [
    ("Basic Usage", "Toggle <code>.rs-chip--active</code> on click. Chips work as filter controls.", """
<button class="rs-chip rs-chip--active">7d</button>
<button class="rs-chip">30d</button>
<button class="rs-chip">3m</button>
<button class="rs-chip">6m</button>
<button class="rs-chip">1y</button>
<button class="rs-chip">All</button>
""", None),
],

"components/alert.html": [
    ("Basic Usage", "Four semantic variants. Include an icon, title, and description.", """
<div class="rs-alert rs-alert--success">
    <svg class="rs-alert__icon" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="8 12 11 15 16 9"/>
    </svg>
    <div class="rs-alert__content">
        <div class="rs-alert__title">Goal reached!</div>
        You hit your target weight of 80.0 kg.
    </div>
</div>
""", None),
    ("Variants", "Replace <code>--success</code> with <code>--danger</code>, <code>--info</code>, or <code>--warning</code>.", """
<div class="rs-alert rs-alert--danger">…</div>
<div class="rs-alert rs-alert--info">…</div>
<div class="rs-alert rs-alert--warning">…</div>
""", None),
],

"components/toast.html": [
    ("Basic Usage", "Use <code>aria-live=\"polite\"</code> on the container so screen readers announce new toasts.", """
<div aria-live="polite">
    <div class="rs-toast">
        <svg class="rs-toast__icon" viewBox="0 0 24 24"
             fill="none" stroke="var(--rs-color-success)"
             stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="8 12 11 15 16 9"/>
        </svg>
        Entry saved — 82.4 kg
    </div>
</div>
""", None),
],

"components/progress.html": [
    ("Basic Usage", "Set width via inline style or JS. Include ARIA attributes for accessibility.", """
<div class="rs-progress rs-progress--success"
     role="progressbar"
     aria-valuenow="72" aria-valuemin="0" aria-valuemax="100">
    <div class="rs-progress__bar" style="width: 72%"></div>
</div>
""", None),
    ("Variants", None, """
<div class="rs-progress rs-progress--success">…</div>
<div class="rs-progress rs-progress--info">…</div>
<div class="rs-progress rs-progress--warning">…</div>
<div class="rs-progress rs-progress--danger">…</div>
""", None),
],

"components/tabs.html": [
    ("Basic Usage", "Use ARIA roles for accessibility. Import <code>tabs.js</code> for keyboard navigation (arrow keys, Home, End).", """
<div class="rs-tabs" role="tablist">
    <button class="rs-tabs__tab" role="tab"
            aria-selected="true">7 days</button>
    <button class="rs-tabs__tab" role="tab"
            aria-selected="false">30 days</button>
    <button class="rs-tabs__tab" role="tab"
            aria-selected="false">3 months</button>
</div>
""", None),
    ("JavaScript", "Initialise with <code>RsTabs</code> for keyboard navigation and state management.", """
import { RsTabs } from '@rescale/js/tabs.js';

const tabs = new RsTabs(
    document.querySelector('.rs-tabs'),
    (index) => {
        // Switch visible panel
        console.log('Active tab:', index);
    }
);

// Programmatic selection
tabs.select(2);
""", "JavaScript"),
],

"components/table.html": [
    ("Basic Usage", "Apply <code>.rs-table</code> to a <code>&lt;table&gt;</code>. Use <code>.rs-table__mono</code> on cells with numeric data.", """
<table class="rs-table">
    <thead>
        <tr>
            <th>Date</th>
            <th>Weight</th>
            <th>Δ Trend</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>23 Feb</td>
            <td class="rs-table__mono">95.1 kg</td>
            <td class="rs-table__mono">−0.2</td>
            <td>
                <span class="rs-badge rs-badge--success">
                    On track
                </span>
            </td>
        </tr>
    </tbody>
</table>
""", None),
],

"components/modal.html": [
    ("Basic Usage", "Use <code>hidden</code> attribute to hide. Add ARIA roles for accessibility.", """
<div class="rs-modal" id="my-modal" hidden
     role="dialog" aria-modal="true"
     aria-labelledby="modal-title">
    <div class="rs-modal__dialog">
        <button class="rs-modal__close" aria-label="Close">
            ✕
        </button>
        <h2 class="rs-modal__title" id="modal-title">
            Delete entry?
        </h2>
        <p class="rs-modal__desc">
            This will permanently remove your weigh-in
            for 23 Feb.
        </p>
        <div class="rs-modal__actions">
            <button class="rs-btn rs-btn--secondary">
                Cancel
            </button>
            <button class="rs-btn rs-btn--danger">
                Delete
            </button>
        </div>
    </div>
</div>
""", None),
    ("JavaScript", "Import <code>RsModal</code> for focus trapping, Escape key, and backdrop click to close.", """
import { RsModal } from '@rescale/js/modal.js';

const modal = new RsModal(
    document.getElementById('my-modal')
);

// Open
document.getElementById('delete-btn')
    .addEventListener('click', () => modal.open());

// Close (also triggered by Escape / backdrop click)
document.getElementById('cancel-btn')
    .addEventListener('click', () => modal.close());
""", "JavaScript"),
],

"components/empty-state.html": [
    ("Basic Usage", "Centre-aligned placeholder with icon, title, description, and a CTA button.", """
<div class="rs-empty">
    <svg class="rs-empty__icon" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" stroke-width="1.5">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <line x1="3" y1="9" x2="21" y2="9"/>
        <line x1="9" y1="3" x2="9" y2="21"/>
    </svg>
    <h3 class="rs-empty__title">No entries yet</h3>
    <p class="rs-empty__desc">
        Log your first weigh-in to start tracking.
    </p>
    <button class="rs-btn rs-btn--primary">
        Add entry
    </button>
</div>
""", None),
],

}


# ── Code block CSS (injected once per page) ────────────────────────
CODE_CSS = """
        .usage { margin-top: var(--space-16); padding-top: var(--space-8); border-top: 1px solid var(--border-decorative); }
        .usage__heading { font-size: var(--text-2xl); font-weight: var(--weight-bold); margin-bottom: var(--space-8); }
        .usage__section { margin-bottom: var(--space-10); }
        .usage__title { font-size: var(--text-sm); font-weight: var(--weight-semibold); margin-bottom: var(--space-2); }
        .usage__desc { font-size: var(--text-sm); color: var(--text-secondary); margin-bottom: var(--space-4); max-width: 640px; line-height: var(--leading-normal); }
        .usage__desc code { font-family: var(--font-mono); font-size: var(--text-xs); background: var(--bg-inset); padding: 2px 6px; border-radius: 4px; }
        .usage__note { font-size: var(--text-sm); color: var(--text-secondary); background: var(--color-warning-dim); padding: var(--space-3) var(--space-4); border-radius: var(--radius-md); margin-bottom: var(--space-4); line-height: var(--leading-normal); }
        .usage__note strong { color: var(--color-warning); }
        .usage__note code { font-family: var(--font-mono); font-size: var(--text-xs); }
        .code-block { position: relative; background: var(--bg-inset); border: 1px solid var(--border-decorative); border-radius: var(--radius-md); overflow: hidden; margin-bottom: var(--space-4); }
        .code-block__header { display: flex; justify-content: space-between; align-items: center; padding: var(--space-2) var(--space-4); border-bottom: 1px solid var(--border-decorative); background: var(--bg-elevated); }
        .code-block__lang { font-family: var(--font-mono); font-size: var(--text-2xs); color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.08em; }
        .code-block__copy { font-family: var(--font-body); font-size: var(--text-2xs); font-weight: var(--weight-semibold); background: none; border: 1px solid var(--border-decorative); border-radius: var(--radius-sm); padding: 2px 10px; color: var(--text-secondary); cursor: pointer; transition: all var(--transition-fast); }
        .code-block__copy:hover { background: var(--bg-glass-hover); color: var(--text-primary); }
        .code-block pre { margin: 0; padding: var(--space-4); overflow-x: auto; font-family: var(--font-mono); font-size: var(--text-xs); line-height: 1.6; color: var(--text-primary); }
"""


def escape_html(code):
    """HTML-escape code for display in <pre>."""
    return htmlmod.escape(code.strip())


def build_usage_section(sections):
    """Build the HTML for usage examples."""
    parts = []
    parts.append('            <div class="usage">')
    parts.append('                <h2 class="usage__heading">Usage</h2>')

    for item in sections:
        title, desc, code, note_or_lang = item
        parts.append('                <div class="usage__section">')
        parts.append(f'                    <h3 class="usage__title">{title}</h3>')

        if desc:
            parts.append(f'                    <p class="usage__desc">{desc}</p>')

        if code:
            lang = note_or_lang if note_or_lang and note_or_lang != "SCSS" and note_or_lang != "JavaScript" else note_or_lang
            if lang is None:
                lang = "HTML"
            parts.append(f'                    <div class="code-block">')
            parts.append(f'                        <div class="code-block__header"><span class="code-block__lang">{lang}</span><button class="code-block__copy" onclick="navigator.clipboard.writeText(this.closest(\'.code-block\').querySelector(\'pre\').textContent).then(()=>{{this.textContent=\'Copied!\';setTimeout(()=>this.textContent=\'Copy\',1500)}})">Copy</button></div>')
            parts.append(f'                        <pre>{escape_html(code)}</pre>')
            parts.append(f'                    </div>')
        elif note_or_lang:
            # It's a note, not code
            parts.append(f'                    <div class="usage__note">{note_or_lang}</div>')

        parts.append('                </div>')

    parts.append('            </div>')
    return "\n".join(parts)


# ── Inject into pages ─────────────────────────────────────────────────
print("Adding code examples to component pages...\n")

for rel_path, sections in EXAMPLES.items():
    filepath = os.path.join(SITE, rel_path)
    if not os.path.exists(filepath):
        print(f"  ✗ NOT FOUND: {rel_path}")
        continue

    with open(filepath) as f:
        html = f.read()

    # Skip if already has usage section
    if 'class="usage"' in html:
        print(f"  ○ Already has usage: {rel_path}")
        continue

    # Inject code block CSS into <style>
    html = html.replace("    </style>", CODE_CSS + "    </style>", 1)

    # Build usage HTML
    usage_html = build_usage_section(sections)

    # Insert before closing </main>
    html = html.replace("        </main>", usage_html + "\n        </main>", 1)

    with open(filepath, "w") as f:
        f.write(html)

    print(f"  ✓ {rel_path} ({len(sections)} examples)")

print("\n✅ Done!")
