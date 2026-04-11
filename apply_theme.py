#!/usr/bin/env python3
"""
Apply The Breathing Diabetic redesign theme to all inner HTML pages.

What this script does to each eligible file:
  1. Removes the old Inter font link (/fonts/inter.css)
  2. Removes any existing Google Fonts preconnect/link tags
  3. Removes any existing /css/theme.css link (idempotent)
  4. Injects Google Fonts preconnect + link tags
  5. Injects /css/theme.css link AFTER the closing </style> tag
     in <head> (so theme.css specificity beats inline styles).
     Falls back to injecting before </head> if no <style> block.

Files/dirs that are NEVER modified:
  - index.html            (old homepage — keep as-is)
  - index-redesign.html   (redesign source — has its own styles)
  - hero-preview.html     (dev scratch file)
  - apply_theme.py        (this script)
  - Files inside: .git/, content/, css/
"""
import os
import re
from pathlib import Path

ROOT = Path('/Users/nheath411/thebreathingdiabetic')

# Files at the root level to skip
SKIP_ROOT_FILES = {'index.html', 'index-redesign.html', 'hero-preview.html'}

# Directory names to skip (anywhere in path)
SKIP_DIRS = {'.git', 'content', 'css', '__pycache__'}

# ── Injected HTML blocks ───────────────────────────────────────────

FONTS_BLOCK = (
    '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garant'
    ':ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,600'
    '&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600'
    '&display=swap" rel="stylesheet">'
)

THEME_LINK = '  <link rel="stylesheet" href="/css/theme.css">'

INJECT_BLOCK = FONTS_BLOCK + '\n' + THEME_LINK


# ── Patterns to strip ─────────────────────────────────────────────

# Old Inter local font
RE_INTER = re.compile(
    r'[ \t]*<link[^>]+/fonts/inter\.css[^>]*/?>[ \t]*\n?',
    re.IGNORECASE
)

# Any Google Fonts preconnect lines
RE_GF_PRECONNECT = re.compile(
    r'[ \t]*<link[^>]+fonts\.gstatic\.com[^>]*/?>[ \t]*\n?',
    re.IGNORECASE
)
RE_GF_GOOGLEAPIS = re.compile(
    r'[ \t]*<link[^>]+fonts\.googleapis\.com[^>]*/?>[ \t]*\n?',
    re.IGNORECASE
)

# Existing theme.css link
RE_THEME = re.compile(
    r'[ \t]*<link[^>]+/css/theme\.css[^>]*/?>[ \t]*\n?',
    re.IGNORECASE
)


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = rel.parts

    # Skip root-level special files
    if len(parts) == 1 and parts[0] in SKIP_ROOT_FILES:
        return True

    # Skip if any parent directory is in SKIP_DIRS
    for part in parts[:-1]:
        if part in SKIP_DIRS or part.startswith('.'):
            return True

    return False


def process_file(path: Path) -> tuple[bool, str]:
    """Returns (was_changed, reason)."""
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        return False, f'read error: {e}'

    original = text

    # Guard: must look like an HTML file
    if '<html' not in text.lower():
        return False, 'not HTML'

    # 1. Strip old font / theme links
    text = RE_INTER.sub('', text)
    text = RE_GF_PRECONNECT.sub('', text)
    text = RE_GF_GOOGLEAPIS.sub('', text)
    text = RE_THEME.sub('', text)

    # 2. Find injection point: after last </style> inside <head>
    head_end_match = re.search(r'</head>', text, re.IGNORECASE)
    if not head_end_match:
        return False, 'no </head> found'

    head_end = head_end_match.start()

    # Find last </style> before </head>
    style_end_match = None
    for m in re.finditer(r'</style>', text[:head_end], re.IGNORECASE):
        style_end_match = m

    if style_end_match:
        pos = style_end_match.end()
        text = text[:pos] + '\n' + INJECT_BLOCK + '\n' + text[pos:]
    else:
        # No inline <style>; inject before </head>
        text = text[:head_end] + INJECT_BLOCK + '\n' + text[head_end:]

    if text == original:
        return False, 'no change needed'

    try:
        path.write_text(text, encoding='utf-8')
    except Exception as e:
        return False, f'write error: {e}'

    return True, 'ok'


def main():
    updated = []
    skipped_special = []
    skipped_no_change = []
    errors = []

    html_files = sorted(ROOT.rglob('*.html'))

    for path in html_files:
        if should_skip(path):
            skipped_special.append(path.relative_to(ROOT))
            continue

        changed, reason = process_file(path)
        rel = path.relative_to(ROOT)

        if changed:
            updated.append(rel)
            print(f'  UPDATED  {rel}')
        elif reason == 'no change needed':
            skipped_no_change.append(rel)
        else:
            errors.append((rel, reason))
            print(f'  SKIPPED  {rel}  ({reason})')

    print()
    print(f'Results:')
    print(f'  Updated  : {len(updated)}')
    print(f'  No change: {len(skipped_no_change)}')
    print(f'  Protected: {len(skipped_special)}')
    if errors:
        print(f'  Errors   : {len(errors)}')
        for rel, reason in errors:
            print(f'    {rel}: {reason}')


if __name__ == '__main__':
    main()
