#!/usr/bin/env python3
"""Create doc pages for Bottom Nav and Topbar, and add them to all component navs."""

import os, re, glob, html as htmlmod

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "site")

# ── Read an existing component page to extract the shell ──────────────
with open(os.path.join(SITE, "components", "chip.html")) as f:
    template = f.read()

# Extract everything from start to the nav__scroll closing, the footer, and closing script
# We'll build pages from scratch using the shell.css patterns

def escape(s):
    return htmlmod.escape(s.strip())


def make_nav_links(active_slug):
    """Build the nav links HTML for the Components section."""
    items = [
        ("Button", "button"), ("Input", "input"), ("Textarea", "textarea"),
        ("Select", "select"), ("Checkbox", "checkbox"), ("Radio", "radio"),
        ("Toggle", "toggle"), ("Range", "range"), ("Badge", "badge"),
        ("Chip", "chip"), ("Alert", "alert"), ("Toast", "toast"),
        ("Progress", "progress"), ("Tabs", "tabs"), ("Table", "table"),
        ("Modal", "modal"), ("Empty State", "empty-state"),
        ("Bottom Nav", "bottom-nav"), ("Topbar", "topbar"),
    ]
    lines = []
    for label, slug in items:
        active = ' nav__link--active' if slug == active_slug else ''
        lines.append(f'            <a class="nav__link{active}" href="../components/{slug}.html">{label}</a>')
    return "\n".join(lines)


def make_page(slug, title, desc, demo_html, demo_css, usage_sections, api_rows, a11y_notes=None):
    """Generate a complete component doc page."""
    nav = make_nav_links(slug)

    # Usage HTML
    usage_parts = []
    for u_title, u_desc, u_code, u_lang in usage_sections:
        lang = u_lang or "HTML"
        block = f'''                <div class="usage__section">
                    <h3 class="usage__title">{u_title}</h3>'''
        if u_desc:
            block += f'\n                    <p class="usage__desc">{u_desc}</p>'
        if u_code:
            block += f'''
                    <div class="code-block">
                        <div class="code-block__header"><span class="code-block__lang">{lang}</span><button class="code-block__copy" onclick="navigator.clipboard.writeText(this.closest('.code-block').querySelector('pre').textContent).then(()=>{{this.textContent='Copied!';setTimeout(()=>this.textContent='Copy',1500)}})">Copy</button></div>
                        <pre>{escape(u_code)}</pre>
                    </div>'''
        block += '\n                </div>'
        usage_parts.append(block)
    usage_html = "\n".join(usage_parts)

    # API table
    api_rows_html = ""
    for cls, el, d in api_rows:
        api_rows_html += f'                    <tr><td><code>{cls}</code></td><td>{el}</td><td>{d}</td></tr>\n'

    # A11y
    a11y_html = ""
    if a11y_notes:
        a11y_items = "\n".join(
            f'                    <li style="font-size: var(--text-sm); color: var(--text-secondary); padding: var(--space-2) 0; border-bottom: 1px solid var(--border-decorative); display: flex; gap: var(--space-3); align-items: baseline;"><span style="color: var(--color-success); flex-shrink: 0;">✓</span> <span>{n}</span></li>'
            for n in a11y_notes
        )
        a11y_html = f'''
            <div class="api" style="margin-top: var(--space-8);">
                <h3 class="api__heading">Accessibility</h3>
                <ul style="list-style: none; padding: 0; margin: 0;">
{a11y_items}
                </ul>
            </div>'''

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Re:Scale — {title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../shell.css">
    <link rel="stylesheet" href="../../src/dist/rescale.css">
    <style>
{demo_css}
        .usage {{ margin-top: var(--space-16); padding-top: var(--space-8); border-top: 1px solid var(--border-decorative); }}
        .usage__heading {{ font-size: var(--text-2xl); font-weight: var(--weight-bold); margin-bottom: var(--space-8); }}
        .usage__section {{ margin-bottom: var(--space-10); }}
        .usage__title {{ font-size: var(--text-sm); font-weight: var(--weight-semibold); margin-bottom: var(--space-2); }}
        .usage__desc {{ font-size: var(--text-sm); color: var(--text-secondary); margin-bottom: var(--space-4); max-width: 640px; line-height: var(--leading-normal); }}
        .usage__desc code {{ font-family: var(--font-mono); font-size: var(--text-xs); background: var(--bg-inset); padding: 2px 6px; border-radius: 4px; }}
        .code-block {{ position: relative; background: var(--bg-inset); border: 1px solid var(--border-decorative); border-radius: var(--radius-md); overflow: hidden; margin-bottom: var(--space-4); }}
        .code-block__header {{ display: flex; justify-content: space-between; align-items: center; padding: var(--space-2) var(--space-4); border-bottom: 1px solid var(--border-decorative); background: var(--bg-elevated); }}
        .code-block__lang {{ font-family: var(--font-mono); font-size: var(--text-2xs); color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.08em; }}
        .code-block__copy {{ font-family: var(--font-body); font-size: var(--text-2xs); font-weight: var(--weight-semibold); background: none; border: 1px solid var(--border-decorative); border-radius: var(--radius-sm); padding: 2px 10px; color: var(--text-secondary); cursor: pointer; transition: all var(--transition-fast); }}
        .code-block__copy:hover {{ background: var(--bg-glass-hover); color: var(--text-primary); }}
        .api {{ margin-top: var(--space-10); }}
        .api__heading {{ font-size: var(--text-sm); font-weight: var(--weight-semibold); margin-bottom: var(--space-4); }}
        .api__table {{ width: 100%; border-collapse: collapse; font-size: var(--text-sm); }}
        .api__table th {{ text-align: left; font-size: var(--text-2xs); font-weight: var(--weight-semibold); text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-tertiary); padding: var(--space-2) var(--space-4); border-bottom: 1px solid var(--border-decorative); }}
        .api__table td {{ padding: var(--space-2) var(--space-4); border-bottom: 1px solid var(--border-decorative); vertical-align: top; }}
        .api__table code {{ font-family: var(--font-mono); font-size: var(--text-xs); background: var(--bg-inset); padding: 1px 6px; border-radius: 4px; white-space: nowrap; }}
        .api__table td:last-child {{ color: var(--text-secondary); }}
        .api__table tbody tr:hover {{ background: var(--accent-dim); }}
    </style>
    <script>if(localStorage.getItem("theme")==="light")document.documentElement.removeAttribute("data-theme");</script>
