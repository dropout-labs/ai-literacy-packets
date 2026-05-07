#!/usr/bin/env python3
"""build.py — DROPOUT Labs AI Literacy Packets build pipeline.

Reads markdown spreads from workbook/en/ and workbook/es/, renders to
print-ready PDFs at US Letter (8.5" × 11"), 0.125" bleed, saddle-stitch
imposable. Three artifacts:

    build/en.pdf          — English-only edition (16 pages)
    build/es.pdf          — Spanish-only edition (16 pages)
    build/bilingual.pdf   — Interleaved en/es facing pages (32 pages)

Toolchain: Python stdlib + Playwright headless Chromium (already on system
via browser-use). No LaTeX, no Pandoc, no system installs required.

Usage:
    python3 scripts/build.py            # build all three PDFs
    python3 scripts/build.py --html     # also keep intermediate HTML
    python3 scripts/build.py --check    # lint markdown + verify spread count
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_DIR = ROOT / "workbook" / "en"
ES_DIR = ROOT / "workbook" / "es"
BUILD_DIR = ROOT / "build"

# Print spec — US Letter trim, 0.125" bleed all sides, saddle-stitch
PAGE_CSS = """
@page {
    size: 8.5in 11in;
    margin: 0.5in 0.6in;
    bleed: 0.125in;
    marks: crop cross;
}
:root {
    --ink: #0e1116;
    --paper: #fdfdfb;
    --accent: #d04a2a;
    --muted: #5b6470;
    --rule: rgba(14,17,22,0.12);
}
* { box-sizing: border-box; }
html, body {
    margin: 0;
    padding: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: 'Source Serif Pro', Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}
