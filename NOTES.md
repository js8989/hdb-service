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
Live site: https://js8989.github.io/hdb-service

- `index.html` — prototypes landing page (links to all 4 prototypes)
- `govuk_hdb_full_journey.html` — citizen-facing registration and application journey
- `govuk_hdb_agent_tool.html` — agent-facing case management tool
- `flow-map.html` — interactive visual flow map of all screens (zoom/pan)
- `govuk_component_showcase.html` — multi-org component showcase: 110+ components across GOV.UK, DWP, MOJ, NHS and DfE
- `dwp-frontend.css` — DWP Frontend CSS (compiled from SCSS via sass npm package, Session 4)
- `moj-frontend.css` — MOJ Frontend CSS (copied from npm package, Session 4)
- `nhs-frontend.css` — NHS Frontend CSS (copied from npm package, Session 4)
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
Live site: https://js8989.github.io/jacks-dev-diary

- `index.html` — the live dev diary site

### Prototype password
All four HDB prototype pages are password protected. Password: `hdb-proto-2026!*!`
Password is stored as a SHA-256 hash in the HTML files (not plain text).

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
- Git configured and authenticated with GitHub — Claude can push directly via CLI (set up in Session 3)
- Node.js installed (via .pkg installer from nodejs.org) — installed Session 4, June 2026
- npm available alongside Node.js
- sass npm package installed locally at `/tmp/dwp-pkg/node_modules/.bin/sass` — used to compile DWP SCSS into `dwp-frontend.css`
- MOJ Frontend CSS copied from npm package to `moj-frontend.css` (pre-compiled, no SCSS step needed)
- NHS Frontend CSS copied from npm package to `nhs-frontend.css` (pre-compiled, no SCSS step needed)
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

**Session 4** — *17 June 2026, ~5pm–8:38pm*
Long session with a lot covered across two main areas: password security and the component showcase.

**Password fix:** The prototype password protection was broken — pressing Cancel on the `prompt()` dialog or entering the wrong password was letting users straight through. Root cause was that the script ran before `<body>` existed in some files, so `document.body.innerHTML` replacement silently failed. Fixed across all three password-protected prototypes (`govuk_hdb_full_journey.html`, `govuk_hdb_agent_tool.html`, `flow-map.html`) using a new approach: SHA-256 hashed overlay div that covers the whole page, removed only on correct password. Hash of current password `hdb-proto-2026!*!` is `382ad70eaa9292d3ce5176937ac29276cef939415721417e9f639dfdb575b535`. The component showcase (`govuk_component_showcase.html`) has no password — it's a reference tool and doesn't need one.

**Hosting switch:** Netlify hit 75% of free-tier bandwidth credits, so switched both sites to GitHub Pages. Both repos (hdb-service and jacks-dev-diary) had to be made public for GitHub Pages to work on the free plan. URLs updated in `index.html` and `My Website/index.html`. GitHub Pages URLs: `https://js8989.github.io/hdb-service` and `https://js8989.github.io/jacks-dev-diary`.

**Component showcase expansion:** Expanded `govuk_component_showcase.html` from 34 GOV.UK components to 110+ across 5 orgs. Each org uses its own real CSS file. Added org-prefix codes (GOV-01, DWP-01, MOJ-01, NHS-01, DFE-01) and a sticky filter bar at the top to filter by org. Black label bars on all cards; white `border-bottom` on card labels to distinguish label from any black-background components.

Orgs added:
- **DWP** (DWP-01 to DWP-08): Uses `dwp-frontend.css` compiled from DWP's npm package SCSS via sass. 8 components: Header, Footer, Step nav, Pagination, Quick reference, Timeline (custom pattern), Task nav, Key details bar (retired).
- **MOJ** (MOJ-01 to MOJ-32): Uses `moj-frontend.css` (pre-compiled, from `@ministryofjustice/frontend` npm). 32 components including: Add another, Alert, Badge, Button menu, Card, Filter, Identity bar, Timeline, Pagination, Search, Side nav, Sortable table, Multi select, Date picker, Progress tracker, Sub nav, Ticket panel, Primary nav, Header, Modal dialog, Notification badge, Copy button, New features banner, Organisation switcher, Page header actions, Multi file upload, Messages, Scrollable pane, Interruption card, Timeout warning, API error, Numeric data.
- **NHS** (NHS-01 to NHS-33): Uses `nhs-frontend.css` (pre-compiled, from `nhsuk-frontend` npm). 33 components including: Action link, Back link, Breadcrumbs, Buttons, Card, Contents list, Details, Error message, Error summary, Expander, Footer, Header, Hint text, Images, Inset text, Panel, Radios, Skip link, Summary list, Table, Tabs, Tag, Task list, Checkboxes, Character count, Date input, Password input, Search input, Select, Text input, Textarea, Pagination, Warning callout.
- **DfE** (DFE-01 to DFE-03): No dedicated CSS file (DfE builds on GOV.UK Frontend). 3 components: Card, Filter, Header + vertical navigation.

