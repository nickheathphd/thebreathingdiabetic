#!/usr/bin/env python3
"""Replace <style> block in all calm-reset/day-*.html with themed CSS."""
import re
from pathlib import Path

ROOT = Path('/Users/nheath411/thebreathingdiabetic')

NEW_STYLE = """  <style>
    /* Page-specific styles — calm-reset day pages
       Nav / footer / body / buttons handled by /css/theme.css */

    .container    { max-width: 1080px; margin: 0 auto; padding: 0 2rem; }
    .content-wrap { max-width: 720px;  margin: 0 auto; }

    /* Page content typography */
    h1 { font-size: clamp(1.875rem, 4vw, 2.75rem); font-weight: 500; line-height: 1.15; letter-spacing: -0.01em; color: var(--forest); }
    h2 { font-size: 1.5rem; font-weight: 500; line-height: 1.3; letter-spacing: -0.01em; color: var(--forest); }
    h3 { font-size: 1rem; font-weight: 600; letter-spacing: -0.01em; color: var(--forest); }
    p  { font-size: 1.0625rem; line-height: 1.8; color: var(--forest-mid); }

    /* "7-Day Calm Reset" label */
    .label {
      display: block;
      font-size: 0.6875rem; font-weight: 600;
      letter-spacing: 0.13em; text-transform: uppercase;
      color: var(--sage); margin-bottom: 0.875rem;
    }

    /* Page hero */
    .page-hero {
      padding: 4rem 0 3.5rem; text-align: center;
      background: linear-gradient(180deg, var(--cream) 0%, var(--white) 100%);
      border-bottom: 1px solid var(--border);
    }
    .page-hero .label { font-size: 0.75rem; letter-spacing: 0.12em; margin-bottom: 1.5rem; }
    .page-hero h1 { margin-bottom: 1rem; }
    .page-hero .subtitle {
      font-size: 1.125rem; color: var(--forest-mid);
      line-height: 1.65; max-width: 540px; margin: 0 auto;
    }

    /* Progress tracker */
    .progress { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin: 2rem 0 0; }
    .progress__dot { width: 10px; height: 10px; border-radius: 50%; background: var(--cream-deep); }
    .progress__dot.active    { background: var(--forest); width: 12px; height: 12px; }
    .progress__dot.completed { background: var(--sage); }
    .progress__label {
      font-size: 0.8125rem; font-weight: 500;
      color: var(--sage); text-align: center; margin-top: 0.625rem;
    }

    /* Body */
    .page-body { padding: 4rem 0 5rem; }
    .intro { margin-bottom: 3rem; }
    .intro p + p { margin-top: 1.125rem; }

    /* Accent rule */
    .section-rule { width: 40px; height: 3px; background: var(--sage); border-radius: 2px; margin: 2.5rem 0; }

    /* Audio cards */
    .audio-section { margin-bottom: 2.5rem; }
    .audio-section h2 { margin-bottom: 1.5rem; }
    .audio-card {
      background: var(--cream); border: 1px solid var(--border);
      border-radius: 10px; padding: 1.5rem 1.75rem; margin-bottom: 1rem;
    }
    .audio-card__label {
      font-size: 0.75rem; font-weight: 600;
      letter-spacing: 0.1em; text-transform: uppercase;
      color: var(--sage); margin-bottom: 0.5rem;
    }
    .audio-card__title  { font-size: 1rem; font-weight: 600; color: var(--forest); margin-bottom: 0.875rem; }
    .audio-card audio   { width: 100%; border-radius: 6px; }
    .audio-card__note   { font-size: 0.875rem; color: var(--sage-mid); margin-top: 0.625rem; line-height: 1.6; }
    .audio-card--alt    { background: var(--white); border-color: var(--sage); }
    .audio-or {
      text-align: center; font-size: 0.875rem; font-weight: 600;
      color: var(--sage); letter-spacing: 0.05em; text-transform: uppercase; margin: 0.5rem 0;
    }

    /* Evening practice block (some days) */
    .evening-section {
      background: var(--cream); border: 1px solid var(--border);
      border-radius: 10px; padding: 1.75rem 2rem; margin-bottom: 2.5rem;
    }
    .evening-section h2 { margin-bottom: 0.5rem; }
    .evening-section .evening-subtitle {
      font-size: 0.9375rem; color: var(--forest-mid);
      margin-bottom: 1.25rem; line-height: 1.6;
    }
    .evening-steps { list-style: none; margin: 1rem 0 0; }
    .evening-steps li {
      display: flex; align-items: flex-start; gap: 0.875rem;
      padding: 0.625rem 0; font-size: 1rem; color: var(--forest); line-height: 1.55;
    }
    .evening-steps li + li { border-top: 1px solid var(--border); }
    .evening-steps .step-num {
      flex-shrink: 0; width: 24px; height: 24px;
      background: var(--forest); color: var(--cream);
      border-radius: 50%; font-size: 0.75rem; font-weight: 700;
      display: flex; align-items: center; justify-content: center; margin-top: 0.125rem;
    }
    .evening-note {
      font-size: 0.9rem; color: var(--sage); font-style: italic;
      margin-top: 1rem; padding-top: 1rem;
      border-top: 1px solid var(--border); line-height: 1.65;
    }

    /* Day prev/next navigation */
    .day-nav { display: flex; align-items: center; justify-content: space-between; margin: 3rem 0 0; gap: 1rem; }
    .day-nav__prev {
      font-size: 0.9375rem; font-weight: 500; color: var(--sage);
      text-decoration: none; display: flex; align-items: center; gap: 0.375rem;
    }
    .day-nav__prev:hover { color: var(--forest); }

    /* CTA box */
    .cta-box { background: var(--forest); border-radius: 12px; padding: 2.5rem 2rem; text-align: center; margin-top: 4rem; }
    .cta-box h3 { font-family: var(--ff-display); color: var(--cream); font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem; }
    .cta-box p  { color: rgba(255,255,255,0.72); font-size: 1rem; line-height: 1.7; max-width: 500px; margin: 0 auto 1.5rem; }

    /* Responsive */
    @media (max-width: 700px) {
      .page-hero     { padding: 3rem 0 2.5rem; }
      .page-body     { padding: 3rem 0 4rem; }
      .audio-card    { padding: 1.25rem; }
      .evening-section { padding: 1.25rem; }
      .cta-box       { padding: 2rem 1.25rem; }
    }
    @media (max-width: 480px) {
      .container  { padding: 0 1.25rem; }
      .day-nav    { flex-direction: column-reverse; align-items: stretch; text-align: center; }
      .day-nav__prev { justify-content: center; }
    }
  </style>"""


def main():
    calm_dir = ROOT / 'calm-reset'
    targets = sorted(calm_dir.glob('day-*.html'))

    updated = 0
    for path in targets:
        text = path.read_text(encoding='utf-8')
        new_text = re.sub(
            r'  <style>.*?</style>',
            NEW_STYLE,
            text,
            count=1,
            flags=re.DOTALL
        )
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            updated += 1
            print(f'  Updated {path.name}')
        else:
            print(f'  SKIPPED {path.name} (no match)')

    print(f'\nDone: {updated}/{len(targets)} files updated')


if __name__ == '__main__':
    main()
