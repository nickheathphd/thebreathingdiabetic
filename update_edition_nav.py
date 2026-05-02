"""
update_edition_nav.py

Reads newsletter/index.html for the ordered list of posts, then injects
"Previous Edition / Next Edition" navigation into every newsletter blog post.

Run this after adding any new newsletter post:
    python3 update_edition_nav.py
"""

import re
from pathlib import Path

BLOG_DIR = Path(__file__).parent / "blog"
NEWSLETTER_INDEX = Path(__file__).parent / "newsletter" / "index.html"

NAV_CSS = """
    /* ── Edition nav ──────────────────────────────────── */
    .edition-nav {
      display: flex;
      gap: 1rem;
      margin: 3rem 0 2rem;
      border-top: 1px solid var(--border);
      padding-top: 2rem;
    }
    .edition-nav__btn {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 0.375rem;
      padding: 1rem 1.25rem;
      background: var(--cream-deep);
      border: 1px solid var(--border);
      border-radius: 8px;
      text-decoration: none;
      color: inherit;
      transition: background 0.15s ease, border-color 0.15s ease;
    }
    .edition-nav__btn:hover {
      background: var(--sage-pale);
      border-color: var(--sage);
      color: inherit;
    }
    .edition-nav__btn--prev { align-items: flex-start; }
    .edition-nav__btn--next { align-items: flex-end; text-align: right; }
    .edition-nav__label {
      font-family: var(--ff-body);
      font-size: 0.6875rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--sage);
    }
    .edition-nav__title {
      font-family: var(--ff-display);
      font-size: 0.9375rem;
      font-style: italic;
      line-height: 1.4;
      color: var(--forest);
    }
    @media (max-width: 600px) {
      .edition-nav { flex-direction: column; }
      .edition-nav__btn--next { align-items: flex-start; text-align: left; }
    }"""


def get_posts():
    with open(NEWSLETTER_INDEX, "r", encoding="utf-8") as f:
        idx = f.read()
    hrefs = re.findall(
        r'<a href="(/blog/[^"]+)"[^>]*class="archive-entry__title"', idx
    )
    posts = []
    for href in hrefs:
        path = BLOG_DIR / href.replace("/blog/", "")
        if not path.exists():
            continue
        with open(path, "r", encoding="utf-8") as f:
            fc = f.read()
        h1 = re.search(r"<h1>(.*?)</h1>", fc, re.DOTALL)
        title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else path.stem
        posts.append((href, title, path))
    return posts


def build_nav(prev_post, next_post):
    def btn(entry, direction):
        if not entry:
            return '  <div style="flex:1"></div>'
        href, title, _ = entry
        label = "&#8592; Previous Edition" if direction == "prev" else "Next Edition &#8594;"
        return (
            f'  <a href="{href}" class="edition-nav__btn edition-nav__btn--{direction}">\n'
            f'    <span class="edition-nav__label">{label}</span>\n'
            f'    <span class="edition-nav__title">{title}</span>\n'
            f"  </a>"
        )

    return (
        "\n<!-- edition-nav -->\n"
        '<div class="edition-nav">\n'
        f"{btn(prev_post, 'prev')}\n"
        f"{btn(next_post, 'next')}\n"
        "</div>\n"
        "<!-- /edition-nav -->\n"
    )


def inject(posts):
    updated = skipped = 0
    for i, (href, title, path) in enumerate(posts):
        prev_post = posts[i + 1] if i + 1 < len(posts) else None
        next_post = posts[i - 1] if i > 0 else None

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove stale nav (idempotent)
        content = re.sub(
            r"\n<!-- edition-nav -->.*?<!-- /edition-nav -->\n",
            "\n",
            content,
            flags=re.DOTALL,
        )

        # Add CSS once
        if "/* ── Edition nav" not in content:
            content = content.replace("  </style>", NAV_CSS + "\n  </style>", 1)

        nav_html = build_nav(prev_post, next_post)

        inserted = False
        for marker in [
            '        <div class="cta-box">',
            '      <div class="cta-box">',
            '<div class="cta-box">',
        ]:
            if marker in content:
                content = content.replace(marker, nav_html + marker, 1)
                inserted = True
                break

        if not inserted:
            signoff = '<p style="margin-top:3rem;">'
            if signoff in content:
                content = content.replace(signoff, nav_html + signoff, 1)
                inserted = True

        if inserted:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            updated += 1
        else:
            print(f"  WARNING: no insertion point in {path.name}")
            skipped += 1

    print(f"Edition nav updated: {updated} posts, {skipped} skipped")


if __name__ == "__main__":
    posts = get_posts()
    print(f"Found {len(posts)} newsletter posts")
    inject(posts)
