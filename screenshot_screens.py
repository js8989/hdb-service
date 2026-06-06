from playwright.sync_api import sync_playwright
import os, pathlib

BASE = pathlib.Path(__file__).parent
OUT  = BASE / "screens"
OUT.mkdir(exist_ok=True)

FULL_JOURNEY = (BASE / "govuk_hdb_full_journey.html").as_uri()
AGENT_TOOL   = (BASE / "govuk_hdb_agent_tool.html").as_uri()

# (code, label, file_url, page_id, js_setup)
SCREENS = [
    # --- Registration journey ---
    ("RG-01", "Start",                        FULL_JOURNEY, "page-start",          None),
    ("RG-02", "Your name",                    FULL_JOURNEY, "page-name",           None),
    ("RG-03", "Date of birth",                FULL_JOURNEY, "page-dob",            None),
    ("RG-04", "NI number",                    FULL_JOURNEY, "page-ni",             None),
    ("RG-04a","No NI – 6 month rule",         FULL_JOURNEY, "page-ni-sixmonth",    None),
    ("RG-04b","No NI – apply for one?",       FULL_JOURNEY, "page-ni-apply",       None),
    ("RG-04c","NI application placeholder",   FULL_JOURNEY, "page-ni-placeholder", None),
    ("RG-04d","No NI – confirm understanding",FULL_JOURNEY, "page-ni-confirm",     None),
    ("RG-05", "Home address",                 FULL_JOURNEY, "page-address",        None),
    ("RG-06", "Check your answers",           FULL_JOURNEY, "page-check",
        """
        document.getElementById('s-firstname').textContent = 'Jane';
        document.getElementById('s-surname').textContent   = 'Smith';
        document.getElementById('s-dob').textContent       = '14 March 1985';
        document.getElementById('s-age').textContent       = '39 years old';
        document.getElementById('s-ni').textContent        = 'AB 12 34 56 C';
        document.getElementById('s-address').textContent   = '12 Example Street\\nLondon\\nSW1A 1AA';
        """),
    ("RG-07", "Application submitted",        FULL_JOURNEY, "page-confirmation",
        "document.getElementById('conf-ref').textContent = 'HDB-482910';"),
    ("RG-08", "Create account – prompt",      FULL_JOURNEY, "page-account-prompt", None),
    ("RG-09", "Create account – email",       FULL_JOURNEY, "page-account-email",  None),
    ("RG-10", "Create account – password",    FULL_JOURNEY, "page-account-password",None),
    ("RG-11", "Create account – passkey",     FULL_JOURNEY, "page-account-passkey",None),
    ("RG-12", "Account created",              FULL_JOURNEY, "page-account-done",
        """
        document.getElementById('conf-email').textContent   = 'jane.smith@example.com';
        document.getElementById('conf-email-2').textContent = 'jane.smith@example.com';
        """),

    # --- Agent tool ---
    ("AT-01", "Agent login",          AGENT_TOOL, "agent-login",  None),
    ("AT-02", "Agent home",           AGENT_TOOL, "agent-home",
        """
        document.getElementById('home-username').textContent     = 'J.Smith';
        document.getElementById('header-username').textContent   = 'J.Smith';
        document.getElementById('banner-username').textContent   = 'Signed in as: j.smith — DWP HDB Case Management';
        """),
    ("AT-03", "Search for citizen",   AGENT_TOOL, "agent-search",
        """
        document.getElementById('header-username-2').textContent  = 'J.Smith';
        document.getElementById('banner-username-2').textContent  = 'Signed in as: j.smith — DWP HDB Case Management';
        """),
    ("AT-04", "Claimant record",      AGENT_TOOL, "agent-record",
        """
        document.getElementById('header-username-3').textContent  = 'J.Smith';
        document.getElementById('banner-username-3').textContent  = 'Signed in as: j.smith — DWP HDB Case Management';
        document.getElementById('record-name').textContent        = 'Jane Smith';
        document.getElementById('record-ni-display').textContent  = 'NI: AB 12 34 56 C';
        document.getElementById('r-firstname').textContent        = 'Jane';
        document.getElementById('r-surname').textContent          = 'Smith';
        document.getElementById('r-dob').textContent              = '14 March 1985';
        document.getElementById('r-age').textContent              = '39 years old';
        document.getElementById('r-ni').textContent               = 'AB 12 34 56 C';
        document.getElementById('r-ni-status').textContent        = 'provided';
        document.getElementById('r-address').textContent          = '12 Example Street\\nLondon\\nSW1A 1AA';
        document.getElementById('r-timestamp').textContent        = '4 June 2026 at 14:32';
        """),
]

def take_screenshot(page, code, label, file_url, page_id, js_setup):
    page.goto(file_url)
    page.evaluate(f"""
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById('{page_id}').classList.add('active');
    """)
    if js_setup:
        page.evaluate(js_setup)
    page.wait_for_timeout(300)
    filename = OUT / f"{code} – {label}.png"
    page.screenshot(path=str(filename), full_page=True)
    print(f"  ✓  {code}  {label}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    pg = context.new_page()
    print(f"\nSaving screenshots to: {OUT}\n")
    for (code, label, url, page_id, js) in SCREENS:
        take_screenshot(pg, code, label, url, page_id, js)
    browser.close()
    print(f"\nDone — {len(SCREENS)} screens saved to /screens/")
