#!/usr/bin/env python3
"""Generate individual documentation pages for Re:Scale design system."""

import re, os, textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "site")

# ── Navigation structure ─────────────────────────────────────────────────
NAV = [
    ("Foundations", [
        ("Colour",             "foundations/colour.html"),
        ("Typography",         "foundations/typography.html"),
        ("Spacing",            "foundations/spacing.html"),
        ("Shape & Elevation",  "foundations/shape.html"),
        ("Accessibility",      "foundations/accessibility.html"),
    ]),
    ("Components", [
        ("Button",       "components/button.html"),
        ("Input",        "components/input.html"),
        ("Textarea",     "components/textarea.html"),
        ("Select",       "components/select.html"),
        ("Checkbox",     "components/checkbox.html"),
        ("Radio",        "components/radio.html"),
        ("Toggle",       "components/toggle.html"),
        ("Range",        "components/range.html"),
        ("Badge",        "components/badge.html"),
        ("Chip",         "components/chip.html"),
        ("Alert",        "components/alert.html"),
        ("Toast",        "components/toast.html"),
        ("Progress",     "components/progress.html"),
        ("Tabs",         "components/tabs.html"),
        ("Table",        "components/table.html"),
        ("Modal",        "components/modal.html"),
        ("Empty State",  "components/empty-state.html"),
    ]),
    ("Layouts", [
        ("Settings",     "layouts/settings.html"),
        ("Chart Detail", "layouts/chart-detail.html"),
        ("Log Entry",    "layouts/log-entry.html"),
        ("Onboarding",   "layouts/onboarding.html"),
        ("Profile",      "layouts/profile.html"),
    ]),
    ("Charts", [
        ("Components",   "charts/components.html"),
        ("Real Data",    "charts/real-data.html"),
    ]),
    ("Resources", [
        ("Icons — Nav",   "resources/icons-nav.html"),
        ("Icons — Trend", "resources/icons-trend.html"),
        ("Dashboard (Light)", "resources/dashboard-light.html"),
        ("Dashboard (Dark)",  "resources/dashboard-dark.html"),
    ]),
]


def build_nav_html(active_path, depth):
    """Build the left nav HTML. depth = how many dirs deep the page is (for relative links)."""
    prefix = "../" * depth
    lines = []
    for group_title, items in NAV:
        lines.append(f'        <div class="nav__group">')
        lines.append(f'            <div class="nav__group-title">{group_title}</div>')
        for label, path in items:
            cls = ' nav__link--active' if path == active_path else ''
            lines.append(f'            <a class="nav__link{cls}" href="{prefix}{path}">{label}</a>')
        lines.append(f'        </div>')
    return "\n".join(lines)


def build_breadcrumb(group, title, depth):
    prefix = "../" * depth
    return f'<a href="{prefix}index.html">Re:Scale</a><span class="sep">›</span>{group}<span class="sep">›</span>{title}'


