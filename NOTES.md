# HDB Service — Project Notes
*For Claude: read this file at the start of every session to get up to speed*

---

## Instructions for Claude — please read first

1. **Ask Jack for the date and time at the start of every session.** Say something like: *"What's today's date and time? I'll use it for the dev diary."* Don't assume or guess.

2. **At the end of every session**, before wrapping up, ask Jack for the date and time again so you have an accurate end time. Then add a dev diary entry to the Dev Diary section at the bottom of this file covering what was built or discussed in the session.

3. **Follow the end-of-session marker convention** (established in Session 3):
   - Write your dev diary entry below the prompt line at the bottom of the Dev Diary section
   - Then move the `<!-- END OF SESSION X -->` comment and the prompt line to sit *after* your entry
   - Update the session number in the marker to match your session
   - Do not edit anything above the most recent `<!-- END OF SESSION X -->` line

4. **Keep the dev diary human-readable and casual** — written as if Jack is describing what he did, not a technical changelog.

---

## What this project is

A prototype of a UK government digital benefit service, simulating PIP (Personal Independence Payment) but called **Health and Disability Benefit (HDB)**. Built in plain HTML files with a Google Sheet as a database backend.

The project has two audiences:
1. **Citizens** — applying for and managing their benefit claim
2. **Agents (DWP staff)** — case management tool for handling claims

---

## File structure

### HDB Service — `/Users/home/Desktop/HDB Service/`
GitHub repo: https://github.com/js8989/hdb-service
Live site: https://jacksdevdiary-hdbservice.netlify.app

- `index.html` — prototypes landing page (links to all 4 prototypes)
- `govuk_hdb_full_journey.html` — citizen-facing registration and application journey
- `govuk_hdb_agent_tool.html` — agent-facing case management tool
- `flow-map.html` — interactive visual flow map of all screens (zoom/pan)
- `govuk_component_showcase.html` — all 34 GOV.UK components for reference
- `screenshot_screens.py` — Python script to auto-generate PNG screenshots of every screen
- `screens/` — folder containing all PNG screenshots (auto-generated)
- `mockups/pip_mockups.html` — standalone HTML mockups for PIP case record and timeline designs
- `mockups/screenshot_mockups.py` — script to generate PNG mockups
- `mockups/PIP-Mockup-1-Case-Record.png` — mockup: case record page
- `mockups/PIP-Mockup-2-Timeline-Overview.png` — mockup: full case timeline (collapsed)
- `mockups/PIP-Mockup-3-Timeline-Drilled-In.png` — mockup: timeline with application journey expanded
- `Update Screens.command` — double-clickable file on Desktop to regenerate all screenshots
- `mockups/devlog_mockup.html` — original mockup for Jack's Dev Diary website

### My Website — `/Users/home/Desktop/My Website/`
GitHub repo: https://github.com/js8989/jacks-dev-diary
Live site: https://jacksdevdiary.netlify.app

- `index.html` — the live dev diary site

### Prototype password
All four HDB prototype pages are password protected. Password: `wijrebfgwirbgfirw!@£&£&^`

---

## Screen codes

### Registration journey (govuk_hdb_full_journey.html)
- RG-01 — Start page
- RG-02 — Your name
- RG-03 — Date of birth
- RG-04 — NI number
- RG-04a — No NI: 6 month rule explanation
- RG-04b — No NI: apply for one?
- RG-04c — NI application placeholder
- RG-04d — No NI: confirm understanding
- RG-05 — Home address (postcode lookup + address selection)
- RG-06 — Check your answers
- RG-07 — Application submitted (confirmation)
- RG-08 — Create account: prompt (optional)
- RG-09 — Create account: email
- RG-10 — Create account: password
- RG-11 — Create account: passkey
- RG-12 — Account created

### Agent tool (govuk_hdb_agent_tool.html)
- AT-01 — Agent login
- AT-02 — Agent home
- AT-03 — Search for citizen (by NI number)
- AT-04 — Claimant record

---

## Key design decisions made

### Address lookup (RG-05)
- User enters house number/name + postcode
- Fuzzy matching (case insensitive, partial match, whitespace trimmed)
- Returns radio button list of matching addresses
- If only one result, auto-selects it
- If no match → friendly error + manual entry option
- If postcode not in demo DB → goes straight to manual entry with fields pre-filled
- Demo postcodes: SW1A 1AA, E1 6AN, M1 1AE, B1 1BB, LS1 1BA, BS1 1TR
- Manual entry accepts any format (Flat 2/1, Ground Floor Flat, Rose Cottage etc.)
- Non-England postcodes are rejected

