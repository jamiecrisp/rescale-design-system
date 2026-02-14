# TrueWeight Design System

A complete design system for **TrueWeight** — a weight tracking app focused on revealing long-term trends rather than stressing over daily fluctuations.

## Overview

- **Dual themes** — Light and dark glassmorphism with full token system
- **WCAG 2.1 AA compliant** — All colours, components, and layouts tested
- **Responsive** — Desktop → tablet → mobile with bottom nav bar
- **Self-contained** — Every HTML file works standalone (no build step)

## Structure

```
├── design-system/
│   ├── foundations.html      # Tokens, typography, spacing, colour, radii, shadows
│   ├── components.html       # Buttons, form inputs, badges, alerts, tables, modals
│   └── layouts.html          # Settings, chart, log entry, onboarding, profile pages
│
├── mockups/
│   ├── dashboard/
│   │   ├── light.html        # Final accessible responsive dashboard (light)
│   │   └── dark.html         # Final accessible responsive dashboard (dark)
│   └── exploration/
│       ├── 01-typography.html    # Early concept: editorial/typography-driven
│       ├── 02-flat-ui.html       # Early concept: colourful flat UI
│       └── 03-glassmorphism-original.html  # Early concept: dark glassmorphism
│
├── icons/
│   ├── icon-home.svg         # Dashboard/home navigation icon
│   ├── icon-charts.svg       # Charts navigation icon (trend line + axis)
│   ├── icon-predictions.svg  # Predictions icon (crosshair/target)
│   ├── icon-profile.svg      # Profile navigation icon
│   ├── nav-icons-reference.html    # All nav icons in context (both themes)
│   └── trend-icons-reference.html  # Weight gain/loss/maintain indicator icons
│
└── README.md
```

## Design Tokens

All themes are driven by CSS custom properties on `:root` (light) and `[data-theme="dark"]`. Toggle between themes by setting the `data-theme` attribute on `<html>`.

### Key Tokens

| Token | Light | Dark | Purpose |
|-------|-------|------|---------|
| `--bg-page` | `#f0f2f5` | `#0a0e1a` | Page background |
| `--bg-glass` | `rgba(255,255,255,0.55)` | `rgba(255,255,255,0.06)` | Card surfaces |
| `--text-primary` | `#1a1d24` (15:1) | `#e8eaed` (16:1) | Main text |
| `--text-secondary` | `#4a4e56` (7.4:1) | `#b0b4bc` (9.3:1) | Supporting text |
| `--text-tertiary` | `#696d76` (4.6:1) | `#828690` (5.3:1) | Subdued text |
| `--color-success` | `#006B4E` (5.8:1) | `#00E5A0` (11.7:1) | Weight loss / positive |
| `--color-danger` | `#A12040` (6.7:1) | `#FF6B8A` (7.1:1) | Weight gain / negative |
| `--color-info` | `#2A4FA8` (6.7:1) | `#5B8DEF` (6.0:1) | Maintain / neutral |
| `--color-warning` | `#7A4B00` (6.6:1) | `#FFB84D` (11.2:1) | Warning |
| `--border-input` | `#7e828a` (3.9:1) | `#606472` (3.0:1) | Form input borders |

Contrast ratios shown are against the respective `--bg-page`.

## Typography

| Scale | Size | Usage |
|-------|------|-------|
| 4XL | 36px | Page hero |
| 3XL | 30px | Page title |
| 2XL | 24px | Section heading |
| XL | 20px | Card title |
| LG | 18px | Lead text |
| Base | 16px | Body (minimum) |
| SM | 14px | Secondary text |
| XS | 12px | Captions, labels |
| 2XS | 11px | Badges, overlines |

**Fonts:** Outfit (display + body), JetBrains Mono (data values + code)

## Spacing

4px base unit: `--space-1` (4px) through `--space-20` (80px).

| Context | Token |
|---------|-------|
| Page padding (desktop) | `--space-12` (48px) |
| Page padding (mobile) | `--space-4` (16px) |
| Between sections | `--space-16` (64px) |
| Card padding | `--space-6` (24px) |
| Card grid gap | `--space-4` (16px) |
| Label → input | `--space-2` (8px) |
| Between form fields | `--space-4` (16px) |

## Accessibility

Every component meets WCAG 2.1 Level AA:

- **Text contrast**: ≥ 4.5:1 (normal), ≥ 3:1 (large 18px+ bold)
- **UI contrast**: ≥ 3:1 for input borders, icons, focus indicators
- **Touch targets**: ≥ 44 × 44px on all interactive elements
- **Focus**: 3px outline with 2px offset, visible on keyboard navigation
- **Skip link**: First focusable element on every page
- **Landmarks**: `<header>`, `<nav>`, `<main>` with `aria-label`
- **Forms**: Every input has a label, errors use icon + text (never colour alone)
- **Tables**: `<caption>` + `scope` on `<th>` elements
- **Motion**: Respects `prefers-reduced-motion`
- **Screen readers**: `aria-current`, `aria-live`, `aria-hidden` on decorative elements

## Icons

SVG icons use `stroke="currentColor"` — they inherit colour from CSS automatically. No separate light/dark versions needed.

- **Nav icons**: Home, Charts, Predictions (target), Profile
- **Trend icons**: Diagonal arrows for loss (↘), gain (↗), maintain (→)

## Viewing

Open any `.html` file directly in a browser. Every page includes a theme toggle button (top-right) to switch between light and dark modes.

## Pushing to GitHub

```bash
cd trueweight-design-system
git init
git add .
git commit -m "Initial commit: TrueWeight design system"
git remote add origin git@github.com:YOUR_USERNAME/trueweight-design-system.git
git push -u origin main
```
