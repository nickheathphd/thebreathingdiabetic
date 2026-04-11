#!/usr/bin/env python3
"""
Replace the hardcoded-inline-style blue newsletter section
in all blog posts with a new version using the design tokens.
"""
import re
from pathlib import Path

ROOT = Path('/Users/nheath411/thebreathingdiabetic')

OLD_PATTERN = re.compile(
    r'<!--\s*──\s*Newsletter signup\s*──\s*-->\s*'
    r'<section style="background:#F0F7FF;border-top:1px solid #E8EDF3;padding:3rem 0;">'
    r'.*?'
    r'</section>',
    re.DOTALL
)

NEW_SECTION = '''\
  <!-- ── Newsletter signup ── -->
  <section style="background:var(--cream-deep);border-top:1px solid rgba(74,119,89,0.18);padding:4rem 0;">
    <div style="max-width:680px;margin:0 auto;padding:0 2rem;text-align:center;">
      <p style="font-family:\'DM Sans\',sans-serif;font-size:.6875rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#4A7759;margin-bottom:.75rem;">The Breathing 411</p>
      <h2 style="font-family:\'Cormorant Garant\',Georgia,serif;font-size:clamp(1.5rem,2.5vw,2.25rem);font-weight:500;color:#1B2E23;margin-bottom:.75rem;line-height:1.2;letter-spacing:-0.01em;">Get the Free Weekly Newsletter</h2>
      <p style="font-family:\'DM Sans\',sans-serif;font-size:1rem;line-height:1.72;color:#3D3A30;margin-bottom:1.75rem;">Weekly breath science, wisdom, and practical tools.</p>
      <script async data-uid="b0db7b731a" src="https://breathlearning.kit.com/b0db7b731a/index.js"></script>
    </div>
  </section>'''


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    new_text, n = OLD_PATTERN.subn(NEW_SECTION, text, count=1)
    if n == 0 or new_text == text:
        return False
    path.write_text(new_text, encoding='utf-8')
    return True


def main():
    blog_dir = ROOT / 'blog'
    targets = [p for p in sorted(blog_dir.glob('*.html')) if p.name != 'index.html']

    updated = 0
    for path in targets:
        if process(path):
            updated += 1

    print(f'Updated {updated} / {len(targets)} blog posts')


if __name__ == '__main__':
    main()
