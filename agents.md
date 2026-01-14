# agents.md — Lemonade Project Contract

This file is the authoritative contract for all agent behavior in this repository.
All agents MUST read and obey this file before performing any work.

---

## Project Identity

- **Repo**: Lemonade
- **CLI Command**: `lemonade`
- **Purpose**: Local CLI tool for generating Etsy listing drafts and Pinterest copy from product photos, with optional browser automation to create Etsy draft listings.
- **Type**: PRIVATE internal execution tool (not SaaS)

---

## Brand Voice

- **Shop Brand**: Trésor Tendance
- **Language**: English only
- **Tone**: Calm, human, professional (not salesy)
- **Audience**: US + EU, age 40+
- **Emojis**: NEVER use emojis or emoticons anywhere

---

## Architecture Layers (STRICT SEPARATION)

### Layer 1 — CORE GENERATION (Safe)

Location: `lemonade/core/`

Responsibilities:
- Read product photo folders from INBOX
- Use OpenAI API for image understanding and text generation
- Generate Etsy listing text, Pinterest copy, and metadata
- Output files to disk (READY folder)
- NEVER interact with Etsy or any browser

Constraints:
- Must work independently even if browser automation is disabled or broken
- No network calls except OpenAI API
- No browser dependencies

### Layer 2 — BROWSER DRIVER (Isolated)

Location: `lemonade/browser/`

Responsibilities:
- Use Playwright with Chromium (non-headless only)
- Automate Etsy draft listing creation
- Upload photos, fill fields, save as DRAFT
- Take screenshots at every major step
- Support pause before final save

Constraints:
- NEVER click Publish
- NEVER auto-publish listings
- Human-like delays between actions
- Persistent browser profile (no passwords in code)
- Can be completely disabled without affecting Layer 1

---

## Queue Structure

Base path: `C:\tresor\etsy\queue\`

```
INBOX\      — Product folders awaiting processing
READY\      — Processed, ready for review
TODAY\      — Current item being worked on
DRAFTED\    — Successfully saved as draft on Etsy
PUBLISHED\  — Manually published (tracked for reference)
```

Each product = ONE folder containing 5-12 JPG/PNG photos of ONE product.

---

## CLI Commands

### Core Generation (Safe)
- `lemonade etsy prep` — Process INBOX, generate drafts to READY
- `lemonade etsy today` — Move next READY item to TODAY, print listing

### Browser Automation (Isolated)
- `lemonade etsy draft` — Create Etsy draft via browser automation
- `lemonade etsy pause` — Open browser, stop before Save Draft
- `lemonade etsy screenshots` — Store timestamped screenshots per step

### Safety / Inspection
- `lemonade etsy dry-run` — Show what would be uploaded (no browser)
- `lemonade etsy status` — Show queue counts

---

## Output Files Per Product

Each READY product folder contains:

1. **listing.md** — Etsy listing content in strict order:
   - A) TITLE (no emojis)
   - B) DESCRIPTION (English, calm, evocative)
   - C) SHIPPING INFORMATION (fixed text)
   - D) PRICE ADVICE
   - E) RECOMMENDED SHIPPING PROFILE
   - F) 13 ETSY TAGS
   - G) ETSY LISTING SETTINGS

2. **pinterest.txt** — Pinterest title and description (rewritten, not copied)

3. **metadata.json** — Machine-readable metadata including:
   - product_folder_name
   - generated_at (ISO timestamp)
   - detected_item_type
   - estimated_weight_with_packaging_kg
   - is_books (boolean)
   - recommended_shipping_profile
   - assumptions_or_notes

---

## Shipping Profile Rules

| Condition | Profile |
|-----------|---------|
| Item is books or set of books | BOOKS – Incremental per item |
| Estimated weight > 2.0 kg | HEAVY ITEMS – Flat Rate |
| Otherwise | STANDARD – Flat Rate |

---

## Fixed Shipping Information Text

Always include exactly:

```
Shipping Information

This item will be carefully packaged and shipped with tracking.
Combined shipping is always possible. Please feel free to contact me before purchasing if you have any questions.
```

---

## Technical Requirements

- Python 3.11+
- Minimal dependencies
- OpenAI API via `OPENAI_API_KEY` environment variable
- Playwright with Chromium only
- Persistent browser profile stored locally
- Clear logging to terminal
- Fail loudly, never silently

---

## Working Style

- Agent writes code
- Human runs commands and observes output
- Prefer boring, explicit solutions over clever ones
- Explain only when needed
- Always provide exact commands to type
- Pause and wait for confirmation at major steps

---

## Forbidden Actions

- NEVER use Etsy API
- NEVER auto-publish listings
- NEVER click Publish button
- NEVER store passwords in code
- NEVER use emojis
- NEVER proceed without confirmation at major steps

---

## File Patterns

Agents may edit:
- `*.py` — Python source files
- `*.md` — Documentation and listing files
- `*.json` — Configuration and metadata
- `*.txt` — Text output files
- `*.toml` — Python project configuration

Agents must NOT edit:
- `.env` files (contain secrets)
- Browser profile data
- User photos

---

*Last updated: 2026-01-14*
