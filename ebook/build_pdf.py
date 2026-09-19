#!/usr/bin/env python3
"""Build a colorful, image-rich, easy-to-read PDF e-book with real stock photos."""

from __future__ import annotations

import html
import re
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
MD_PATH = ROOT / "rotina-leve-familia-grande.md"
HTML_PATH = ROOT / "dist" / "ebook.html"
PDF_PATH = ROOT / "dist" / "Rotina-Leve-com-Familia-Grande.pdf"
STOCK = ROOT / "assets" / "stock"


def uri(name: str) -> str:
    return (STOCK / name).resolve().as_uri()


def esc(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def is_table_sep(line: str) -> bool:
    s = line.strip().strip("|").strip()
    return bool(s) and set(s.replace(":", "").replace("-", "").replace(" ", "").replace("|", "")) == set()


def parse_table(lines: list[str], start: int) -> tuple[str, int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        if not is_table_sep(lines[i]):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
        i += 1
    if not rows:
        return "", start
    header, body = rows[0], rows[1:]
    out = ['<div class="table-wrap"><table><thead><tr>']
    out.append("".join(f"<th>{esc(c)}</th>" for c in header))
    out.append("</tr></thead><tbody>")
    for row in body:
        while len(row) < len(header):
            row.append("")
        out.append("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row[: len(header)]) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out), i


def render_md(md: str, inject_after_h3: dict[str, str] | None = None) -> str:
    """Convert markdown chunk to HTML; optionally inject HTML after matching h3 titles."""
    inject_after_h3 = inject_after_h3 or {}
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_list = False
    list_tag = "ul"

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append(f"</{list_tag}>")
            in_list = False

    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            close_list()
            i += 1
            continue
        if stripped == "---":
            close_list()
            out.append('<div class="divider"><span></span><span></span><span></span></div>')
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
            close_list()
            table_html, i = parse_table(lines, i)
            out.append(table_html)
            continue
        if re.match(r"^#\s+", stripped) or re.match(r"^##\s+Capítulo", stripped):
            # skip top-level chapter titles — handled by wrappers
            if re.match(r"^#\s+Capítulo", stripped) or re.match(r"^##\s+Cozinha|^##\s+A casa|^##\s+Tempo|^##\s+Filhos|^##\s+Calma|^##\s+Conclus", stripped):
                i += 1
                # also skip following ### chapter subtitle if present as first ###
                continue
            if stripped.startswith("# "):
                close_list()
                out.append(f"<h2 class='section-h'>{esc(stripped[2:].strip())}</h2>")
                i += 1
                continue
        if stripped.startswith("#### "):
            close_list()
            out.append(f"<h4>{esc(stripped[5:].strip())}</h4>")
            i += 1
            continue
        if stripped.startswith("### "):
            close_list()
            text = stripped[4:].strip()
            # skip chapter subtitle lines that duplicate hero
            if text.startswith("Planejamento de refeições") or text.startswith("Organização de horários") or text.startswith("Gerenciamento de tempo") or text.startswith("Criação de autonomia") or text.startswith("Saúde mental"):
                i += 1
                continue
            cls = "h3"
            if any(text.startswith(x) for x in ("A dor", "A verdade", "A culpa", "O erro", "O caos")):
                cls = "eyebrow-title"
            elif "Checklist" in text or "checklist" in text:
                cls = "check-h"
            elif "Mini plano" in text:
                cls = "action-h"
            elif "Chamada para ação" in text:
                out.append(f'<div class="cta-panel"><h3>{esc(text)}</h3>')
                i += 1
                continue
            out.append(f'<h3 class="{cls}">{esc(text)}</h3>')
            for key, block in inject_after_h3.items():
                if key.lower() in text.lower():
                    out.append(block)
            i += 1
            continue
        if stripped.startswith("## "):
            close_list()
            text = stripped[3:].strip()
            if text.startswith("Índice") or text.startswith("Extras"):
                i += 1
                continue
            if text.startswith("Você não precisa"):
                out.append(f'<h3 class="soft-h">{esc(text)}</h3>')
            else:
                out.append(f"<h2>{esc(text)}</h2>")
            i += 1
            continue
        if stripped.startswith("> "):
            close_list()
            out.append(f'<blockquote class="quote">{esc(stripped[2:].strip())}</blockquote>')
            i += 1
            continue
        if re.match(r"^- \[[ xX]\] ", stripped):
            if not in_list or list_tag != "ul":
                close_list()
                out.append('<ul class="checklist">')
                in_list = True
                list_tag = "ul"
            item = re.sub(r"^- \[[ xX]\] ", "", stripped)
            out.append(f'<li><span class="box"></span><span>{esc(item)}</span></li>')
            i += 1
            continue
        if stripped.startswith("- "):
            if not in_list or list_tag != "ul":
                close_list()
                out.append('<ul class="bullets">')
                in_list = True
                list_tag = "ul"
            out.append(f"<li>{esc(stripped[2:])}</li>")
            i += 1
            continue
        if re.match(r"^\d+\.\s+", stripped):
            if not in_list or list_tag != "ol":
                close_list()
                out.append('<ol class="steps">')
                in_list = True
                list_tag = "ol"
            item = re.sub(r"^\d+\.\s+", "", stripped)
            out.append(f"<li>{esc(item)}</li>")
            i += 1
            continue
        close_list()
        if stripped.startswith("*Fim do") or stripped.startswith("*Coleção"):
            out.append(f'<p class="fine">{esc(stripped.strip("*"))}</p>')
        elif stripped.startswith(("**Dica", "**Regra", "**Frase", "**Meta", "**Permissão", "**Se você", "**Você não", "**1 prioridade")):
            out.append(f'<div class="tip">{esc(stripped)}</div>')
        else:
            out.append(f"<p>{esc(stripped)}</p>")
        i += 1
    close_list()
    return "\n".join(out)


def img_break(src: str, caption: str, tall: bool = False) -> str:
    cls = "photo-break tall" if tall else "photo-break"
    return f'''<figure class="{cls}">
  <img src="{uri(src)}" alt="{html.escape(caption)}" />
  <figcaption>{html.escape(caption)}</figcaption>
</figure>'''


def img_duo(src1: str, src2: str, c1: str, c2: str) -> str:
    return f'''<div class="duo">
  <figure><img src="{uri(src1)}" alt="{html.escape(c1)}" /><figcaption>{html.escape(c1)}</figcaption></figure>
  <figure><img src="{uri(src2)}" alt="{html.escape(c2)}" /><figcaption>{html.escape(c2)}</figcaption></figure>
</div>'''


def chapter_hero(num: int, title: str, subtitle: str, image: str, color: str) -> str:
    return f'''<section class="chapter" style="--accent:{color}">
  <div class="hero">
    <img src="{uri(image)}" alt="{html.escape(title)}" />
    <div class="hero-shade"></div>
    <div class="hero-copy">
      <span class="badge">Capítulo {num}</span>
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(subtitle)}</p>
    </div>
  </div>
  <div class="chapter-body">'''


CSS = r"""
:root {
  --ink: #1f2430;
  --muted: #5a6472;
  --paper: #fffdf9;
  --white: #ffffff;
  --coral: #ff6b57;
  --coral-soft: #ffe3de;
  --teal: #0f8f8a;
  --teal-deep: #0a6e6a;
  --teal-soft: #d8f3f1;
  --sun: #ffc857;
  --sun-soft: #fff3d6;
  --berry: #c44569;
  --berry-soft: #f8dce5;
  --sky: #3d8bfd;
  --line: #eadfd6;
}

@page {
  size: A4;
  margin: 14mm 12mm 16mm 12mm;
  @bottom-center {
    content: counter(page);
    font-family: "DejaVu Sans", sans-serif;
    font-size: 9pt;
    color: #5a6472;
  }
}
@page :first {
  margin: 0;
  @bottom-center { content: none; }
}

* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: "DejaVu Sans", sans-serif;
  font-size: 11.5pt;
  line-height: 1.62;
}
img { max-width: 100%; display: block; }
p { margin: 0 0 11px; }
strong { color: var(--teal-deep); }
h1,h2,h3,h4 {
  font-family: "DejaVu Serif", serif;
  line-height: 1.22;
  break-after: avoid;
  color: var(--teal-deep);
}
h2 { font-size: 18pt; margin: 18px 0 10px; }
h3 { font-size: 14pt; margin: 16px 0 8px; }
h4 { font-size: 12pt; margin: 12px 0 6px; color: var(--coral); }

/* COVER */
.cover {
  break-after: page;
  width: 210mm; height: 297mm;
  position: relative; overflow: hidden;
  background: #ff6b57;
}
.cover img.bg {
  position: absolute; top: 0; left: 0; right: 0;
  width: 210mm; height: 185mm;
  object-fit: cover;
}
.cover .veil {
  position: absolute; top: 0; left: 0; right: 0; height: 185mm;
  background: linear-gradient(180deg, rgba(255,107,87,0.15) 0%, rgba(15,143,138,0.2) 60%, rgba(31,36,48,0.35) 100%);
}
.cover .copy {
  position: absolute; left: 0; right: 0; bottom: 0;
  height: 125mm;
  padding: 14mm 15mm 16mm;
  color: white;
  background: linear-gradient(135deg, #0a6e6a 0%, #0f8f8a 40%, #3d8bfd 78%, #c44569 100%);
}
.cover .accent-bar {
  position: absolute; left: 0; right: 0; top: 182mm;
  height: 10px;
  background: linear-gradient(90deg, #ff6b57, #ffc857, #0f8f8a, #3d8bfd);
}
.pill {
  display: inline-block;
  background: var(--sun);
  color: #1f2430;
  font-size: 9pt;
  font-weight: 700;
  letter-spacing: .06em;
  text-transform: uppercase;
  padding: 8px 14px;
  margin-bottom: 12px;
}
.cover h1 {
  color: white;
  font-size: 30pt;
  margin: 0 0 10px;
  max-width: 12ch;
}
.cover .sub {
  font-size: 12.5pt;
  line-height: 1.45;
  max-width: 36ch;
  margin: 0 0 14px;
  color: #fff8f2;
}
.cover .meta {
  border-top: 3px solid var(--sun);
  padding-top: 12px;
  font-size: 11pt;
  max-width: 42ch;
  color: rgba(255,255,255,.96);
}

/* INTRO */
.intro-wrap { }
.intro-banner {
  background: linear-gradient(120deg, #0f8f8a, #3d8bfd 55%, #c44569);
  color: white;
  padding: 18px 16px;
  margin: 0 0 14px;
}
.intro-banner h2 { color: white; margin: 0; font-size: 22pt; }
.intro-banner p { margin: 6px 0 0; color: rgba(255,255,255,.95); font-size: 11pt; }
.lead {
  font-size: 13.5pt;
  background: var(--coral-soft);
  border-left: 8px solid var(--coral);
  padding: 14px 16px;
  margin: 0 0 14px;
  line-height: 1.55;
}
.highlight-box {
  background: linear-gradient(135deg, #fff3d6, #ffe3de);
  border: 3px solid var(--coral);
  padding: 14px 16px;
  margin: 14px 0;
}
.highlight-box p { margin: 0; font-size: 12.5pt; }
.promise {
  display: table;
  width: 100%;
  margin: 12px 0 16px;
  background: var(--teal-soft);
  border: 2px solid var(--teal);
}
.promise .cell {
  display: table-cell;
  width: 25%;
  padding: 12px 10px;
  vertical-align: top;
  border-right: 1px solid rgba(15,143,138,.25);
}
.promise .cell:last-child { border-right: none; }
.promise .n {
  display: inline-block;
  background: var(--teal);
  color: white;
  font-weight: 700;
  font-size: 10pt;
  padding: 3px 8px;
  margin-bottom: 6px;
}
.promise p { margin: 0; font-size: 10pt; color: var(--ink); }

/* TOC */
.toc { break-before: page; }
.toc h2 {
  background: var(--sun);
  display: inline-block;
  padding: 8px 14px;
  margin: 0 0 14px;
  color: #1f2430;
}
.toc-card {
  display: table;
  width: 100%;
  margin: 0 0 12px;
  background: white;
  border: 2px solid var(--line);
  overflow: hidden;
}
.toc-card .thumb {
  display: table-cell;
  width: 42%;
  vertical-align: top;
}
.toc-card .thumb img {
  width: 100%;
  height: 128px;
  object-fit: cover;
}
.toc-card .info {
  display: table-cell;
  vertical-align: middle;
  padding: 12px 14px;
}
.toc-card .num {
  display: inline-block;
  background: var(--coral);
  color: white;
  font-weight: 700;
  padding: 4px 10px;
  font-size: 10pt;
  margin-bottom: 6px;
}
.toc-card h3 { margin: 0 0 4px; font-size: 13pt; color: var(--ink); }
.toc-card p { margin: 0; font-size: 10pt; color: var(--muted); }

/* CHAPTER */
.chapter { break-before: page; --accent: var(--coral); }
.hero {
  position: relative;
  height: 250px;
  overflow: hidden;
  margin: 0 0 14px;
  background: #333;
}
.hero img {
  width: 100%;
  height: 250px;
  object-fit: cover;
}
.hero-shade {
  position: absolute; inset: 0;
  background: linear-gradient(100deg, rgba(20,24,32,.88) 0%, rgba(20,24,32,.45) 55%, rgba(20,24,32,.15) 100%);
}
.hero-copy {
  position: absolute; left: 0; right: 0; bottom: 0;
  padding: 16px 16px 14px;
  color: white;
}
.badge {
  display: inline-block;
  background: var(--accent);
  color: white;
  font-size: 9pt;
  font-weight: 700;
  letter-spacing: .05em;
  text-transform: uppercase;
  padding: 5px 11px;
  margin-bottom: 8px;
  font-family: "DejaVu Sans", sans-serif;
}
.hero-copy h1 {
  color: white;
  font-size: 20pt;
  margin: 0 0 4px;
}
.hero-copy p {
  margin: 0;
  color: rgba(255,255,255,.95);
  font-size: 11pt;
  max-width: 48ch;
  font-family: "DejaVu Sans", sans-serif;
}
.chapter-body { padding: 0 1mm 2mm; }
.chapter-body > *:last-child { margin-bottom: 0; }

.eyebrow-title {
  color: var(--coral);
  font-size: 15pt;
}
.check-h {
  background: var(--teal);
  color: white !important;
  display: inline-block;
  padding: 6px 12px;
}
.action-h {
  background: var(--sun);
  color: #1f2430 !important;
  display: inline-block;
  padding: 6px 12px;
}

.tip {
  background: var(--sun-soft);
  border: 2px solid var(--sun);
  border-left-width: 8px;
  padding: 12px 14px;
  margin: 12px 0;
  font-size: 11.2pt;
}
.quote {
  margin: 14px 0;
  padding: 14px 16px;
  background: linear-gradient(135deg, var(--berry-soft), var(--coral-soft));
  border-left: 8px solid var(--berry);
  font-family: "DejaVu Serif", serif;
  font-size: 13pt;
  color: #4a2030;
}
.bullets { margin: 0 0 12px; padding-left: 1.1em; }
.bullets li { margin-bottom: 5px; }
.bullets li::marker { color: var(--coral); font-weight: 700; }
.steps { margin: 0 0 12px; padding-left: 1.3em; }
.steps li { margin-bottom: 7px; padding-left: 4px; }
.steps li::marker { color: var(--teal); font-weight: 700; font-size: 1.05em; }

.checklist {
  list-style: none;
  margin: 10px 0 14px;
  padding: 12px 14px;
  background: white;
  border: 2px dashed var(--teal);
}
.checklist li {
  display: table;
  width: 100%;
  margin: 0 0 8px;
}
.checklist .box {
  display: table-cell;
  width: 16px;
  height: 16px;
  border: 2px solid var(--coral);
  background: #fff;
  vertical-align: top;
}
.checklist li > span:last-child {
  display: table-cell;
  padding-left: 10px;
  vertical-align: top;
}

.table-wrap {
  margin: 12px 0 16px;
  border: 2px solid var(--teal);
  overflow: hidden;
}
table { width: 100%; border-collapse: collapse; font-size: 10pt; }
th {
  background: var(--teal);
  color: white;
  text-align: left;
  padding: 9px 10px;
  font-family: "DejaVu Sans", sans-serif;
}
td {
  padding: 8px 10px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
  background: white;
}
tr:nth-child(even) td { background: var(--teal-soft); }

.photo-break {
  margin: 16px 0;
  break-inside: avoid;
}
.photo-break img {
  width: 100%;
  height: 210px;
  object-fit: cover;
  border-bottom: 8px solid var(--accent, var(--coral));
}
.photo-break.tall img { height: 250px; }
.photo-break figcaption,
.duo figcaption {
  font-size: 9pt;
  color: var(--muted);
  padding: 6px 2px 0;
  font-style: italic;
}
.duo {
  display: table;
  width: 100%;
  table-layout: fixed;
  margin: 14px 0 16px;
  break-inside: avoid;
}
.duo figure {
  display: table-cell;
  width: 50%;
  padding-right: 6px;
  margin: 0;
  vertical-align: top;
}
.duo figure:last-child { padding-right: 0; padding-left: 6px; }
.duo img {
  width: 100%;
  height: 165px;
  object-fit: cover;
  border-bottom: 6px solid var(--sun);
}

.color-strip {
  background: linear-gradient(90deg, var(--coral), var(--sun), var(--teal));
  height: 8px;
  margin: 8px 0 14px;
}
.divider {
  text-align: center;
  margin: 16px 0;
}
.divider span {
  display: inline-block;
  width: 10px; height: 10px;
  border-radius: 50%;
  margin: 0 4px;
  background: var(--coral);
}
.divider span:nth-child(2) { background: var(--sun); }
.divider span:nth-child(3) { background: var(--teal); }

.cta-panel {
  break-inside: avoid;
  background: linear-gradient(135deg, #0a6e6a, #3d8bfd 70%, #c44569);
  color: white;
  padding: 18px 16px;
  margin: 16px 0;
}
.cta-panel h3, .cta-panel strong { color: white !important; }
.cta-panel p, .cta-panel li { color: rgba(255,255,255,.96); }
.cta-panel .checklist {
  background: rgba(255,255,255,.12);
  border-color: rgba(255,255,255,.55);
}
.cta-panel .checklist .box { border-color: var(--sun); background: transparent; }

.extras { break-before: page; }
.extras-banner {
  background: var(--berry);
  color: white;
  padding: 16px;
  margin: 0 0 14px;
}
.extras-banner h2 { color: white; margin: 0; }
.fine {
  text-align: center;
  color: var(--muted);
  font-size: 9.5pt;
  margin-top: 18px;
  padding-top: 10px;
  border-top: 2px solid var(--line);
}
.soft-h { color: var(--berry); font-size: 14pt; }
.pad { padding: 0 1mm; }
.big-close {
  break-before: page;
}
.big-close .hero { height: 210px; }
.big-close .hero img { height: 210px; }
"""


def slice_md(md: str) -> dict[str, str]:
    def find(pat: str):
        return re.search(pat, md, re.M)

    intro_m = find(r"^##\s+Introdução\s*$")
    toc_m = find(r"^##\s+Índice")
    caps = {}
    for n in range(1, 6):
        caps[n] = find(rf"^#\s+Capítulo\s+{n}\s*$")
    conc = find(r"^#\s+Conclusão")
    extras = find(r"^##\s+Extras")

    intro = md[intro_m.start():toc_m.start()] if intro_m and toc_m else ""
    body = {}
    for n in range(1, 6):
        start = caps[n].start() if caps[n] else None
        if n < 5:
            end = caps[n + 1].start() if caps[n + 1] else None
        else:
            end = conc.start() if conc else None
        if start is not None and end is not None:
            body[n] = md[start:end]
        elif start is not None:
            body[n] = md[start:]
    conclusion = ""
    if conc:
        end = extras.start() if extras else len(md)
        conclusion = md[conc.start():end]
    extras_md = md[extras.start():] if extras else ""
    return {"intro": intro, "body": body, "conclusion": conclusion, "extras": extras_md}


def build_intro(intro_md: str) -> str:
    intro_md = re.sub(r"^##\s+Introdução\s*$", "", intro_md, count=1, flags=re.M)
    content = render_md(intro_md)
    content = re.sub(
        r"<p>(Se você abriu este e-book.+?)</p>",
        r'<div class="lead"><p>\1</p></div>',
        content,
        count=1,
    )
    # Insert a vivid photo early — right after the opening lead block
    early = img_break("cover-bright.jpg", "Você não está sozinha nessa rotina.")
    if '<div class="lead">' in content:
        content = content.replace("</div>", "</div>\n" + early, 1)
    else:
        content = early + content

    promises = """
    <div class="promise">
      <div class="cell"><span class="n">01</span><p>Menos decisões no automático</p></div>
      <div class="cell"><span class="n">02</span><p>Menos culpa no fim do dia</p></div>
      <div class="cell"><span class="n">03</span><p>Mais previsibilidade no caos</p></div>
      <div class="cell"><span class="n">04</span><p>Espaços reais de paz para você</p></div>
    </div>
    """
    closing = f'''
    <div class="highlight-box">
      <p><strong>Você não precisa ser perfeita. Você precisa de um caminho.</strong><br/>Vamos juntas?</p>
    </div>
    {img_duo("family.jpg", "coffee.jpg", "Rotina real em família", "Pequenas pausas que salvam o dia")}
    {img_break("smile.jpg", "Método simples. Vida real. Resultado leve.")}
    '''
    content = re.sub(r"<p>Você não precisa ser perfeita\.</p>\s*<p>Você precisa de um caminho\.</p>\s*<p>Vamos juntas\?</p>", "", content)
    content = re.sub(r"<p>Vamos juntas\?</p>", "", content)
    content = content.replace("</ul>", "</ul>" + promises, 1)
    content += closing
    return f"""
    <section class="intro-wrap pad">
      <div class="intro-banner">
        <h2>Introdução</h2>
        <p>Conectando com a dor da mãe sobrecarregada — e mostrando que dá para ter rotina leve com método.</p>
      </div>
      {content}
    </section>
    """


def build_toc() -> str:
    items = [
        (1, "Cozinha que trabalha por você", "Refeições e cozinha eficiente para família grande", "kitchen-1.jpg", "#ff6b57"),
        (2, "A casa pode fluir melhor", "Horários, tarefas e divisão de responsabilidades", "tidy.jpg", "#0f8f8a"),
        (3, "Tempo para eles e para você", "Cuidados com os filhos + tempo próprio", "time-1.jpg", "#3d8bfd"),
        (4, "Filhos que ajudam de verdade", "Autonomia e participação na rotina", "play.jpg", "#c44569"),
        (5, "Calma no meio do caos", "Saúde mental no dia a dia", "calm-2.jpg", "#ffc857"),
    ]
    cards = []
    for num, title, desc, img, color in items:
        cards.append(f'''
        <div class="toc-card">
          <div class="thumb"><img src="{uri(img)}" alt="{html.escape(title)}" /></div>
          <div class="info">
            <span class="num" style="background:{color}">Capítulo {num}</span>
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(desc)}</p>
          </div>
        </div>''')
    return f'''<section class="toc pad">
      <h2>O que você vai encontrar</h2>
      <p>Cinco capítulos práticos, visuais e diretos — para aplicar ainda esta semana.</p>
      <div class="color-strip"></div>
      {''.join(cards)}
    </section>'''


CHAPTERS = {
    1: {
        "title": "Cozinha que trabalha por você",
        "subtitle": "Planejamento de refeições e cozinha eficiente para famílias grandes",
        "image": "kitchen-1.jpg",
        "color": "#ff6b57",
        "mid": lambda: img_duo("kitchen-2.jpg", "market.jpg", "Prep que economiza energia", "Compras com lista e menos estresse"),
        "late": lambda: img_break("breakfast.jpg", "Café da manhã simples também é estratégia", tall=False),
        "inject": {
            "método em 4 passos": img_break("veggies.jpg", "Comida de verdade, sistema simples", True),
        },
    },
    2: {
        "title": "A casa não se limpa sozinha (mas pode fluir melhor)",
        "subtitle": "Horários, tarefas domésticas e divisão de responsabilidades",
        "image": "tidy.jpg",
        "color": "#0f8f8a",
        "mid": lambda: img_duo("home-2.jpg", "laundry.jpg", "Casa funcional > casa perfeita", "Lavanderia em ritmo sustentável"),
        "late": lambda: img_break("cozy.jpg", "Uma superfície limpa já muda o clima da casa"),
        "inject": {
            "Rotinas âncora": img_break("checklist-img.jpg", "Âncoras curtas reduzem discussão"),
        },
    },
    3: {
        "title": "Tempo para eles, tempo para você",
        "subtitle": "Gerenciamento de tempo entre cuidados e tempo próprio",
        "image": "time-1.jpg",
        "color": "#3d8bfd",
        "mid": lambda: img_duo("time-2.jpg", "coffee.jpg", "Blocos reais de descanso", "Micro-pausas que recarregam"),
        "late": lambda: img_break("sunset.jpg", "Tempo próprio não é egoísmo — é manutenção"),
        "inject": {
            "mapa da semana": img_break("planner.jpg", "O que não está no papel some no caos"),
        },
    },
    4: {
        "title": "Filhos que ajudam (de verdade)",
        "subtitle": "Autonomia e participação das crianças na rotina",
        "image": "play.jpg",
        "color": "#c44569",
        "mid": lambda: img_duo("kids-2.jpg", "toys.jpg", "Participar cria pertencimento", "Missões curtas > sermões longos"),
        "late": lambda: img_break("smile.jpg", "Elogie o esforço, não só o resultado"),
        "inject": {
            "faixa etária": img_break("kids-2.jpg", "Cada idade pode contribuir de um jeito"),
        },
    },
    5: {
        "title": "Calma no meio do caos",
        "subtitle": "Saúde mental e equilíbrio emocional no dia a dia",
        "image": "calm-2.jpg",
        "color": "#ffc857",
        "mid": lambda: img_duo("calm-1.jpg", "journal.jpg", "Respirar também é produtividade", "Rituais que protegem sua mente"),
        "late": lambda: img_break("sunset.jpg", "Você pode ser uma mãe boa e cansada ao mesmo tempo"),
        "inject": {
            "primeiros socorros": img_break("time-1.jpg", "No pico do estresse: pare o corpo primeiro"),
        },
    },
}


def build_chapter(num: int, md: str) -> str:
    meta = CHAPTERS[num]
    # strip leading chapter headers from md
    md2 = re.sub(r"^#\s+Capítulo\s+\d+\s*$", "", md, count=1, flags=re.M)
    md2 = re.sub(r"^##\s+.+$", "", md2, count=1, flags=re.M)
    md2 = re.sub(r"^###\s+.+$", "", md2, count=1, flags=re.M)
    body = render_md(md2, inject_after_h3=meta.get("inject", {}))

    # insert mid image after roughly first third of content blocks
    parts = body.split("</p>")
    if len(parts) > 8:
        mid_at = max(6, len(parts) // 3)
        parts[mid_at] = parts[mid_at] + "</p>" + meta["mid"]()
        body = "</p>".join(parts)
        # fix potential double
        body = body.replace("</p></p>", "</p>")
    else:
        body = meta["mid"]() + body

    # late image before first checklist if present
    if '<ul class="checklist">' in body:
        body = body.replace('<ul class="checklist">', meta["late"]() + '<ul class="checklist">', 1)
    else:
        body += meta["late"]()

    return (
        chapter_hero(num, meta["title"], meta["subtitle"], meta["image"], meta["color"])
        + body
        + "</div></section>"
    )


def build_conclusion(md: str) -> str:
    md2 = re.sub(r"^#\s+Conclusão.*$", "", md, count=1, flags=re.M)
    md2 = re.sub(r"^###\s+Você não precisa.*$", "", md2, count=1, flags=re.M)
    body = render_md(md2)
    # ensure cta panel closed
    if '<div class="cta-panel">' in body and "</div><!--cta-->" not in body:
        # close before fine print or end
        if '<p class="fine">' in body:
            body = body.replace('<p class="fine">', '</div><p class="fine">', 1)
        else:
            body += "</div>"
    return f'''
    <section class="chapter big-close" style="--accent:#c44569">
      <div class="hero">
        <img src="{uri('family.jpg')}" alt="Conclusão" />
        <div class="hero-shade"></div>
        <div class="hero-copy">
          <span class="badge">Conclusão</span>
          <h1>Você não precisa dar conta de tudo</h1>
          <p>Você precisa de um sistema que te carregue nos dias difíceis.</p>
        </div>
      </div>
      <div class="chapter-body">
        {img_duo('smile.jpg', 'sunset.jpg', 'Progresso pequeno conta', 'Sustentável > perfeito')}
        {body}
      </div>
    </section>
    '''


def build_extras(md: str) -> str:
    md2 = re.sub(r"^##\s+Extras.*$", "", md, count=1, flags=re.M)
    body = render_md(md2)
    return f'''
    <section class="extras pad">
      <div class="extras-banner">
        <h2>Extras práticos</h2>
        <p style="margin:6px 0 0;color:rgba(255,255,255,.95)">Checklists prontos para copiar, imprimir e colar na geladeira.</p>
      </div>
      {img_break('checklist-img.jpg', 'Tire da cabeça. Coloque no papel.')}
      {body}
    </section>
    '''


def build_html(md: str) -> str:
    parts = slice_md(md)
    chapters_html = "\n".join(build_chapter(n, parts["body"][n]) for n in range(1, 6) if n in parts["body"])
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Rotina Leve com Família Grande</title>
<style>{CSS}</style>
</head>
<body>
  <section class="cover">
    <img class="bg" src="{uri('cover-bright.jpg')}" alt="Capa" />
    <div class="veil"></div>
    <div class="accent-bar"></div>
    <div class="copy">
      <div class="pill">Coleção Organização Real para Mães · E-book 1</div>
      <h1>Rotina Leve com Família Grande</h1>
      <p class="sub">O método prático para mães sobrecarregadas organizarem a casa, o tempo e a mente — sem culpa e sem perfeição.</p>
      <p class="meta">Para mães de famílias grandes — e para toda mãe que sente que o dia nunca é suficiente.</p>
    </div>
  </section>

  {build_intro(parts['intro'])}
  {build_toc()}
  {chapters_html}
  {build_conclusion(parts['conclusion'])}
  {build_extras(parts['extras'])}
</body>
</html>
"""


def main() -> None:
    ROOT.joinpath("dist").mkdir(parents=True, exist_ok=True)
    md = MD_PATH.read_text(encoding="utf-8")
    html_doc = build_html(md)
    HTML_PATH.write_text(html_doc, encoding="utf-8")
    print(f"HTML: {HTML_PATH} ({HTML_PATH.stat().st_size/1024:.0f} KB)")
    HTML(string=html_doc, base_url=str(ROOT)).write_pdf(PDF_PATH)
    from pypdf import PdfReader
    pages = len(PdfReader(str(PDF_PATH)).pages)
    print(f"PDF:  {PDF_PATH} ({PDF_PATH.stat().st_size/1024:.0f} KB, {pages} pages)")


if __name__ == "__main__":
    main()