</head>
<body>
    <button class="nav__toggle" id="nav-toggle" aria-label="Toggle navigation">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="nav__overlay" id="nav-overlay"></div>

    <div class="shell">
        <nav class="nav" id="nav">
            <a href="../../index.html" class="nav__brand">
                <div class="nav__brand-icon">⚡</div>
                <div class="nav__brand-text">Re:<span>Scale</span></div>
            </a>
            <div class="nav__scroll">
        <div class="nav__group">
            <div class="nav__group-title">Components</div>
{nav}
        </div></div>
            <div class="nav__footer">
                <button class="nav__theme-toggle" id="theme-btn">☀️ Light mode</button>
            </div>
        </nav>

        <main class="main">
            <div class="main__header">
                <div class="main__breadcrumb"><a href="../../index.html">Re:Scale</a><span class="sep">›</span>Components<span class="sep">›</span>{title}</div>
                <h1 class="main__title">{title}</h1>
                <p class="main__desc">{desc}</p>
            </div>
            <div class="section">
{demo_html}
            </div>
            <div class="usage">
                <h2 class="usage__heading">Usage</h2>
{usage_html}
            </div>
            <div class="api">
                <h3 class="api__heading">{title} Classes</h3>
                <table class="api__table">
                    <thead><tr><th>Class / Attr</th><th>Element</th><th>Description</th></tr></thead>
                    <tbody>
{api_rows_html}                    </tbody>
                </table>
            </div>{a11y_html}
        </main>
    </div>

    <script>
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
        const toggle = document.getElementById('nav-toggle');
        const nav = document.getElementById('nav');
        const overlay = document.getElementById('nav-overlay');
        toggle.addEventListener('click', () => {{ nav.classList.toggle('is-open'); overlay.classList.toggle('is-open'); }});
        overlay.addEventListener('click', () => {{ nav.classList.remove('is-open'); overlay.classList.remove('is-open'); }});
    </script>