### Prototype bar
- Green bar (#00703c) at the bottom of every page footer
- Shows address lookup test data for demo purposes
- "🔧 Prototype only — address lookup test data: SW1A 1AA + house no. 14 | E1 6AN + Flat 2/1 | M1 1AE + 1"

### Account creation (RG-08 to RG-12)
- Optional after application submission
- Email + password + passkey (WebAuthn API — works on modern devices)
- Password strength indicator (Weak/Fair/Strong)
- Show/hide toggle on password fields
- Skip passkey option available

### Google Sheets integration
- Both files use the same Google Apps Script URL as database
- Full journey submits application data to sheet
- Agent tool reads from sheet by NI number search

---

## Case lifecycle — key domain knowledge

*This is based on how PIP works in real life, applied to HDB*

### Terminology hierarchy
```
Linked Journey  (top level — the whole case thread, e.g. "Linked Journey 1")
  └── Journey  (e.g. Application, Mandatory Reconsideration, Appeal, Award Review)
        └── Sub-journey  (e.g. Registration, Evidence submission, Assessment, Decision)
              └── Events  (individual dated things that happened)
```

### Case lifecycle
```
APPLICATION (Journey)
  → Decision: Awarded or Refused

If awarded:
AWARD — payments begin

AWARD REVIEW (Journey) — at review date
  → Decision: Re-awarded (cycles back) or Ended

Any decision (Application or Award Review) can trigger:
MANDATORY RECONSIDERATION (Journey)
  → Must be requested within ~4 weeks of decision
  → Deadline is soft — can be extended up to ~3 months with good reason
  → In practice any reason accepted (vulnerable people)
  → 3 types:
      - Eligibility MR — do I qualify at all?
      - Entitlement MR — what rate/component should I get?
      - Non-compliance MR — stopped due to not engaging (3 reasons:
          1. Didn't return form on time
          2. Missed 3 appointments
          3. Third reason TBC)
  → MR Decision: changed or upheld
  → Cannot MR an MR decision — must go to Appeal

APPEAL (Journey — exceptional)
  → Off the back of an MR decision only
  → During appeal, claimant CAN start a new application (Linked Journey 2)
  → Award payments CONTINUE during MR and appeal
  → If appeal successful: increased payments backdated to original decision date
  → If appeal negative but new app (LJ2) positive: new app continues, NO backdating
```

### Parallel journeys (Linked Journeys)
- Maximum 2 linked journeys simultaneously (confirmed — may revisit if appeal happens twice)
- Both are part of the same case
- Agent tool must show both clearly with their individual statuses
- Backdating rules differ depending on combination of outcomes

### Non-compliance decisions
Three reasons a non-compliance decision can be made:
1. Didn't return a form on time
2. Didn't attend an appointment 3 times
3. Third reason TBC (to confirm with colleagues)

---

## Agent tool — design direction

### Case record page (AT-04 evolving)
Sections planned:
1. **Claimant identity bar** — name, NI, DOB, age, case ref (persistent at top)
2. **Case status** — Linked Journey cards showing current state of each journey
3. **Personal details** — non-eligibility-affecting data
4. **Eligibility-relevant information** — conditions, components, employment etc.
5. **Links** to full timeline, decisions etc.

### Timeline design
- **Top level**: shows Journeys as collapsible rows with dates
- **Accordion open**: shows Sub-journeys with header labels, then Events within each
- Event types: Decision, Evidence, Contact, Admin (colour coded)
- Each event shows: date, type tag, description, link if applicable, agent initials
- "Award in payment" shown as a persistent banner when relevant
- Current journey highlighted in orange
- Future journeys shown greyed out

### Mockups status
Three PNG mockups created (in /mockups/ folder):
- Mockup 1: Case record — single column, Linked Journey cards, personal + eligibility sections
- Mockup 2: Full timeline collapsed — correct MR timing, payment banner, correct terminology
- Mockup 3: Timeline drilled in — application journey open with sub-journey headers and events

---

## Things still to do / discuss

- [ ] Claimant home / portal (citizen-facing account area)
- [ ] Save and continue functionality for forms (requires citizen login)
- [ ] Google Sheet evolution — multiple sheets, dummy data for different case positions
- [ ] Third non-compliance reason (confirm with colleagues)
- [ ] Whether a third linked journey is possible if appeal happens twice
- [ ] Dummy data / pre-populated cases for demo purposes
- [ ] RG-05 and other screen tweaks still to review
- [ ] Agent tool code updates to match the new mockup designs

---

## Tech setup

- Python 3.9 with Playwright installed (for screenshots)
- Playwright Chromium at: `/Users/home/Library/Caches/ms-playwright/`
- Run screenshots: `python3 "/Users/home/Desktop/HDB Service/screenshot_screens.py"`
- Or double-click "Update Screens.command" on Desktop
- Git configured, pushing to GitHub via web upload (no CLI auth set up)
- Node.js not installed
- Homebrew not installed

---

## Style guide

- GOV.UK design system throughout (citizen-facing)
- Agent tool: dark blue header (#003078), blue border (#1d70b8), staff banner
- Citizen journey: black header (#0b0c0c), GOV.UK green buttons (#00703c)
- Font: Noto Sans
- All screens follow GOV.UK patterns: error messages in red, focus yellow, etc.

---

## Dev diary

*A human-readable log of what we built each session. Will eventually become a small website (devlog_mockup.html has the design).*

---

**Session 1** — *Friday, 5 June 2026*
The big founding session — everything before 16 June. Started the project from scratch. Built two core HTML files: a citizen-facing registration journey (`govuk_hdb_full_journey.html`, 17 screens RG-01 to RG-12) and an agent-facing case management tool (`govuk_hdb_agent_tool.html`). Both styled in the GOV.UK design system. Connected a Google Sheet via Google Apps Script as a lightweight database backend. Set up a GitHub repo. Built an automated Python/Playwright screenshot pipeline with a double-clickable Desktop shortcut to regenerate all PNGs in one go. Introduced screen codes (RG-xx, AT-xx). Built an interactive zoom/pan flow map of all 20 screens with dynamically drawn arrows. Redesigned the address page (RG-05) with postcode + house number lookup, fuzzy matching, and radio button selection. Added an optional account creation flow (RG-08 to RG-12) with email, password, and passkey. Added a green prototype bar to every page footer. Had a deep dive into the full PIP case lifecycle — established the Linked Journey / Journey / Sub-journey / Events terminology hierarchy. Created 3 PNG mockups for a new agent tool case record and timeline design. Ran out of context window and created this NOTES.md to carry knowledge forward.

---

**Session 2** — *6 June & 8 June 2026*
Explored GOV.UK design system compliance for the agent tool mockups. Introduced mockup versioning (v0.x = iteration, v1.0 = final). Built v0.2 with proper GOV.UK components. Built a `govuk_component_showcase.html` reference file showing all 34 GOV.UK components. Scanned DWP, HMRC, MOJ, Home Office and 8 other UK government design systems — found cross-govt precedent for all our custom patterns (DWP Timeline, MOJ Identity Bar etc.). Built v0.3 using only standard components — felt too weak visually. Agreed v0.4 will be a compromise: v0.2 visual design justified by cross-govt precedent rather than replaced by it. Also created the Dev Diary concept and designed `devlog_mockup.html`.

Key decisions:
- Custom components are justifiable by cross-govt precedent, not violations
- v0.4 = v0.2 design language + proper markup where possible

<!-- END OF SESSION 2 — do not edit above this line -->

---

**Session 3** — *16 June 2026, ~9pm–11pm*
Big session — took the dev diary from a mockup file to a real live website. Created a new GitHub repo (`jacks-dev-diary`) and a separate one for the HDB prototypes. Set up two Netlify sites: jacksdevdiary.netlify.app for the diary and jacksdevdiary-hdbservice.netlify.app for the prototypes. Built a prototypes landing page for the HDB site in the same dark style as the diary. Set up GitHub authentication so Claude can push directly from the Mac without any manual uploading. Tidied the diary entries — condensed 5 days down to 3, fixed all dates, removed the burger menu then brought it back properly with a working Prototypes link. Added password protection to all four prototype pages. Added a JDD favicon in the site colours to both sites. Also tidied NOTES.md to cover both repos in one place.

Key decisions:
- NOTES.md stays in the HDB Service folder and covers both projects
- jacks-dev-diary repo = the website; hdb-service repo = the prototypes
- Prototype password stored in NOTES.md (see File structure section above)

<!-- END OF SESSION 3 — do not edit above this line -->

---

*⬇ Next session: add your dev diary entry below this line, then move the end-of-session marker to after your entry.*

---