Key technical notes for showcase:
- `crypto.subtle` (SHA-256) only works on HTTPS, not `file://` URLs — that's why showcase has no password (password overlay + crypto = grey screen on file:// because crypto fails silently and page never reveals)
- Headers and footers for all orgs written manually WITHOUT width container classes (no `govuk-width-container`, `nhsuk-width-container` etc.) to prevent overflow from card boundaries
- The `transform: scale(0.5)` trick was used for some wide GOV.UK components (GOV-07 cookie banner, GOV-15 footer) — works well but needs explicit height calculation
- MOJ components with no HTML in docs (skipped): Calendar, Feedback banner, Contextual date, Banner, Inset text
- NHS review date component is deprecated — skipped
- Minor visual glitches remain in some cards — noted for a future session to tidy

**Node.js install:** Installed Node.js via .pkg from nodejs.org so we could access npm packages for DWP/MOJ/NHS CSS. Had to install sass locally (not globally, to avoid sudo issues): `cd /tmp/dwp-pkg && npm install sass`.

**Known issues to fix next session:**
- Some component cards have minor visual glitches (Jack noted but didn't specify — review needed)
- DWP CSS may need updating if DWP Frontend releases a new version
- MOJ components: some JS-dependent ones (date picker, multi-select) won't be interactive without MOJ Frontend JS being loaded

**Evening continuation (~8pm–8:38pm):**
- Added a JDD nav bar (fixed, 36px, black #111) to all 4 prototype pages — left link goes to diary, right link goes back to prototypes landing. On the flow map, the existing blue toolbar was shifted down from top:0 to top:36px; viewport adjusted to top:88px. Filter bar in showcase changed from sticky top:0 to top:36px.
- Rewrote all 4 dev diary entries (Days 1–4) to sound more like Jack and less like a technical changelog.
- Removed all PIP / Personal Independence Payment references from user-facing pages — replaced with "health-based benefit" or "HDB" where needed.
- Removed all DWP references from user-facing pages: agent tool banner "DWP HDB Case Management" → "HDB Case Management"; NI number hint "letters from DWP or HMRC" → "letters from HMRC or other government departments"; landing page description updated.
- Split prototypes landing page (index.html) into two sections: "Prototypes" (registration journey + agent tool) and "Documentation" (flow map + component showcase).
- Custom domain discussion: buying a domain (~£10–15/yr from Namecheap/Google Domains) would enable a nicer URL. GitHub Pages supports custom domains for free once pointed. Alternative: rename jacks-dev-diary repo to `js8989.github.io` to serve diary at the root URL with no path (GitHub user site feature — only one repo can do this).

<!-- END OF SESSION 4 — do not edit above this line -->

---

*⬇ Next session: add your dev diary entry below this line, then move the end-of-session marker to after your entry.*

---

**Session 5** — *22 June 2026, ~5:43pm (Crete)*
Short planning session — no code written. Spent the session on a Miro board sketching out the layout for the new agent tool case record page (AT-04), building on the component shortlist discussed with Claude. The design brings together components from across the design systems into a cohesive page structure: MOJ-19 header at the top, then a dual service navigation (GOV-25) — one strip for main sections (Case record, Timeline, Documents, Notes) and one for sub-sections (Case overview, Personal details, Evidence and Documents, Tasks and Actions). Below that: breadcrumbs, a DWP Quick reference block for the claimant name and NI, and a MOJ badge row showing case status (Active / Suspended / In Progress / Closed / On Hold) plus flag indicators (SREL, Additional Support, Other Flag shown in red; grey "No flags" if none apply). Worked out a colour-coded status system for three separate status types — Award status (Purple = awaiting decision, Green = in award, Orange = not in award, Grey = archived), Dispute status (Green = accepted, Yellow = window open, Orange = in dispute, or none), and Change of Circs status (blue badge if active, or none). The main content area uses a GOV-1 accordion labelled "Live Cases (n)" containing a GOV-27 summary list for personal details and a Linked Journey card showing status + award in payment with timeline links. A right-hand panel shows key dates (date of claim, review date, dispute/change of circs dates) plus current award details and tasks. Archived cases hidden by default with a small blue expand arrow at the bottom.

<!-- END OF SESSION 5 — do not edit above this line -->

---

*⬇ Next session: add your dev diary entry below this line, then move the end-of-session marker to after your entry.*

---
