#!/usr/bin/env python3
"""
Fix the site structure:
1. Root index.html = standalone homepage (no left nav)
2. Section pages get scoped left nav (only their own section's links)
"""

import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "site")

# ── Section mapping ────────────────────────────────────────────────────
# folder_prefix → nav group title to KEEP
SECTION_MAP = {
    "foundations": "Foundations",
    "components":  "Components",
    "layouts":     "Layouts",
    "charts":      "Charts",
    "resources":   "Resources",
}


# ══════════════════════════════════════════════════════════════════════
# 1. SCOPE LEFT NAV ON SECTION PAGES
# ══════════════════════════════════════════════════════════════════════
print("Scoping section navs...\n")

for section_folder, keep_title in SECTION_MAP.items():
    pattern = os.path.join(SITE, section_folder, "*.html")
    files = sorted(glob.glob(pattern))

    for filepath in files:
        with open(filepath) as f:
            html = f.read()

        # Find all nav__group blocks and remove ones that don't match
        # Pattern: <div class="nav__group"> ... </div> (with nav__group-title inside)
        def replace_nav(match):
            block = match.group(0)
            # Extract the group title
            title_match = re.search(r'class="nav__group-title">([^<]+)<', block)
            if title_match:
                title = title_match.group(1).strip()
                if title == keep_title:
                    return block  # Keep this group
            return ""  # Remove this group

        new_html = re.sub(
            r'<div class="nav__group">.*?</div>\s*(?=<div class="nav__group">|</div>\s*<div class="nav__footer">)',
            replace_nav,
            html,
            flags=re.DOTALL
        )

        # Handle the last nav group (before nav__footer)
        # The regex above might miss the last group, so also handle it
        new_html = re.sub(
            r'(<div class="nav__group">(?:(?!<div class="nav__group">).)*?</div>)\s*(\s*</div>\s*<div class="nav__footer">)',
            lambda m: (m.group(1) if keep_title in m.group(1) else "") + m.group(2),
            new_html,
            flags=re.DOTALL
        )

        if new_html != html:
            with open(filepath, "w") as f:
                f.write(new_html)
            print(f"  ✓ {section_folder}/{os.path.basename(filepath)} → only '{keep_title}'")
        else:
            print(f"  ○ {section_folder}/{os.path.basename(filepath)} — unchanged")

print()


# ══════════════════════════════════════════════════════════════════════
# 2. NEW ROOT INDEX (no sidebar)
# ══════════════════════════════════════════════════════════════════════
print("Writing root index.html (standalone homepage)...\n")

