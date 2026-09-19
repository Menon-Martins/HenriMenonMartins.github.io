#!/usr/bin/env python3
"""Build a beautiful full-color PDF e-book."""

from __future__ import annotations

import html
import re
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
MD_PATH = ROOT / "rotina-leve-familia-grande.md"
HTML_PATH = ROOT / "dist" / "ebook.html"
PDF_PATH = ROOT / "dist" / "Rotina-Leve-com-Familia-Grande.pdf"
ASSETS = ROOT / "assets"

CHAPTER_META = {
    1: ("cap1-cozinha.png", "Cozinha que trabalha por você", "Planejamento de refeições e cozinha eficiente para famílias grandes"),
    2: ("cap2-casa.png", "A casa não se limpa sozinha (mas pode fluir melhor)", "Organização de horários, tarefas domésticas e divisão de responsabilidades"),
    3: ("cap3-tempo.png", "Tempo para eles, tempo para você", "Gerenciamento de tempo entre cuidados com as crianças e tempo próprio"),
    4: ("cap4-autonomia.png", "Filhos que ajudam (de verdade)", "Criação de autonomia e participação das crianças na rotina"),
    5: ("cap5-calma.png", "Calma no meio do caos", "Saúde mental e equilíbrio emocional no dia a dia"),
}


def md_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
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
    out = ['<div class="table-wrap"><table>']
    out.append("<thead><tr>" + "".join(f"<th>{md_inline(c)}</th>" for c in header) + "</tr></thead><tbody>")
    for row in body:
        while len(row) < len(header):
            row.append("")
        out.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in row[: len(header)]) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out), i


def asset_uri(name: str) -> str:
    return (ASSETS / name).resolve().as_uri()


