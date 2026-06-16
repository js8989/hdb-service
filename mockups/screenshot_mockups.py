from playwright.sync_api import sync_playwright
import pathlib

BASE = pathlib.Path(__file__).parent
SRC  = (BASE / 'pip_mockups.html').as_uri()
OUT  = BASE

PAGES = [
    ('page-record',          'PIP-Mockup-1-Case-Record'),
    ('page-timeline',        'PIP-Mockup-2-Timeline-Overview'),
    ('page-timeline-detail', 'PIP-Mockup-3-Timeline-Drilled-In'),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1280, 'height': 900})
    page = context.new_page()
    print(f'\nSaving mockups to: {OUT}\n')
    for page_id, filename in PAGES:
        page.goto(SRC)
        page.evaluate(f"""
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById('{page_id}').classList.add('active');
        """)
        page.wait_for_timeout(300)
        out_path = OUT / f'{filename}.png'
        page.screenshot(path=str(out_path), full_page=True)
        print(f'  ✓  {filename}')
    browser.close()
    print(f'\nDone — 3 mockups saved.')
