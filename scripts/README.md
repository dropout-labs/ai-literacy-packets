# Build pipeline

This directory holds the build scripts that turn the markdown source
into print-ready PDFs.

## What gets built

| Artifact | Source | Purpose |
|---|---|---|
| `build/en.pdf` | `workbook/en/*.md` | English-only edition |
| `build/es.pdf` | `workbook/es/*.md` | Spanish-only edition |
| `build/bilingual.pdf` | interleaved en/es | The actual print product — facing pages |

## Local build

Requirements:
- Python 3.10+
- Google Chrome OR Chromium installed somewhere the script can find it

```bash
python3 scripts/build.py
```

Output goes to `build/`. Run `--help` for flags:
- `--check` validates spread count without building
- `--html` keeps intermediate HTML files for inspection

## CI build

`.github/workflows/build.yml` runs on every push to `main`, every PR
that touches `workbook/`, and every tag that starts with `v`. On tag
push, the workflow attaches the three PDFs to the corresponding
GitHub Release.

## Print spec

| Field | Value |
|---|---|
| Trim size | 8.5" × 11" (US Letter) |
| Bleed | 0.125" all sides |
| Margins | 0.5" top/bottom, 0.6" left/right |
| Body type | 11pt serif, 1.5 line-height |
| Body color | dark charcoal (#0e1116) on cream paper (#fdfdfb) |
| Accent | terracotta (#d04a2a) |
| Bind | saddle-stitch (2 staples on spine) |

See `partners/print-spec.md` for full vendor spec.

## Known limitations (as of v1.0)

- Some content-dense spreads currently overflow to a second printed
  page (en: 32 pp vs. 16-spread target; es: 34 pp; bilingual: 65 pp
  vs. 32-spread target). Editorial pass + designer layout in v1.1
  to hit the 16-spread target precisely.
- No real illustrations yet — placeholder ASCII boxes where
  illustrations should go. Illustrator engagement in v1.1.
- Body font falls back to Georgia if Source Serif Pro is not
  installed locally. CI uses DejaVu serif fallback.