def render_blocks(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_list = False
    list_tag = "ul"
    open_sections: list[str] = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append(f"</{list_tag}>")
            in_list = False

    def open_section(cls: str) -> None:
        close_list()
        out.append(f'<section class="{cls}">')
        open_sections.append(cls)

    def close_sections() -> None:
        close_list()
        while open_sections:
            open_sections.pop()
            out.append("</section>")

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_list()
            i += 1
            continue

        if stripped == "---":
            close_list()
            out.append('<hr class="soft-rule" />')
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
            close_list()
            table_html, i = parse_table(lines, i)
            out.append(table_html)
            continue

        m_cap = re.match(r"^#\s+Capítulo\s+(\d+)\s*$", stripped)
        if m_cap:
            close_sections()
            num = int(m_cap.group(1))
            title = CHAPTER_META.get(num, ("", f"Capítulo {num}", ""))[1]
            subtitle = CHAPTER_META.get(num, ("", "", ""))[2]
            img = CHAPTER_META.get(num, ("", "", ""))[0]
            j = i + 1
            # Consume only the immediate ## title and one ### subtitle under the chapter.
            got_h2 = False
            got_h3 = False
            while j < len(lines):
                s = lines[j].strip()
                if not s:
                    j += 1
                    continue
                if not got_h2 and s.startswith("## ") and not s.startswith("###"):
                    title = s[3:].strip()
                    got_h2 = True
                    j += 1
                    continue
                if got_h2 and not got_h3 and s.startswith("### "):
                    subtitle = s[4:].strip()
                    got_h3 = True
                    j += 1
                    break
                break
            open_section("chapter")
            out.append('<div class="chapter-hero">')
            if img:
                out.append(f'<img src="{asset_uri(img)}" alt="Capítulo {num}" />')
            out.append('<div class="chapter-hero-overlay">')
            out.append(f'<span class="chapter-kicker">Capítulo {num}</span>')
            out.append(f"<h1>{md_inline(title)}</h1>")
            if subtitle:
                out.append(f'<p class="chapter-sub">{md_inline(subtitle)}</p>')
            out.append("</div></div>")
            i = j
            continue

        if re.match(r"^#\s+Conclusão", stripped):
            close_sections()
            open_section("chapter conclusion-chapter")
            # consume optional ### under it
            title = stripped[2:].strip()
            j = i + 1
            sub = ""
            while j < len(lines):
                s = lines[j].strip()
                if not s:
                    j += 1
                    continue
                if s.startswith("### "):
                    sub = s[4:].strip()
                    j += 1
                    break
                break
            out.append('<div class="section-banner conclusion-banner">')
            out.append('<span class="chapter-kicker">Encerramento</span>')
            out.append(f"<h1>{md_inline(title)}</h1>")
            if sub:
                out.append(f'<p class="chapter-sub">{md_inline(sub)}</p>')
            out.append("</div>")
            i = j
            continue

        if stripped.startswith("#### "):
            close_list()
            out.append(f"<h4>{md_inline(stripped[5:].strip())}</h4>")
            i += 1
            continue

        if stripped.startswith("### "):
            close_list()
            text = stripped[4:].strip()
            cls = "h3"
            if text.startswith(("A dor", "A verdade", "A culpa", "O erro", "O caos")):
                cls = "pain-title"
            elif "Checklist" in text or "checklist" in text:
                cls = "checklist-title"
            elif "Mini plano" in text:
                cls = "action-title"
            elif "Chamada para ação" in text:
                out.append('<div class="cta-box">')
                out.append(f'<h3 class="cta-title">{md_inline(text)}</h3>')
                i += 1
                continue
            out.append(f'<h3 class="{cls}">{md_inline(text)}</h3>')
            i += 1
            continue

        if stripped.startswith("## "):
            close_list()
            text = stripped[3:].strip()
            if text.startswith("Extras"):
                # close cta box if open roughly
                if '<div class="cta-box">' in "\n".join(out[-30:]) and "</div><!--cta-->" not in "\n".join(out[-5:]):
                    out.append("</div><!--cta-->")
                close_sections()
                open_section("extras-section")
                out.append(f"<h2>{md_inline(text)}</h2>")
            elif text.startswith("Índice"):
                # skip — custom TOC
                i += 1
                # skip until next major section
                while i < len(lines):
                    s = lines[i].strip()
                    if s.startswith("# Capítulo") or s.startswith("## Introdução") is False and s.startswith("# "):
                        if s.startswith("# Capítulo") or s.startswith("## Conclus") or s.startswith("# Conclus"):
                            break
                    if s.startswith("# Capítulo"):
                        break
                    # stop at chapter 1
                    if re.match(r"^#\s+Capítulo\s+1", s):
                        break
                    i += 1
                continue
            else:
                out.append(f"<h2>{md_inline(text)}</h2>")
            i += 1
            continue

        if stripped.startswith("# "):
            close_list()
            out.append(f"<h1>{md_inline(stripped[2:].strip())}</h1>")
            i += 1
            continue

        if stripped.startswith("> "):
            close_list()
            out.append(f"<blockquote>{md_inline(stripped[2:].strip())}</blockquote>")
            i += 1
            continue

        if re.match(r"^- \[[ xX]\] ", stripped):
            if not in_list or list_tag != "ul":
                close_list()
                out.append('<ul class="checklist">')
                in_list = True
                list_tag = "ul"
            item = re.sub(r"^- \[[ xX]\] ", "", stripped)
            out.append(f'<li><span class="box"></span><span>{md_inline(item)}</span></li>')
            i += 1
            continue

        if stripped.startswith("- "):
            if not in_list or list_tag != "ul":
                close_list()
                out.append("<ul>")
                in_list = True
                list_tag = "ul"
            out.append(f"<li>{md_inline(stripped[2:])}</li>")
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            if not in_list or list_tag != "ol":
                close_list()
                out.append("<ol>")
                in_list = True
                list_tag = "ol"
            item = re.sub(r"^\d+\.\s+", "", stripped)
            out.append(f"<li>{md_inline(item)}</li>")
            i += 1
            continue

        close_list()
        if stripped.startswith("*Fim do") or stripped.startswith("*Coleção"):
            out.append(f'<p class="footer-note">{md_inline(stripped.strip("*"))}</p>')
        elif stripped.startswith("**Dica") or stripped.startswith("**Regra") or stripped.startswith("**Frase") or stripped.startswith("**Meta") or stripped.startswith("**Permissão") or stripped.startswith("**Se você") or stripped.startswith("**Você não"):
            out.append(f'<p class="callout">{md_inline(stripped)}</p>')
        else:
            out.append(f"<p>{md_inline(stripped)}</p>")
        i += 1

    close_sections()
    return "\n".join(out)


CSS = """
@font-face {
  font-family: 'DejaVu Serif';
  src: local('DejaVu Serif');
}
@font-face {
  font-family: 'DejaVu Sans';
  src: local('DejaVu Sans');
}

:root {
  --sage: #3f6f63;
  --sage-deep: #2f564c;
  --sage-soft: #dceae4;
  --peach: #e8a090;
  --peach-soft: #f7e3dc;
  --ink: #24302c;
  --muted: #5b6b64;
  --paper: #f7faf8;
  --white: #ffffff;
  --line: #c9ddd4;
  --sand: #eef5f1;
}

@page {
  size: A4;
  margin: 16mm 14mm 16mm 14mm;
  @bottom-center {
    content: counter(page);
    font-family: 'DejaVu Sans', sans-serif;
    font-size: 9pt;
    color: #5b6b64;
  }
}
@page :first {
  margin: 0;
  @bottom-center { content: none; }
}

* { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: 'DejaVu Sans', sans-serif;
  font-size: 10.8pt;
  line-height: 1.5;
}

img { max-width: 100%; }

.cover {
  break-after: page;
  width: 210mm;
  height: 297mm;
  margin: 0;
  position: relative;
  overflow: hidden;
  background: linear-gradient(165deg, #2f564c 0%, #3f6f63 45%, #6d9a8c 78%, #e8a090 100%);
}

.cover-image {
  position: absolute;
  inset: 0;
  width: 210mm;
  height: 297mm;
  object-fit: cover;
  opacity: 0.9;
}

.cover-veil {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(36,48,44,0.12) 0%, rgba(36,48,44,0.28) 45%, rgba(36,48,44,0.82) 100%);
}

.cover-content {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  z-index: 2;
  padding: 28mm 18mm 24mm;
  color: white;
}

.cover-badge {
  display: inline-block;
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.35);
  padding: 8px 14px;
  font-size: 9pt;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.cover h1 {
  font-family: 'DejaVu Serif', serif;
  font-size: 32pt;
  line-height: 1.1;
  margin: 0 0 12px;
  max-width: 12ch;
}

.cover .subtitle {
  font-size: 12pt;
  line-height: 1.45;
  max-width: 36ch;
  margin: 0 0 18px;
  color: rgba(255,255,255,0.95);
}

.cover-meta {
  font-size: 10pt;
  opacity: 0.92;
  border-top: 1px solid rgba(255,255,255,0.35);
  padding-top: 12px;
  max-width: 42ch;
}

.page-pad { padding: 0 2mm; }

h1, h2, h3, h4 {
  font-family: 'DejaVu Serif', serif;
  color: var(--sage-deep);
  line-height: 1.25;
  break-after: avoid;
}

h2 { font-size: 16pt; margin: 18px 0 8px; }
h3 { font-size: 12.5pt; margin: 14px 0 6px; }
h4 { font-size: 11pt; margin: 12px 0 5px; color: var(--sage); }

p { margin: 0 0 8px; }
strong { color: var(--sage-deep); }
ul, ol { margin: 0 0 10px; padding-left: 1.15em; }
li { margin-bottom: 4px; }

.soft-rule {
  border: none;
  border-top: 1px solid var(--line);
  margin: 14px 0;
}

.intro-card {
  background: linear-gradient(135deg, var(--sage-soft), var(--peach-soft));
  padding: 16px 16px 8px;
  margin: 0 0 14px;
  border-left: 5px solid var(--sage);
}
.intro-card h2 { margin-top: 0; }

.toc-section { break-before: page; }
.toc-grid { margin-top: 10px; }
.toc-item {
  display: table;
  width: 100%;
  background: var(--sand);
  border: 1px solid var(--line);
  padding: 10px 12px;
  margin: 0 0 10px;
}
.toc-num {
  display: table-cell;
  width: 40px;
  vertical-align: top;
}
.toc-num span {
  display: inline-block;
  width: 34px;
  height: 34px;
  line-height: 34px;
  text-align: center;
  border-radius: 50%;
  background: var(--sage);
  color: white;
  font-family: 'DejaVu Serif', serif;
  font-weight: 700;
  font-size: 13pt;
}
.toc-body { display: table-cell; vertical-align: top; padding-left: 10px; }
.toc-body h3 { margin: 0 0 3px; font-size: 12pt; }
.toc-body p { margin: 0; color: var(--muted); font-size: 9.5pt; }

.chapter { break-before: page; }

.chapter-hero {
  position: relative;
  margin: 0 0 14px;
  overflow: hidden;
  height: 200px;
  background: var(--sage);
}

.chapter-hero img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.chapter-hero-overlay {
  position: absolute;
  left: 0; right: 0; bottom: 0; top: 0;
  background: linear-gradient(100deg, rgba(36,48,44,0.82) 0%, rgba(36,48,44,0.4) 55%, rgba(36,48,44,0.18) 100%);
  color: white;
  padding: 16px 16px 14px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.chapter-kicker {
  display: inline-block;
  align-self: flex-start;
  background: rgba(232,160,144,0.95);
  color: #2c241f;
  font-size: 8.5pt;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 4px 9px;
  margin-bottom: 8px;
  font-family: 'DejaVu Sans', sans-serif;
}

.chapter-hero h1 {
  color: white;
  font-size: 18pt;
  margin: 0 0 4px;
}
.chapter-sub {
  margin: 0;
  color: rgba(255,255,255,0.93);
  font-size: 10pt;
  max-width: 52ch;
  font-family: 'DejaVu Sans', sans-serif;
}

.section-banner {
  background: linear-gradient(120deg, var(--sage-deep), var(--sage));
  color: white;
  padding: 18px 16px;
  margin: 0 0 14px;
}
.section-banner h1 { color: white; margin: 4px 0 0; font-size: 18pt; }
.section-banner .chapter-sub { color: rgba(255,255,255,0.92); }

.pain-title { color: var(--sage-deep); }
.checklist-title { color: var(--sage); }
.action-title {
  background: var(--peach-soft);
  display: inline-block;
  padding: 5px 10px;
  border-left: 4px solid var(--peach);
}

.callout {
  background: var(--sage-soft);
  border-left: 4px solid var(--sage);
  padding: 9px 11px;
  margin: 10px 0;
}

blockquote {
  margin: 12px 0;
  padding: 10px 14px;
  background: var(--peach-soft);
  border-left: 4px solid var(--peach);
  font-family: 'DejaVu Serif', serif;
  font-size: 11pt;
  color: var(--sage-deep);
}

.checklist {
  list-style: none;
  padding: 10px 12px;
  margin: 8px 0 12px;
  background: var(--white);
  border: 1px dashed var(--sage);
}
.checklist li {
  display: table;
  width: 100%;
  margin-bottom: 6px;
}
.checklist .box {
  display: table-cell;
  width: 16px;
  height: 14px;
  border: 1.5px solid var(--sage);
  background: white;
  vertical-align: top;
}
.checklist li > span:last-child {
  display: table-cell;
  padding-left: 8px;
  vertical-align: top;
}

.table-wrap {
  margin: 10px 0 14px;
  border: 1px solid var(--line);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9.5pt;
}
th {
  background: var(--sage);
  color: white;
  text-align: left;
  padding: 7px 8px;
  font-family: 'DejaVu Sans', sans-serif;
}
td {
  padding: 7px 8px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
tr:nth-child(even) td { background: var(--sand); }

.cta-box {
  break-inside: avoid;
  background: linear-gradient(135deg, var(--sage-deep), #4f8778);
  color: white;
  padding: 16px;
  margin: 14px 0;
}
.cta-box h3, .cta-box strong { color: white; }
.cta-box p, .cta-box li { color: rgba(255,255,255,0.96); }

.footer-note {
  text-align: center;
  color: var(--muted);
  font-size: 9pt;
  margin-top: 18px;
  padding-top: 10px;
  border-top: 1px solid var(--line);
}

.extras-section { break-before: page; }
"""


def build_toc() -> str:
    cards = []
    for num, (_img, title, desc) in CHAPTER_META.items():
        cards.append(
            f"""<div class="toc-item">
  <div class="toc-num"><span>{num}</span></div>
  <div class="toc-body">
    <h3>{html.escape(title)}</h3>
    <p>{html.escape(desc)}</p>
  </div>
</div>"""
        )
    return f"""<section class="toc-section page-pad">
  <h2>Índice / Sumário</h2>
  <p>Cinco capítulos práticos para transformar sobrecarga em sistema leve e repetível.</p>
  <div class="toc-grid">{''.join(cards)}
    <div class="toc-item">
      <div class="toc-num"><span style="background:#e8a090;color:#2c241f">+</span></div>
      <div class="toc-body">
        <h3>Conclusão, CTA e Extras</h3>
        <p>Encerramento inspirador, próximos e-books da coleção e checklists imprimíveis.</p>
      </div>
    </div>
  </div>
</section>"""


def extract_intro_and_body(md: str) -> tuple[str, str]:
    intro_m = re.search(r"^##\s+Introdução\s*$", md, re.M)
    toc_m = re.search(r"^##\s+Índice\s*/\s*Sumário\s*$", md, re.M)
    cap1_m = re.search(r"^#\s+Capítulo\s+1\s*$", md, re.M)
    intro = md[intro_m.start() : toc_m.start()] if intro_m and toc_m else ""
    body = md[cap1_m.start() :] if cap1_m else md
    return intro, body


def build_html(md: str) -> str:
    intro, body = extract_intro_and_body(md)
    intro_html = render_blocks(intro)
    body_html = render_blocks(body)
    capa = asset_uri("capa-ebook.png")

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Rotina Leve com Família Grande</title>
  <style>{CSS}</style>
</head>
<body>
  <section class="cover">
    <img class="cover-image" src="{capa}" alt="Capa" />
    <div class="cover-veil"></div>
    <div class="cover-content">
      <div class="cover-badge">Coleção Organização Real para Mães · E-book 1</div>
      <h1>Rotina Leve com Família Grande</h1>
      <p class="subtitle">O método prático para mães sobrecarregadas organizarem a casa, o tempo e a mente — sem culpa e sem perfeição.</p>
      <p class="cover-meta">Para mães de famílias grandes — e para toda mãe que sente que o dia nunca é suficiente.</p>
    </div>
  </section>

  <section class="page-pad">
    <div class="intro-card">{intro_html}</div>
  </section>

  {build_toc()}

  <div class="page-pad">{body_html}</div>
</body>
</html>"""


def main() -> None:
    ROOT.joinpath("dist").mkdir(parents=True, exist_ok=True)
    md = MD_PATH.read_text(encoding="utf-8")
    html_doc = build_html(md)
    HTML_PATH.write_text(html_doc, encoding="utf-8")
    print(f"HTML written: {HTML_PATH} ({HTML_PATH.stat().st_size} bytes)")

    HTML(string=html_doc, base_url=str(ROOT)).write_pdf(PDF_PATH)
    from pypdf import PdfReader

    pages = len(PdfReader(str(PDF_PATH)).pages)
    print(f"PDF written: {PDF_PATH} ({PDF_PATH.stat().st_size / 1024:.0f} KB, {pages} pages)")


if __name__ == "__main__":
    main()