</body>
</html>'''

# ══════════════════════════════════════════════════════════════════════
# BOTTOM NAV PAGE
# ══════════════════════════════════════════════════════════════════════
print("Creating Bottom Nav page...")

bottom_nav_demo = '''
                <h3 style="font-size: var(--text-xs); font-weight: var(--weight-semibold); text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-tertiary); margin-bottom: var(--space-4);">Preview</h3>
                <p style="font-size: var(--text-sm); color: var(--text-secondary); margin-bottom: var(--space-6);">The bottom nav is only visible below 640px. Resize your browser or view on mobile to see it. The preview below simulates the mobile appearance.</p>
                <div class="demo-phone">
                    <div class="demo-phone__screen">
                        <div class="demo-phone__content">
                            <div style="text-align: center; padding: var(--space-8) 0; color: var(--text-tertiary); font-size: var(--text-sm);">App content area</div>
                        </div>
                        <nav class="demo-bottom-nav">
                            <a href="#" class="demo-bottom-nav__item demo-bottom-nav__item--active">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/></svg>
                                <span>Home</span>
                            </a>
                            <a href="#" class="demo-bottom-nav__item">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zm6-4a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zm6-3a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/></svg>
                                <span>Charts</span>
                            </a>
                            <a href="#" class="demo-bottom-nav__item">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/></svg>
                                <span>Log</span>
                            </a>
                            <a href="#" class="demo-bottom-nav__item">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/></svg>
                                <span>Predict</span>
                            </a>
                            <a href="#" class="demo-bottom-nav__item">
                                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clip-rule="evenodd"/></svg>
                                <span>Profile</span>
                            </a>
                        </nav>
                    </div>
                </div>'''

bottom_nav_css = '''        .demo-phone { max-width: 375px; margin: 0 auto; }
        .demo-phone__screen { border: 1px solid var(--border-decorative); border-radius: var(--radius-xl); overflow: hidden; background: var(--bg-page); position: relative; }
        .demo-phone__content { min-height: 200px; display: flex; align-items: center; justify-content: center; padding-bottom: 72px; }
        .demo-bottom-nav { display: flex; position: absolute; bottom: 0; left: 0; right: 0; height: 72px; background: var(--bg-elevated); backdrop-filter: blur(20px); border-top: 1px solid var(--border-decorative); box-shadow: var(--shadow-lg); padding: 8px 8px; justify-content: space-around; align-items: center; }
        .demo-bottom-nav__item { display: flex; flex-direction: column; align-items: center; gap: 3px; text-decoration: none; color: var(--text-tertiary); font-size: 0.62rem; font-weight: 500; padding: 6px 10px; border-radius: var(--radius-md); min-width: 52px; transition: color 0.15s ease; }
        .demo-bottom-nav__item svg { width: 20px; height: 20px; }
        .demo-bottom-nav__item--active { color: var(--accent); }
        .demo-bottom-nav__item:hover { color: var(--text-primary); }