.spread {
    page-break-after: always;
    padding-top: 0;
}
.spread:last-child { page-break-after: auto; }
.lang-marker {
    position: running(langmarker);
    font-size: 8pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    font-weight: 700;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
@page { @top-right { content: element(langmarker); } }
h1 {
    font-size: 26pt;
    line-height: 1.05;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin: 0 0 0.6em;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--ink);
}
h2 {
    font-size: 14pt;
    margin: 1.2em 0 0.4em;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--ink);
}
h3 {
    font-size: 12pt;
    margin: 1em 0 0.3em;
    color: var(--accent);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
p { margin: 0 0 0.7em; }
ul, ol { margin: 0 0 0.8em 1.2em; padding: 0; }
li { margin: 0.1em 0; }
blockquote {
    margin: 0.8em 0;
    padding: 0.5em 0.9em;
    border-left: 3px solid var(--accent);
    background: rgba(208,74,42,0.04);
    font-style: italic;
    color: var(--ink);
}
code {
    font-family: 'JetBrains Mono', 'Source Code Pro', Menlo, monospace;
    font-size: 9.5pt;
    background: rgba(0,0,0,0.04);
    padding: 0.05em 0.3em;
    border-radius: 2px;
}
pre {
    font-family: 'JetBrains Mono', 'Source Code Pro', Menlo, monospace;
    font-size: 9pt;
    line-height: 1.4;
    background: rgba(0,0,0,0.04);
    border-radius: 4px;
    padding: 0.7em 0.9em;
    overflow-x: auto;
    page-break-inside: avoid;
}
hr {
    border: 0;
    border-top: 1px solid var(--rule);
    margin: 1em 0;
}
.spread-num {
    font-size: 9pt;
    color: var(--muted);
    margin-bottom: 0.2em;
    letter-spacing: 0.06em;
}
.activity-box {
    border: 2px solid var(--accent);
    border-radius: 6px;
    padding: 0.8em 1em;
    margin: 0.8em 0;
    page-break-inside: avoid;
}
"""

HTML_SHELL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="lang-marker">{lang_label}</div>
{body}
</body>
</html>
"""


def collect_spreads(directory: Path) -> list[Path]:
    files = sorted(p for p in directory.iterdir()
                   if p.suffix == ".md" and re.match(r"^\d{2}-", p.name))
    return files


def md_to_html(md_text: str) -> str:
    """Minimal markdown → HTML. Stdlib-only. Handles the subset our spreads use."""
    out_lines: list[str] = []
    in_code = False
    in_list = False
    list_buffer: list[str] = []

    def flush_list():
        nonlocal in_list
        if in_list:
            out_lines.append("<ul>")
            out_lines.extend(list_buffer)
            out_lines.append("</ul>")
            list_buffer.clear()
            in_list = False

    for raw in md_text.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            flush_list()
            if in_code:
                out_lines.append("</pre>")
                in_code = False
            else:
                out_lines.append("<pre>")
                in_code = True
            continue
        if in_code:
            out_lines.append(_html_escape(line))
            continue
        if not line.strip():
            flush_list()
            out_lines.append("")
            continue
        if line.startswith("# "):
            flush_list()
            out_lines.append(f"<h1>{_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            flush_list()
            out_lines.append(f"<h2>{_inline(line[3:])}</h2>")
        elif line.startswith("### "):
            flush_list()
            out_lines.append(f"<h3>{_inline(line[4:])}</h3>")
        elif line.startswith("> "):
            flush_list()
            out_lines.append(f"<blockquote>{_inline(line[2:])}</blockquote>")
        elif line.startswith("- ") or line.startswith("* "):
            list_buffer.append(f"<li>{_inline(line[2:])}</li>")
            in_list = True
        elif line.startswith("---"):
            flush_list()
            out_lines.append("<hr>")
        else:
            flush_list()
            out_lines.append(f"<p>{_inline(line)}</p>")
    flush_list()
    if in_code:
        out_lines.append("</pre>")
    return "\n".join(out_lines)


def _inline(text: str) -> str:
    text = _html_escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def _html_escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def build_html(spreads: list[Path], lang: str, title: str) -> str:
    lang_labels = {"en": "DROPOUT LABS · EN", "es": "DROPOUT LABS · ES",
                   "bi": "DROPOUT LABS · BILINGUAL"}
    body_parts = []
    for i, p in enumerate(spreads, 1):
        md = p.read_text(encoding="utf-8")
        # Strip frontmatter-style "> Status: ..." blockquotes that are author notes
        md = re.sub(r"^> ⚠️ \*\*needs-validation\*\*.*?\n", "", md, flags=re.M)
        body_parts.append(
            f'<div class="spread"><div class="spread-num">spread {i:02d} of {len(spreads):02d}</div>\n'
            + md_to_html(md)
            + "</div>"
        )
    return HTML_SHELL.format(
        lang=lang.split("-")[0] if "-" in lang else lang,
        title=title,
        css=PAGE_CSS,
        lang_label=lang_labels.get(lang, lang.upper()),
        body="\n".join(body_parts),
    )


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    """Render HTML → PDF via headless Chromium (Playwright's chromium binary)."""
    # Find a chromium/chrome binary
    candidates = [
        Path.home() / ".cache/ms-playwright/chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    ]
    chrome = None
    for c in candidates:
        if "*" in str(c):
            matches = list(c.parent.parent.glob(c.parent.parent.name + "/" + c.name)) if False else \
                      sorted(c.parent.parent.parent.glob(c.parent.parent.name + "/" + c.parent.name + "/" + c.name))
            if matches:
                chrome = matches[0]
                break
        elif c.exists():
            chrome = c
            break
    # Simpler glob fallback:
    if chrome is None:
        for m in (Path.home() / ".cache/ms-playwright").glob("chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium"):
            chrome = m
            break
    if chrome is None:
        for m in (Path.home() / ".cache/ms-playwright").glob("chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium"):
            chrome = m
            break
    if chrome is None or not Path(chrome).exists():
        raise RuntimeError(
            "No Chromium binary found. Install via: pip install playwright && playwright install chromium"
        )
    cmd = [
        str(chrome),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path.resolve()}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"chrome failed: {result.stderr[-500:]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", action="store_true", help="Keep intermediate HTML")
    parser.add_argument("--check", action="store_true", help="Validate, don't build")
    args = parser.parse_args()

    en_spreads = collect_spreads(EN_DIR)
    es_spreads = collect_spreads(ES_DIR)

    print(f"  English spreads: {len(en_spreads)}")
    print(f"  Spanish spreads: {len(es_spreads)}")

    if len(en_spreads) != 16:
        print(f"  ✗ Expected 16 English spreads, got {len(en_spreads)}", file=sys.stderr)
        return 1
    if len(es_spreads) != 16:
        print(f"  ✗ Expected 16 Spanish spreads, got {len(es_spreads)}", file=sys.stderr)
        return 1
    print("  ✓ Spread count OK")

    if args.check:
        return 0

    BUILD_DIR.mkdir(exist_ok=True)

    # English-only PDF
    en_html = BUILD_DIR / "en.html"
    en_pdf = BUILD_DIR / "en.pdf"
    en_html.write_text(build_html(en_spreads, "en", "AI Literacy Packet · English"), encoding="utf-8")
    render_pdf(en_html, en_pdf)
    print(f"  ✓ {en_pdf.name} ({en_pdf.stat().st_size // 1024} KB)")

    # Spanish-only PDF
    es_html = BUILD_DIR / "es.html"
    es_pdf = BUILD_DIR / "es.pdf"
    es_html.write_text(build_html(es_spreads, "es", "Cuaderno de IA · Español"), encoding="utf-8")
    render_pdf(es_html, es_pdf)
    print(f"  ✓ {es_pdf.name} ({es_pdf.stat().st_size // 1024} KB)")

    # Bilingual interleaved PDF — facing pages: en1, es1, en2, es2, ...
    bi_spreads: list[Path] = []
    for en, es in zip(en_spreads, es_spreads):
        bi_spreads.extend([en, es])
    bi_html = BUILD_DIR / "bilingual.html"
    bi_pdf = BUILD_DIR / "bilingual.pdf"
    bi_html.write_text(build_html(bi_spreads, "bi", "AI Literacy Packet · Bilingual"), encoding="utf-8")
    render_pdf(bi_html, bi_pdf)
    print(f"  ✓ {bi_pdf.name} ({bi_pdf.stat().st_size // 1024} KB)")

    if not args.html:
        for h in (en_html, es_html, bi_html):
            h.unlink()

    return 0


if __name__ == "__main__":
    sys.exit(main())
