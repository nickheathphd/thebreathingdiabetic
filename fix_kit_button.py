#!/usr/bin/env python3
"""
Add a JS snippet after the Kit embed script in all blog posts.
The snippet polls for Kit's button and forces forest-green color,
overriding Kit's inline style which CSS !important can't always beat.
"""
import re
from pathlib import Path

ROOT = Path('/Users/nheath411/thebreathingdiabetic')

OLD = '      <script async data-uid="b0db7b731a" src="https://breathlearning.kit.com/b0db7b731a/index.js"></script>'

NEW = '''\
      <script async data-uid="b0db7b731a" src="https://breathlearning.kit.com/b0db7b731a/index.js"></script>
      <script>(function(){var t=setInterval(function(){var b=document.querySelector('.formkit-submit');if(b){b.style.setProperty('background-color','#1B2E23','important');b.style.setProperty('border-color','#1B2E23','important');b.style.setProperty('border-radius','100px','important');b.style.setProperty('font-family','\'DM Sans\',sans-serif','important');clearInterval(t);}},50);setTimeout(function(){clearInterval(t);},8000);})();</script>'''


def main():
    blog_dir = ROOT / 'blog'
    targets = [p for p in sorted(blog_dir.glob('*.html')) if p.name != 'index.html']

    updated = 0
    for path in targets:
        text = path.read_text(encoding='utf-8')
        if OLD in text:
            path.write_text(text.replace(OLD, NEW, 1), encoding='utf-8')
            updated += 1

    print(f'Updated {updated} / {len(targets)} blog posts')


if __name__ == '__main__':
    main()
