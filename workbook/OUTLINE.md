# v0.1 — Outline & Activity Inventory

> Status: **v0.1 outline complete** · target Jun 2026 · published May 2026

This document defines the scope, structure, and pedagogical commitments of the bilingual AI Literacy Packet before any content is written. It is the contract everything downstream is held to.

---

## 1. Audience

- **Primary**: youth ages 12–18 in underserved Santa Barbara County communities, with primary languages English or Spanish (often bilingual in the home)
- **Secondary**: parents, older siblings, and family members who pick up the packet alongside the youth
- **Tertiary**: librarians, school counselors, and partner-site staff who steward distribution

The packet is designed so a 12-year-old can finish it without help, and a 17-year-old does not feel talked down to. Reading level target: **6th grade Lexile range (~850–950L)** in English, with parallel readability in Spanish.

## 2. Pedagogical commitments

These are non-negotiable. Every page is held to all of them.

1. **Bilingual on facing pages.** English on the left page, Spanish on the right page, every spread, identical content. The Spanish edition is not a translation appendix; it is a peer.
2. **Works without WiFi or a teacher.** A young person at a kitchen table with a pencil can complete the packet end to end. Optional QR-code companions extend the work but are never required.
3. **Asks more than it tells.** Each spread leads with a question or scenario, not a definition. Definitions show up after the youth has already started reasoning about the thing.
4. **Project-based.** The packet produces an artifact (a written reflection, a labeled sketch, a worked-through example) the youth can keep, share, or photograph.
5. **No gatekeeping.** No vocabulary is used without being explained in plain language. No prior tech background is assumed.
6. **Honest about AI.** We do not hype. We do not catastrophize. We name what AI is good at, bad at, and dangerous at, with examples.
7. **Family-inclusive.** A parent or older sibling can engage with the packet alongside the youth without feeling excluded.

## 3. Page count and layout

- **Target spread count**: 16 spreads (32 printed pages, English-left/Spanish-right facing)
- **Trim size**: 8.5" × 11" (US Letter) for low-cost local printing
- **Bleed**: 0.125" all sides
- **Bind**: saddle-stitch (2 staples on the spine)
- **Cover**: card stock (80–100 lb), interior pages standard 60–70 lb book paper

## 4. Spread-level outline (16 spreads)

| # | Spread title | Section | Content type |
|---|---|---|---|
| 1 | Cover | Front matter | Title, art, "yours to keep" line |
| 2 | Welcome / Bienvenida | Front matter | Letter to the reader, how to use this packet |
| 3 | Where AI already is in your life | Part 1: What is AI? | Scenario inventory |
| 4 | Patterns: what AI is actually doing | Part 1: What is AI? | Concept + worked example |
| 5 | Activity: Sort by feature | Part 1: What is AI? | Unplugged activity (paper sort) |
| 6 | Data is what AI eats | Part 2: How does it work? | Concept + worked example |
| 7 | Where data comes from (and what's left out) | Part 2: How does it work? | Concept + reflection |
| 8 | Activity: Build a tiny dataset | Part 2: How does it work? | Unplugged activity |
| 9 | Prompts: how to ask AI for what you want | Part 3: How to use it well | Concept + practice |
| 10 | Activity: Prompt redesign | Part 3: How to use it well | Unplugged activity |
| 11 | When to trust AI, when to double-check | Part 3: How to use it well | Decision rubric |
| 12 | When AI is wrong: hallucinations & bias | Part 4: When it's wrong | Concept + examples |
| 13 | Activity: Spot the AI | Part 4: When it's wrong | Unplugged activity |
| 14 | When AI is dangerous: deepfakes, scams, manipulation | Part 4: When it's wrong | Concept + safety guide |
| 15 | Family conversation guide | Back matter | Discussion prompts |
| 16 | Reflection + what's next + back-cover credits | Back matter | Reflection + reprint info |

## 5. Activity inventory (5 unplugged, paper-only)

Each activity is fully detailed in `activities/`. All five are designed to:
- be completable with a pencil and the packet itself
- take 10–20 minutes each
- produce a tangible output the youth can keep
- work in either English or Spanish without translation overhead

| ID | Activity | Spread | Time | Skill |
|---|---|---|---|---|
| A1 | Sort by feature | 5 | 10 min | Pattern recognition; what "features" are |
| A2 | Build a tiny dataset | 8 | 15 min | Where data comes from; what's missing |
| A3 | Prompt redesign | 10 | 15 min | Asking AI clearly; iterating |
| A4 | Spot the AI | 13 | 20 min | Recognizing AI-generated content |
| A5 | Family conversation guide | 15 | open-ended | Talking with family about AI |

## 6. Visual & illustration commitments

- **Low text density** — no spread is more than 60% text by area
- **High-contrast typography** — minimum 11pt body, dark ink on cream background
- **Hand-drawn or warm-illustrated**, not stock-photo or corporate
- **Skin-tone diversity** in any depicted humans; default toward Latine/Hispanic representation given primary audience
- **Spanish typography matches English typography exactly** — same font, same hierarchy, same emphasis. Do not visually demote Spanish.

## 7. Accessibility floor

- 11pt minimum body text
- Reading level audit: Flesch-Kincaid grade 6 max for English; equivalent CEFR B1 for Spanish
- Color contrast minimum 4.5:1 (WCAG AA)
- No information conveyed by color alone
- All QR codes paired with the underlying URL printed in plain text
- Sans-serif body font; sufficient line-height (≥1.4)

## 8. Open-source release plan

- Source files (markdown + assets) → `github.com/dropout-labs/ai-literacy-packets`
- Print-ready PDFs → GitHub Releases at v1.0
- Both English-only and bilingual editions published as separate PDFs (some partners may want English-only or Spanish-only)
- Each release tagged: `v0.1`, `v0.5`, `v0.9`, `v1.0`

## 9. Versioning policy

- **v0.1** — outline + activity inventory (this document)
- **v0.5** — English content draft, 16 spreads
- **v0.9** — bilingual draft, Spanish marked `needs-validation` until a paid community translator validates register
- **v1.0** — bilingual final, paid translator validation complete, accessibility audit complete, print-ready PDFs published

## 10. What v0.1 explicitly does NOT yet contain

- Actual workbook content (lands in v0.5)
- Spanish text (lands in v0.9)
- Final illustrations (lands in v1.0)
- Print-ready PDFs (lands in v1.0)
- Validated translator engagement (lands in v0.9 → v1.0)

This is by design. v0.1 is the spec. Everything else is built against it.
