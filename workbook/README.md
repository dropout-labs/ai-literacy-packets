# Workbook source

This directory holds the source files for the printed bilingual workbook.

## Layout

```
workbook/
├── en/    # English source pages (page-by-page)
└── es/    # Spanish source pages (page-by-page, mirroring en/)
```

The workbook is designed for **facing-page bilingual layout**: every English page on the left has a Spanish page on the right covering identical content. This is intentional and non-negotiable. The Spanish edition is not a translation appendix; it is a peer.

## Status

Pre-v0.1 — outline pending. See repo root [README.md](../README.md) for milestone schedule.

## Planned structure (v1.0 target)

| Section | Pages | Topic |
|---|---|---|
| Front matter | 2 | Title, intro, family note, how to use |
| Part 1 | 6 | What is AI? (concrete examples in everyday life) |
| Part 2 | 6 | How does AI actually work? (data, patterns, prompts) |
| Part 3 | 6 | How do I use AI well? (questions to ask, tools to try) |
| Part 4 | 6 | When does AI get it wrong, and how do I notice? |
| Activities | 4 | Unplugged exercises (cross-references to `activities/`) |
| Back matter | 2 | Family conversation guide, QR codes, reprint instructions |

Total target: ~32 pages (16 English + 16 Spanish facing).