homepage = '''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Re:Scale Design System</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg-page: #f0f2f5; --bg-glass: rgba(255,255,255,0.55); --bg-glass-hover: rgba(255,255,255,0.7);
            --bg-elevated: #ffffff; --bg-inset: #e8eaed;
            --border-decorative: rgba(0,0,0,0.10);
            --text-primary: #1a1d24; --text-secondary: #4a4e56; --text-tertiary: #696d76;
            --accent: #006B4E; --accent-dim: rgba(0,107,78,0.12); --accent-on: #ffffff;
            --font-body: 'Outfit', sans-serif; --font-mono: 'JetBrains Mono', monospace;
            --text-3xl: 1.875rem; --text-2xl: 1.5rem; --text-xl: 1.25rem; --text-lg: 1.125rem;
            --text-base: 1rem; --text-sm: 0.875rem; --text-xs: 0.75rem; --text-2xs: 0.6875rem;
            --weight-medium: 500; --weight-semibold: 600; --weight-bold: 700;
            --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-5: 20px;
            --space-6: 24px; --space-8: 32px; --space-10: 40px; --space-12: 48px; --space-16: 64px;
            --radius-sm: 6px; --radius-md: 10px; --radius-lg: 14px; --radius-xl: 16px; --radius-full: 9999px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.06); --shadow-md: 0 2px 12px rgba(0,0,0,0.06);
            --transition-fast: 0.15s ease;
        }
        [data-theme="dark"] {
            --bg-page: #0a0e1a; --bg-glass: rgba(255,255,255,0.06); --bg-glass-hover: rgba(255,255,255,0.1);
            --bg-elevated: #131722; --bg-inset: #0d1120;
            --border-decorative: rgba(255,255,255,0.10);
            --text-primary: #e8eaed; --text-secondary: #b0b4bc; --text-tertiary: #828690;
            --accent: #00E5A0; --accent-dim: rgba(0,229,160,0.15); --accent-on: #0a0e1a;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.2); --shadow-md: 0 2px 12px rgba(0,0,0,0.2);
        }

        body { font-family: var(--font-body); font-size: var(--text-base); line-height: 1.5; color: var(--text-primary); background: var(--bg-page); -webkit-font-smoothing: antialiased; }
        *:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
        *:focus:not(:focus-visible) { outline: none; }

        .page { max-width: 960px; margin: 0 auto; padding: var(--space-8) var(--space-6); }

        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-16); }
        .brand { display: flex; align-items: center; gap: var(--space-3); text-decoration: none; color: var(--text-primary); }
        .brand__icon { width: 32px; height: 32px; background: var(--accent); color: var(--accent-on); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-size: var(--text-sm); font-weight: var(--weight-bold); }
        .brand__text { font-size: var(--text-base); font-weight: var(--weight-bold); }
        .brand__text span { color: var(--accent); }
        .theme-toggle { background: var(--bg-glass); border: 1px solid var(--border-decorative); border-radius: var(--radius-full); padding: var(--space-2) var(--space-4); font-family: var(--font-body); font-size: var(--text-xs); font-weight: var(--weight-semibold); color: var(--text-secondary); cursor: pointer; backdrop-filter: blur(12px); }
        .theme-toggle:hover { background: var(--bg-glass-hover); }

        .hero { text-align: center; margin-bottom: var(--space-16); }
        .hero__title { font-size: var(--text-3xl); font-weight: var(--weight-bold); margin-bottom: var(--space-2); }
        .hero__title span { color: var(--accent); }
        .hero__desc { font-size: var(--text-lg); color: var(--text-secondary); max-width: 480px; margin: 0 auto var(--space-8); }
        .hero__stats { display: flex; gap: var(--space-8); justify-content: center; flex-wrap: wrap; }
        .stat__value { font-size: var(--text-2xl); font-weight: var(--weight-bold); font-family: var(--font-mono); color: var(--accent); }
        .stat__label { font-size: var(--text-xs); color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.08em; }

        .group { margin-bottom: var(--space-12); }
        .group__title { font-size: var(--text-xs); font-weight: var(--weight-semibold); text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-tertiary); margin-bottom: var(--space-4); }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: var(--space-4); }
        .card { background: var(--bg-glass); border: 1px solid var(--border-decorative); border-radius: var(--radius-xl); padding: var(--space-5) var(--space-6); backdrop-filter: blur(16px); text-decoration: none; color: var(--text-primary); transition: all var(--transition-fast); display: block; }
        .card:hover { border-color: var(--accent); transform: translateY(-2px); box-shadow: var(--shadow-md); }
        .card__title { font-size: var(--text-sm); font-weight: var(--weight-semibold); margin-bottom: 2px; }
        .card__desc { font-size: var(--text-xs); color: var(--text-tertiary); }

        @media (max-width: 640px) {
            .page { padding: var(--space-4); }
            .hero__stats { gap: var(--space-4); }
            .grid { grid-template-columns: 1fr 1fr; }
        }
    </style>
    <script>if(localStorage.getItem("theme")==="light")document.documentElement.removeAttribute("data-theme");</script>
</head>
<body>
    <div class="page">
        <header class="header">
            <a href="index.html" class="brand">
                <div class="brand__icon">⚡</div>
                <div class="brand__text">Re:<span>Scale</span></div>
            </a>
            <button class="theme-toggle" id="theme-btn">☀️ Light mode</button>
        </header>

        <div class="hero">
            <h1 class="hero__title">Re:<span>Scale</span> Design System</h1>
            <p class="hero__desc">Glassmorphism UI for weight tracking. WCAG AA, dark-first, SCSS&nbsp;+&nbsp;BEM.</p>
            <div class="hero__stats">
                <div class="stat"><div class="stat__value">17</div><div class="stat__label">Components</div></div>
                <div class="stat"><div class="stat__value">5</div><div class="stat__label">Layouts</div></div>
                <div class="stat"><div class="stat__value">2</div><div class="stat__label">Themes</div></div>
                <div class="stat"><div class="stat__value">AA</div><div class="stat__label">WCAG</div></div>
            </div>
        </div>

        <div class="group">
            <div class="group__title">Foundations</div>
            <div class="grid">
                <a class="card" href="site/foundations/colour.html"><div class="card__title">Colour</div><div class="card__desc">Semantic palette, light &amp; dark tokens</div></a>
                <a class="card" href="site/foundations/typography.html"><div class="card__title">Typography</div><div class="card__desc">Type scale, weights, font stacks</div></a>
                <a class="card" href="site/foundations/spacing.html"><div class="card__title">Spacing</div><div class="card__desc">4px-base spacing scale</div></a>
                <a class="card" href="site/foundations/shape.html"><div class="card__title">Shape &amp; Elevation</div><div class="card__desc">Radii, shadows, glassmorphism</div></a>
                <a class="card" href="site/foundations/accessibility.html"><div class="card__title">Accessibility</div><div class="card__desc">Focus, skip links, reduced motion</div></a>
            </div>
        </div>

        <div class="group">
            <div class="group__title">Components</div>
            <div class="grid">
                <a class="card" href="site/components/button.html"><div class="card__title">Button</div><div class="card__desc">4 variants, 3 sizes, icon support</div></a>
                <a class="card" href="site/components/input.html"><div class="card__title">Input</div><div class="card__desc">Text input with validation states</div></a>
                <a class="card" href="site/components/textarea.html"><div class="card__title">Textarea</div><div class="card__desc">Multi-line text entry</div></a>
                <a class="card" href="site/components/select.html"><div class="card__title">Select</div><div class="card__desc">Native dropdown (use sparingly)</div></a>
                <a class="card" href="site/components/checkbox.html"><div class="card__title">Checkbox</div><div class="card__desc">Multi-select, custom styling</div></a>
                <a class="card" href="site/components/radio.html"><div class="card__title">Radio</div><div class="card__desc">Single-select, horizontal &amp; vertical</div></a>
                <a class="card" href="site/components/toggle.html"><div class="card__title">Toggle</div><div class="card__desc">On/off switch for settings</div></a>
                <a class="card" href="site/components/range.html"><div class="card__title">Range</div><div class="card__desc">Slider for continuous values</div></a>
                <a class="card" href="site/components/badge.html"><div class="card__title">Badge</div><div class="card__desc">5 semantic status indicators</div></a>
                <a class="card" href="site/components/chip.html"><div class="card__title">Chip</div><div class="card__desc">Filter chips for time ranges</div></a>
                <a class="card" href="site/components/alert.html"><div class="card__title">Alert</div><div class="card__desc">Inline notification banners</div></a>
                <a class="card" href="site/components/toast.html"><div class="card__title">Toast</div><div class="card__desc">Ephemeral confirmations</div></a>
                <a class="card" href="site/components/progress.html"><div class="card__title">Progress</div><div class="card__desc">Horizontal progress bars</div></a>
                <a class="card" href="site/components/tabs.html"><div class="card__title">Tabs</div><div class="card__desc">Pill-style tab switcher</div></a>
                <a class="card" href="site/components/table.html"><div class="card__title">Table</div><div class="card__desc">Data table with mono columns</div></a>
                <a class="card" href="site/components/modal.html"><div class="card__title">Modal</div><div class="card__desc">Dialog with focus trap</div></a>
                <a class="card" href="site/components/empty-state.html"><div class="card__title">Empty State</div><div class="card__desc">No-data placeholder with CTA</div></a>
            </div>
        </div>

        <div class="group">
            <div class="group__title">Layouts</div>
            <div class="grid">
                <a class="card" href="site/layouts/settings.html"><div class="card__title">Settings</div><div class="card__desc">Toggles, radio groups, sidebar</div></a>
                <a class="card" href="site/layouts/chart-detail.html"><div class="card__title">Chart Detail</div><div class="card__desc">Full chart with data summary</div></a>
                <a class="card" href="site/layouts/log-entry.html"><div class="card__title">Log Entry</div><div class="card__desc">Daily weigh-in screen</div></a>
                <a class="card" href="site/layouts/onboarding.html"><div class="card__title">Onboarding</div><div class="card__desc">Multi-step wizard</div></a>
                <a class="card" href="site/layouts/profile.html"><div class="card__title">Profile</div><div class="card__desc">Stats, avatar, account</div></a>
            </div>
        </div>

        <div class="group">
            <div class="group__title">Charts &amp; Resources</div>
            <div class="grid">
                <a class="card" href="site/charts/components.html"><div class="card__title">Chart Components</div><div class="card__desc">Trend-focused chart designs</div></a>
                <a class="card" href="site/charts/real-data.html"><div class="card__title">Real Data Demo</div><div class="card__desc">415 days of real weight data</div></a>
                <a class="card" href="site/resources/icons-nav.html"><div class="card__title">Icons — Nav</div><div class="card__desc">SVG navigation icons</div></a>
                <a class="card" href="site/resources/icons-trend.html"><div class="card__title">Icons — Trend</div><div class="card__desc">Directional trend indicators</div></a>
                <a class="card" href="site/resources/dashboard-light.html"><div class="card__title">Dashboard (Light)</div><div class="card__desc">Full mockup — light theme</div></a>
                <a class="card" href="site/resources/dashboard-dark.html"><div class="card__title">Dashboard (Dark)</div><div class="card__desc">Full mockup — dark theme</div></a>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('theme-btn').addEventListener('click', function() {
            const html = document.documentElement;
            if (html.getAttribute('data-theme') === 'dark') {
                html.removeAttribute('data-theme');
                this.textContent = '🌙 Dark mode';
                localStorage.setItem('theme', 'light');
            } else {
                html.setAttribute('data-theme', 'dark');
                this.textContent = '☀️ Light mode';
                localStorage.setItem('theme', 'dark');
            }
        });
        if (localStorage.getItem('theme') === 'light') {
            document.getElementById('theme-btn').textContent = '🌙 Dark mode';
        }
    </script>
</body>
</html>'''