'''

bottom_nav_usage = [
    ("Basic Usage", "The bottom nav appears only on mobile (below 640px). Place it at the end of <code>&lt;body&gt;</code>. Add <code>.rs-container</code> to your main content wrapper to add bottom padding automatically.", """
<body>
    <main class="rs-container">
        <!-- App content -->
    </main>

    <nav class="rs-bottom-nav" aria-label="Main navigation">
        <a href="/" class="rs-bottom-nav__item rs-bottom-nav__item--active"
           aria-current="page">
            <svg width="20" height="20" viewBox="0 0 20 20"
                 fill="currentColor">
                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0
                    001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0
                    001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001
                    1h2a1 1 0 001-1v-6.586l.293.293a1 1 0
                    001.414-1.414l-7-7z"/>
            </svg>
            <span>Home</span>
        </a>
        <a href="/charts" class="rs-bottom-nav__item">
            <svg>…</svg>
            <span>Charts</span>
        </a>
        <a href="/log" class="rs-bottom-nav__item">
            <svg>…</svg>
            <span>Log</span>
        </a>
        <a href="/profile" class="rs-bottom-nav__item">
            <svg>…</svg>
            <span>Profile</span>
        </a>
    </nav>
</body>
""", None),
    ("SCSS Import", "Import only the bottom nav component:", """
@use "@rescale/scss/settings" as *;
@use "@rescale/scss/components/bottom-nav/bottom-nav";
""", "SCSS"),
]

bottom_nav_api = [
    (".rs-bottom-nav",              "&lt;nav&gt;",  "Container — hidden on desktop, fixed to bottom on mobile (≤640px)"),
    (".rs-bottom-nav__item",        "&lt;a&gt;",    "Nav item — flex column with icon + label, 52px min-width"),
    (".rs-bottom-nav__item--active","",              "Active state — accent colour"),
    (".rs-container",               "&lt;main&gt;", "Content wrapper — adds bottom padding on mobile to prevent overlap"),
]

bottom_nav_a11y = [
    "Add <code>aria-label=\"Main navigation\"</code> to the <code>&lt;nav&gt;</code> element",
    "Mark the current page with <code>aria-current=\"page\"</code> on the active link",
    "Icons should have <code>fill=\"currentColor\"</code> so colour changes with state",
    "All tap targets meet the 44px minimum (52px min-width × 72px nav height)",
]

with open(os.path.join(SITE, "components", "bottom-nav.html"), "w") as f:
    f.write(make_page("bottom-nav", "Bottom Nav", "Mobile-only fixed bottom navigation bar with icon + label items. Hidden on desktop.",
        bottom_nav_demo, bottom_nav_css, bottom_nav_usage, bottom_nav_api, bottom_nav_a11y))
print("  ✓ site/components/bottom-nav.html")


# ══════════════════════════════════════════════════════════════════════
# TOPBAR PAGE
# ══════════════════════════════════════════════════════════════════════
print("Creating Topbar page...")

topbar_demo = '''
                <h3 style="font-size: var(--text-xs); font-weight: var(--weight-semibold); text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-tertiary); margin-bottom: var(--space-4);">Preview</h3>

                <div class="card" style="padding: var(--space-4); margin-bottom: var(--space-6);">
                    <div class="rs-topbar">
                        <a href="#" class="rs-topbar__brand">
                            <div class="rs-topbar__brand-glyph">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                            </div>
                            <div class="rs-topbar__brand-text">Re:<span>Scale</span></div>
                        </a>
                        <nav class="rs-topbar__nav">
                            <a href="#" class="rs-topbar__nav-link rs-topbar__nav-link--active">Home</a>
                            <a href="#" class="rs-topbar__nav-link">Charts</a>
                            <a href="#" class="rs-topbar__nav-link">Log</a>
                            <a href="#" class="rs-topbar__nav-link">Predict</a>
                        </nav>
                        <div class="rs-topbar__user">
                            <div class="rs-topbar__user-avatar" aria-label="Profile menu">JC</div>
                        </div>
                    </div>
                </div>

                <h3 style="font-size: var(--text-xs); font-weight: var(--weight-semibold); text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-tertiary); margin-bottom: var(--space-4); margin-top: var(--space-10);">Without Navigation</h3>
                <p style="font-size: var(--text-sm); color: var(--text-secondary); margin-bottom: var(--space-4);">On mobile, the nav links are hidden (replaced by the bottom nav). The topbar shows just the brand + avatar.</p>

                <div class="card" style="padding: var(--space-4); max-width: 375px;">
                    <div class="rs-topbar">
                        <a href="#" class="rs-topbar__brand">
                            <div class="rs-topbar__brand-glyph">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                            </div>
                            <div class="rs-topbar__brand-text">Re:<span>Scale</span></div>
                        </a>
                        <div class="rs-topbar__user">
                            <div class="rs-topbar__user-avatar" aria-label="Profile menu">JC</div>
                        </div>
                    </div>
                </div>'''

topbar_css = '''        .card { background: var(--bg-glass); border: 1px solid var(--border-decorative); border-radius: var(--radius-xl); backdrop-filter: blur(16px); }
'''

topbar_usage = [
    ("Basic Usage", "The topbar contains three sections: brand, nav, and user avatar. On mobile (≤640px), the nav section is hidden.", """
<header class="rs-topbar">
    <a href="/" class="rs-topbar__brand">
        <div class="rs-topbar__brand-glyph">
            <svg width="20" height="20" viewBox="0 0 24 24"
                 fill="none" stroke="white" stroke-width="2.5">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
        </div>
        <div class="rs-topbar__brand-text">
            Re:<span>Scale</span>
        </div>
    </a>

    <nav class="rs-topbar__nav">
        <a href="/" class="rs-topbar__nav-link
           rs-topbar__nav-link--active">Home</a>
        <a href="/charts" class="rs-topbar__nav-link">Charts</a>
        <a href="/log" class="rs-topbar__nav-link">Log</a>
        <a href="/predict" class="rs-topbar__nav-link">Predict</a>
    </nav>

    <div class="rs-topbar__user">
        <div class="rs-topbar__user-avatar"
             aria-label="Profile menu">JC</div>
    </div>
</header>
""", None),
    ("Brand Only", "For pages where navigation isn't needed (e.g. onboarding), omit the nav and user sections.", """
<header class="rs-topbar">
    <a href="/" class="rs-topbar__brand">
        <div class="rs-topbar__brand-glyph">…</div>
        <div class="rs-topbar__brand-text">
            Re:<span>Scale</span>
        </div>
    </a>
</header>
""", None),
    ("SCSS Import", "Import only the topbar component:", """
@use "@rescale/scss/settings" as *;
@use "@rescale/scss/components/topbar/topbar";
""", "SCSS"),
]

topbar_api = [
    (".rs-topbar",                   "&lt;header&gt;", "Container — flex row with space-between, bottom margin"),
    (".rs-topbar__brand",            "&lt;a&gt;",      "Brand link — flex row with glyph + text"),
    (".rs-topbar__brand-glyph",      "&lt;div&gt;",    "38×38 gradient icon container"),
    (".rs-topbar__brand-text",       "&lt;div&gt;",    "Brand wordmark (20px, semibold). <code>&lt;span&gt;</code> inside gets accent colour"),
    (".rs-topbar__nav",              "&lt;nav&gt;",    "Pill-shaped nav container — glass background, hidden on mobile"),
    (".rs-topbar__nav-link",         "&lt;a&gt;",      "Nav link — 12px text, rounded, hover/active states"),
    (".rs-topbar__nav-link--active", "",                "Active link — glass background, primary text, shadow"),
    (".rs-topbar__user",             "&lt;div&gt;",    "User section container — flex row"),
    (".rs-topbar__user-avatar",      "&lt;div&gt;",    "36×36 gradient avatar — initials, hover scale effect"),
]

topbar_a11y = [
    "Use <code>&lt;header&gt;</code> element for the topbar container",
    "Wrap nav links in <code>&lt;nav&gt;</code> with <code>aria-label</code>",
    "Mark the active link with <code>aria-current=\"page\"</code>",
    "Avatar should have <code>aria-label=\"Profile menu\"</code> for screen readers",
    "On mobile, navigation moves to <code>.rs-bottom-nav</code> — don't duplicate links",
]

with open(os.path.join(SITE, "components", "topbar.html"), "w") as f:
    f.write(make_page("topbar", "Topbar", "Desktop header with brand, navigation links, and user avatar. Nav links hidden on mobile in favour of bottom nav.",
        topbar_demo, topbar_css, topbar_usage, topbar_api, topbar_a11y))
print("  ✓ site/components/topbar.html")


# ══════════════════════════════════════════════════════════════════════
# ADD NAV LINKS TO ALL EXISTING COMPONENT PAGES
# ══════════════════════════════════════════════════════════════════════
print("\nAdding nav links to existing component pages...")

new_links = '''            <a class="nav__link" href="../components/bottom-nav.html">Bottom Nav</a>
            <a class="nav__link" href="../components/topbar.html">Topbar</a>'''

for filepath in sorted(glob.glob(os.path.join(SITE, "components", "*.html"))):
    basename = os.path.basename(filepath)
    if basename in ("bottom-nav.html", "topbar.html"):
        continue  # already have the links

    with open(filepath) as f:
        html = f.read()

    # Check if links already added
    if "bottom-nav.html" in html:
        print(f"  ○ {basename} — already has links")
        continue

    # Insert after the Empty State link
    html = html.replace(
        '<a class="nav__link" href="../components/empty-state.html">Empty State</a>',
        '<a class="nav__link" href="../components/empty-state.html">Empty State</a>\n' + new_links
    )

    with open(filepath, "w") as f:
        f.write(html)
    print(f"  ✓ {basename}")


# ══════════════════════════════════════════════════════════════════════
# CREATE EXAMPLE HTML FILES IN SRC
# ══════════════════════════════════════════════════════════════════════
print("\nCreating src example HTML files...")

# Bottom nav example
bn_example = '''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bottom Nav — Re:Scale Component Example</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../dist/rescale.css">
    <style>
        body { min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .hint { text-align: center; color: var(--rs-text-tertiary); font-size: var(--rs-text-sm); padding: var(--rs-space-8); }
    </style>
</head>
<body>
    <main class="rs-container">
        <div class="hint">
            <p>Resize to ≤640px to see the bottom nav</p>
        </div>
    </main>

    <nav class="rs-bottom-nav" aria-label="Main navigation">
        <a href="#" class="rs-bottom-nav__item rs-bottom-nav__item--active" aria-current="page">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/></svg>
            <span>Home</span>
        </a>
        <a href="#" class="rs-bottom-nav__item">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zm6-4a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zm6-3a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/></svg>
            <span>Charts</span>
        </a>
        <a href="#" class="rs-bottom-nav__item">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd"/></svg>
            <span>Log</span>
        </a>
        <a href="#" class="rs-bottom-nav__item">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clip-rule="evenodd"/></svg>
            <span>Profile</span>
        </a>
    </nav>
</body>
</html>'''

with open(os.path.join(BASE, "src", "scss", "components", "bottom-nav", "example.html"), "w") as f:
    f.write(bn_example)
print("  ✓ src/scss/components/bottom-nav/example.html")

# Topbar example
tb_example = '''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Topbar — Re:Scale Component Example</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../dist/rescale.css">
    <style>
        body { padding: var(--rs-space-6); }
    </style>
</head>
<body>
    <header class="rs-topbar">
        <a href="#" class="rs-topbar__brand">
            <div class="rs-topbar__brand-glyph">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            </div>
            <div class="rs-topbar__brand-text">Re:<span>Scale</span></div>
        </a>

        <nav class="rs-topbar__nav" aria-label="Main navigation">
            <a href="#" class="rs-topbar__nav-link rs-topbar__nav-link--active" aria-current="page">Home</a>
            <a href="#" class="rs-topbar__nav-link">Charts</a>
            <a href="#" class="rs-topbar__nav-link">Log</a>
            <a href="#" class="rs-topbar__nav-link">Predict</a>
        </nav>

        <div class="rs-topbar__user">
            <div class="rs-topbar__user-avatar" aria-label="Profile menu">JC</div>
        </div>
    </header>
</body>
</html>'''

with open(os.path.join(BASE, "src", "scss", "components", "topbar", "example.html"), "w") as f:
    f.write(tb_example)
print("  ✓ src/scss/components/topbar/example.html")


print("\n✅ Done!")