def page(path, group, title, desc, body_content, extra_head="", extra_css=""):
    """Generate a full HTML page."""
    depth = path.count("/")
    prefix = "../" * depth
    nav = build_nav_html(path, depth)
    bc = build_breadcrumb(group, title, depth)

    html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Re:Scale — {title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{prefix}shell.css">
{extra_head}    <style>
{extra_css}    </style>
    <script>if(localStorage.getItem("theme")==="light")document.documentElement.removeAttribute("data-theme");</script>
</head>
<body>
    <button class="nav__toggle" id="nav-toggle" aria-label="Toggle navigation">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="nav__overlay" id="nav-overlay"></div>

    <div class="shell">
        <nav class="nav" id="nav">
            <a href="{prefix}index.html" class="nav__brand">
                <div class="nav__brand-icon">⚡</div>
                <div class="nav__brand-text">Re:<span>Scale</span></div>
            </a>
            <div class="nav__scroll">
{nav}
            </div>
            <div class="nav__footer">
                <button class="nav__theme-toggle" id="theme-btn">☀️ Light mode</button>
            </div>
        </nav>

        <main class="main">
            <div class="main__header">
                <div class="main__breadcrumb">{bc}</div>
                <h1 class="main__title">{title}</h1>
                <p class="main__desc">{desc}</p>
            </div>
{body_content}
        </main>
    </div>

    <script>
        // Theme toggle
        document.getElementById('theme-btn').addEventListener('click', function() {{
            const html = document.documentElement;
            if (html.getAttribute('data-theme') === 'dark') {{
                html.removeAttribute('data-theme');
                this.textContent = '🌙 Dark mode';
                localStorage.setItem('theme', 'light');
            }} else {{
                html.setAttribute('data-theme', 'dark');
                this.textContent = '☀️ Light mode';
                localStorage.setItem('theme', 'dark');
            }}
        }});
        if (localStorage.getItem('theme') === 'light') {{
            document.getElementById('theme-btn').textContent = '🌙 Dark mode';
        }}
        // Mobile nav
        const toggle = document.getElementById('nav-toggle');
        const nav = document.getElementById('nav');
        const overlay = document.getElementById('nav-overlay');
        toggle.addEventListener('click', () => {{ nav.classList.toggle('is-open'); overlay.classList.toggle('is-open'); }});
        overlay.addEventListener('click', () => {{ nav.classList.remove('is-open'); overlay.classList.remove('is-open'); }});
    </script>
</body>
</html>'''
    return html


def write(path, content):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print(f"  ✓ {path}")


def read_source(name):
    """Read one of the old monolithic HTML files."""
    path = os.path.join(BASE, "design-system", name)
    with open(path) as f:
        return f.read()


def extract_section(html, start_id, end_id=None):
    """Extract content between section markers."""
    # Find start
    start_match = re.search(rf'(<!--\s*═.*?{start_id}.*?═\s*-->|<h2[^>]*id="{start_id}")', html)
    if not start_match:
        return ""
    start = start_match.start()
    if end_id:
        end_match = re.search(rf'(<!--\s*═.*?{end_id}.*?═\s*-->|<h2[^>]*id="{end_id}")', html[start+1:])
        if end_match:
            return html[start:start+1+end_match.start()]
    # Take to next h2 or end of main content
    end_match = re.search(r'(<!--\s*═{4,}|<h2\s)', html[start+50:])
    if end_match:
        return html[start:start+50+end_match.start()]
    return html[start:]


# ── READ SOURCE FILES ─────────────────────────────────────────────────
print("Reading source files...")
foundations_html = read_source("foundations.html")
components_html = read_source("components.html")
layouts_html = read_source("layouts.html")


# ══════════════════════════════════════════════════════════════════════
# FOUNDATIONS
# ══════════════════════════════════════════════════════════════════════
print("\nFoundations:")

# Extract sections by finding content between section headers
def extract_foundation_section(html, section_id, next_id=None):
    """Extract a foundation section by its title id."""
    pattern = rf'<h2\s+class="ds-section-title"\s+id="{section_id}"'
    match = re.search(pattern, html)
    if not match:
        return ""
    start = match.start()
    if next_id:
        next_match = re.search(rf'<h2\s+class="ds-section-title"\s+id="{next_id}"', html[start+1:])
        if next_match:
            return html[start:start+1+next_match.start()].strip()
    return html[start:].strip()


def extract_component_section(html, section_id, next_id=None):
    """Extract a component section by its title id."""
    pattern = rf'<h2\s+class="ds-section-title"\s+id="{section_id}"'
    match = re.search(pattern, html)
    if not match:
        return ""
    start = match.start()
    if next_id:
        next_match = re.search(rf'<h2\s+class="ds-section-title"\s+id="{next_id}"', html[start+1:])
        if next_match:
            return html[start:start+1+next_match.start()].strip()
    # Otherwise go to end of main content
    end_match = re.search(r'</div>\s*</div>\s*$', html[start:])
    if end_match:
        return html[start:start+end_match.start()].strip()
    return html[start:].strip()


def extract_layout_section(html, section_title, next_title=None):
    """Extract a layout section by its label text."""
    pattern = rf'<h2 class="layout-label">{re.escape(section_title)}</h2>'
    match = re.search(pattern, html)
    if not match:
        return ""
    # Go back to the layout-section div
    section_start = html.rfind('<div class="layout-section">', 0, match.start())
    if section_start < 0:
        section_start = match.start()
    if next_title:
        next_match = re.search(rf'<h2 class="layout-label">{re.escape(next_title)}</h2>', html[section_start+1:])
        if next_match:
            # find the opening div before it
            chunk = html[section_start:section_start+1+next_match.start()]
            # trim to end of last closing </div>
            return chunk.strip()
    # Last section — go to the end
    # Find the closing </div> of the layout-section
    return html[section_start:].strip()


# Extract CSS from foundations
foundations_style = ""
match = re.search(r'<style>(.*?)</style>', foundations_html, re.DOTALL)
if match:
    foundations_style = match.group(1)

# Foundation sections
f_sections = [
    ("colours-title", "type-title"),
    ("type-title", "spacing-title"),
    ("spacing-title", "shape-title"),
    ("shape-title", "a11y-title"),
    ("a11y-title", None),
]
f_names = [
    ("colour",        "Colour",            "Semantic colour palette with light & dark tokens. All colours use CSS custom properties for runtime theming."),
    ("typography",    "Typography",        "Type scale, weights, and font stacks. Outfit for UI, JetBrains Mono for data."),
    ("spacing",       "Spacing",           "Consistent 4px-base spacing scale applied across all components."),
    ("shape",         "Shape & Elevation", "Border radii, shadows, and glassmorphism surface treatments."),
    ("accessibility", "Accessibility",     "WCAG 2.1 AA compliance — focus rings, skip links, screen reader utilities, reduced motion."),
]

for i, (slug, title, desc) in enumerate(f_names):
    section_id, next_id = f_sections[i]
    content = extract_foundation_section(foundations_html, section_id, next_id)
    # Strip the h2 title since we have our own header
    content = re.sub(r'<h2\s+class="ds-section-title"[^>]*>.*?</h2>', '', content, count=1)
    # Wrap in our section class
    body = f'            <div class="section">\n{content}\n            </div>'
    p = page(f"foundations/{slug}.html", "Foundations", title, desc, body, extra_css=foundations_style)
    write(f"foundations/{slug}.html", p)


# ══════════════════════════════════════════════════════════════════════
# COMPONENTS
# ══════════════════════════════════════════════════════════════════════
print("\nComponents:")

# Extract component CSS
comp_style = ""
match = re.search(r'<style>(.*?)</style>', components_html, re.DOTALL)
if match:
    comp_style = match.group(1)

# Component sections mapping: (id, next_id, slug, title, desc)
comp_sections = [
    ("btn-t", "form-t", "button", "Button",
     "Primary, secondary, ghost and danger variants in three sizes. All buttons meet 44px minimum tap target."),
]

# For forms, we need to split the big Form Inputs section into individual components
# Let's extract the whole Form Inputs section first, then split by sub-title

def extract_subsection(html, subtitle_text, next_subtitle_text=None):
    """Extract a subsection from component HTML by subtitle text."""
    pattern = rf'<div class="mb-10"><h3 class="ds-sub-title">{re.escape(subtitle_text)}</h3>'
    match = re.search(pattern, html)
    if not match:
        return ""
    start = match.start()
    if next_subtitle_text:
        next_pattern = rf'<div class="mb-10"><h3 class="ds-sub-title">{re.escape(next_subtitle_text)}</h3>'
        next_match = re.search(next_pattern, html[start+1:])
        if next_match:
            return html[start:start+1+next_match.start()].strip()
    # Go to next section-title h2
    next_h2 = re.search(r'<h2\s+class="ds-section-title"', html[start+1:])
    if next_h2:
        return html[start:start+1+next_h2.start()].strip()
    return html[start:].strip()


# Button — merge all button subsections
btn_content = ""
for sub in ["Variants", "Sizes", "With Icons", "Full Width"]:
    next_sub = {"Variants": "Sizes", "Sizes": "With Icons", "With Icons": "Full Width", "Full Width": None}.get(sub)
    if next_sub:
        btn_content += extract_subsection(components_html, sub, next_sub) + "\n"
    else:
        # Full Width is last before Form Inputs section
        c = extract_subsection(components_html, sub, "Text Input — States")
        btn_content += c + "\n"

write("components/button.html", page("components/button.html", "Components", "Button",
    "Primary, secondary, ghost and danger variants in three sizes. All buttons meet 44px minimum tap target.",
    f'            <div class="section">\n{btn_content}\n            </div>', extra_css=comp_style))

# Input (Text Input States + Common Fields)
input_content = extract_subsection(components_html, "Text Input — States", "Common Fields")
input_content += "\n" + extract_subsection(components_html, "Common Fields", "Textarea")
write("components/input.html", page("components/input.html", "Components", "Input",
    "Text input with validation states, hints, and monospace weight-entry variant.",
    f'            <div class="section">\n{input_content}\n            </div>', extra_css=comp_style))

# Textarea
write("components/textarea.html", page("components/textarea.html", "Components", "Textarea",
    "Multi-line text input for notes and descriptions.",
    f'            <div class="section">\n{extract_subsection(components_html, "Textarea", "Select")}\n            </div>', extra_css=comp_style))

# Select
write("components/select.html", page("components/select.html", "Components", "Select",
    "Native select dropdown. Use sparingly — prefer radio buttons for short lists.",
    f'            <div class="section">\n{extract_subsection(components_html, "Select", "Checkbox &amp; Radio")}\n            </div>', extra_css=comp_style))

# Checkbox & Radio — split into two pages
checkbox_radio = extract_subsection(components_html, "Checkbox &amp; Radio", "Toggle Switch")
# Split at the second demo-col (radio section)
write("components/checkbox.html", page("components/checkbox.html", "Components", "Checkbox",
    "Multi-select checkboxes with custom styling and accessible focus states.",
    f'            <div class="section">\n{checkbox_radio}\n            </div>', extra_css=comp_style))

write("components/radio.html", page("components/radio.html", "Components", "Radio",
    "Single-select radio buttons. Prefer over &lt;select&gt; for ≤5 options.",
    f'            <div class="section">\n{checkbox_radio}\n            </div>', extra_css=comp_style))

# Toggle
write("components/toggle.html", page("components/toggle.html", "Components", "Toggle",
    "On/off switch for boolean settings like sync, dark mode, and notifications.",
    f'            <div class="section">\n{extract_subsection(components_html, "Toggle Switch", "Range Slider")}\n            </div>', extra_css=comp_style))

# Range
write("components/range.html", page("components/range.html", "Components", "Range",
    "Slider input for continuous values like goal weight.",
    f'            <div class="section">\n{extract_subsection(components_html, "Range Slider", "Status Badges")}\n            </div>', extra_css=comp_style))

# Badge
write("components/badge.html", page("components/badge.html", "Components", "Badge",
    "Compact status indicators — success, danger, info, warning, and neutral.",
    f'            <div class="section">\n{extract_subsection(components_html, "Status Badges", "Filter Chips")}\n            </div>', extra_css=comp_style))

# Chip
write("components/chip.html", page("components/chip.html", "Components", "Chip",
    "Toggle-able filter chips for time ranges and categories.",
    f'            <div class="section">\n{extract_subsection(components_html, "Filter Chips", "Inline Alerts")}\n            </div>', extra_css=comp_style))

# Alert
write("components/alert.html", page("components/alert.html", "Components", "Alert",
    "Inline notification banners with icon, title, and description.",
    f'            <div class="section">\n{extract_subsection(components_html, "Inline Alerts", "Toast Notification")}\n            </div>', extra_css=comp_style))

# Toast
toast_content = extract_subsection(components_html, "Toast Notification", "Progress")
if not toast_content:
    toast_content = extract_subsection(components_html, "Toast Notification")
write("components/toast.html", page("components/toast.html", "Components", "Toast",
    "Ephemeral confirmation messages. Use aria-live for screen reader support.",
    f'            <div class="section">\n{toast_content}\n            </div>', extra_css=comp_style))

# Progress
progress_section = extract_component_section(components_html, "prog-t", "tab-t")
progress_section = re.sub(r'<h2\s+class="ds-section-title"[^>]*>.*?</h2>', '', progress_section, count=1)
write("components/progress.html", page("components/progress.html", "Components", "Progress",
    "Horizontal progress bars in four semantic colours.",
    f'            <div class="section">\n{progress_section}\n            </div>', extra_css=comp_style))

# Tabs
tabs_section = extract_component_section(components_html, "tab-t", "table-t")
tabs_section = re.sub(r'<h2\s+class="ds-section-title"[^>]*>.*?</h2>', '', tabs_section, count=1)
write("components/tabs.html", page("components/tabs.html", "Components", "Tabs",
    "Pill-style tab switcher for time ranges. Supports keyboard navigation via tabs.js.",
    f'            <div class="section">\n{tabs_section}\n            </div>', extra_css=comp_style))

# Table
table_section = extract_component_section(components_html, "table-t", "modal-t")
table_section = re.sub(r'<h2\s+class="ds-section-title"[^>]*>.*?</h2>', '', table_section, count=1)
write("components/table.html", page("components/table.html", "Components", "Table",
    "Data table with monospace weight columns and hover highlighting.",
    f'            <div class="section">\n{table_section}\n            </div>', extra_css=comp_style))

# Modal
modal_section = extract_component_section(components_html, "modal-t", "empty-t")
modal_section = re.sub(r'<h2\s+class="ds-section-title"[^>]*>.*?</h2>', '', modal_section, count=1)
write("components/modal.html", page("components/modal.html", "Components", "Modal",
    "Confirmation dialog with backdrop, focus trap, and escape-to-close.",
    f'            <div class="section">\n{modal_section}\n            </div>', extra_css=comp_style))

# Empty State
empty_section = extract_component_section(components_html, "empty-t")
empty_section = re.sub(r'<h2\s+class="ds-section-title"[^>]*>.*?</h2>', '', empty_section, count=1)
# Clean up trailing </div> from the page wrapper
empty_section = re.sub(r'\s*</div>\s*</div>\s*$', '', empty_section)
write("components/empty-state.html", page("components/empty-state.html", "Components", "Empty State",
    "Placeholder for screens with no data — icon, title, description and CTA.",
    f'            <div class="section">\n{empty_section}\n            </div>', extra_css=comp_style))


# ══════════════════════════════════════════════════════════════════════
# LAYOUTS
# ══════════════════════════════════════════════════════════════════════
print("\nLayouts:")

# Extract layouts CSS
layouts_style = ""
match = re.search(r'<style>(.*?)</style>', layouts_html, re.DOTALL)
if match:
    layouts_style = match.group(1)

layout_titles = ["Settings", "Chart Detail", "Log Entry", "Onboarding", "Profile"]
layout_slugs = ["settings", "chart-detail", "log-entry", "onboarding", "profile"]
layout_descs = [
    "Settings page with sidebar navigation, toggle rows, and radio groups.",
    "Full-width chart with data summary, time range filters, and entry log below.",
    "Focused single-purpose screen for logging daily weight.",
    "Multi-step wizard for first-time setup.",
    "User profile with stats, avatar, and account management.",
]

for i, (title, slug, desc) in enumerate(zip(layout_titles, layout_slugs, layout_descs)):
    next_title = layout_titles[i+1] if i+1 < len(layout_titles) else None
    content = extract_layout_section(layouts_html, title, next_title)
    # Strip the label/desc since we have our own header
    content = re.sub(r'<h2 class="layout-label">.*?</h2>', '', content, count=1)
    write(f"layouts/{slug}.html", page(f"layouts/{slug}.html", "Layouts", title, desc,
        f'            <div class="section">\n{content}\n            </div>', extra_css=layouts_style))


# ══════════════════════════════════════════════════════════════════════
# CHARTS (copy existing files as-is into iframes, or link)
# ══════════════════════════════════════════════════════════════════════
print("\nCharts:")

for slug, title, desc, src_file in [
    ("components", "Chart Components", "Trend-focused chart designs for all user scenarios.", "charts/chart-components.html"),
    ("real-data", "Real Data Demo", "415 days of real weight data visualised across 8 chart views.", "charts/chart-realdata.html"),
]:
    body = f'''            <div class="section">
                <p style="margin-bottom: var(--space-4);"><a href="../design-system/{src_file}" style="color: var(--accent);">Open full-screen →</a></p>
                <iframe src="../design-system/{src_file}" style="width:100%; height:800px; border:1px solid var(--border-decorative); border-radius: var(--radius-lg); background: var(--bg-page);" loading="lazy"></iframe>
            </div>'''
    write(f"charts/{slug}.html", page(f"charts/{slug}.html", "Charts", title, desc, body))


# ══════════════════════════════════════════════════════════════════════
# RESOURCES
# ══════════════════════════════════════════════════════════════════════
print("\nResources:")

os.makedirs(os.path.join(SITE, "resources"), exist_ok=True)

for slug, title, desc, src_file in [
    ("icons-nav", "Icons — Navigation", "SVG navigation icons for the main app shell.", "icons/nav-icons-reference.html"),
    ("icons-trend", "Icons — Trend", "Directional trend indicators for weight change.", "icons/trend-icons-reference.html"),
    ("dashboard-light", "Dashboard (Light)", "Full dashboard mockup in light theme.", "mockups/dashboard/light.html"),
    ("dashboard-dark", "Dashboard (Dark)", "Full dashboard mockup in dark theme.", "mockups/dashboard/dark.html"),
]:
    body = f'''            <div class="section">
                <p style="margin-bottom: var(--space-4);"><a href="../{src_file}" style="color: var(--accent);">Open full-screen →</a></p>
                <iframe src="../{src_file}" style="width:100%; height:800px; border:1px solid var(--border-decorative); border-radius: var(--radius-lg); background: var(--bg-page);" loading="lazy"></iframe>
            </div>'''
    write(f"resources/{slug}.html", page(f"resources/{slug}.html", "Resources", title, desc, body))


print("\n✅ All pages generated!")
print(f"   Total: {sum(len(items) for _, items in NAV)} pages + index")