with open(os.path.join(BASE, "index.html"), "w") as f:
    f.write(homepage)
print("  ✓ index.html (standalone homepage, no sidebar)\n")


# ══════════════════════════════════════════════════════════════════════
# 3. SCOPE LEFT NAVS
# ══════════════════════════════════════════════════════════════════════
print("Scoping section navs...\n")

for section_folder, keep_title in SECTION_MAP.items():
    pattern = os.path.join(SITE, section_folder, "*.html")
    files = sorted(glob.glob(pattern))

    for filepath in files:
        with open(filepath) as f:
            html = f.read()

        # Strategy: find the nav__scroll div, extract only the matching group
        # Find all nav groups
        groups = list(re.finditer(
            r'(<div class="nav__group">.*?</div>)\s*(?=<div class="nav__group">|</div>\s*</div>)',
            html, re.DOTALL
        ))

        if not groups:
            # Try alternate pattern — last group before nav__footer
            print(f"  ⚠ No groups found in {section_folder}/{os.path.basename(filepath)}")
            continue

        # Find which groups to keep
        keep_blocks = []
        remove_blocks = []
        for g in groups:
            block = g.group(1)
            title_m = re.search(r'nav__group-title">([^<]+)<', block)
            if title_m and title_m.group(1).strip() == keep_title:
                keep_blocks.append(block)
            else:
                remove_blocks.append(g)

        if not remove_blocks:
            print(f"  ○ {section_folder}/{os.path.basename(filepath)} — already scoped")
            continue

        # Remove non-matching groups
        for g in reversed(remove_blocks):
            start, end = g.start(), g.end()
            # Also remove trailing whitespace
            while end < len(html) and html[end] in ' \n\r\t':
                end += 1
            html = html[:start] + html[end:]

        with open(filepath, "w") as f:
            f.write(html)
        print(f"  ✓ {section_folder}/{os.path.basename(filepath)}")

# ══════════════════════════════════════════════════════════════════════
# 4. CLEAN UP: remove site/index.html (no longer needed)
# ══════════════════════════════════════════════════════════════════════
site_index = os.path.join(SITE, "index.html")
if os.path.exists(site_index):
    os.remove(site_index)
    print(f"\n  ✓ Removed site/index.html (replaced by root index.html)")

print("\n✅ Done!")
