#!/usr/bin/env python3
"""Add .cta-box .btn-primary override to all calm-reset day pages."""
from pathlib import Path

ROOT = Path('/Users/nheath411/thebreathingdiabetic')

OLD = '    .cta-box p  { color: rgba(255,255,255,0.72); font-size: 1rem; line-height: 1.7; max-width: 500px; margin: 0 auto 1.5rem; }'

NEW = '''\
    .cta-box p  { color: rgba(255,255,255,0.72); font-size: 1rem; line-height: 1.7; max-width: 500px; margin: 0 auto 1.5rem; }
    .cta-box .btn-primary { background: var(--cream); color: var(--forest); }
    .cta-box .btn-primary:hover { background: var(--white); box-shadow: 0 6px 24px rgba(0,0,0,0.18); transform: translateY(-2px); }'''


def main():
    calm_dir = ROOT / 'calm-reset'
    targets = sorted(calm_dir.glob('day-*.html'))
    updated = 0
    for path in targets:
        text = path.read_text(encoding='utf-8')
        if OLD in text:
            path.write_text(text.replace(OLD, NEW, 1), encoding='utf-8')
            updated += 1
            print(f'  Updated {path.name}')
        else:
            print(f'  SKIPPED {path.name}')
    print(f'\nDone: {updated}/{len(targets)} updated')


if __name__ == '__main__':
    main()
