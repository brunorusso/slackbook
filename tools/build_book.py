#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from typing import Iterable, Sequence

import markdown
from markdown.extensions.toc import slugify

try:
    from weasyprint import HTML
except ImportError:  # pragma: no cover - optional dependency for PDF rendering.
    HTML = None

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_BOOK_DIR = REPO_ROOT / "src-book"
OUTPUT_DIR = REPO_ROOT / "the-book"
OUTPUT_FILE = OUTPUT_DIR / "book.html"
OUTPUT_PDF_FILE = OUTPUT_DIR / "book.pdf"
ASSET_DIRECTORIES = ("img", "ps-imgs")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera o livro em HTML ou PDF.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--html",
        dest="output_format",
        action="store_const",
        const="html",
        help="Gera o livro em formato HTML (padrão).",
    )
    group.add_argument(
        "--pdf",
        dest="output_format",
        action="store_const",
        const="pdf",
        help="Gera o livro em formato PDF usando papel A4.",
    )
    parser.set_defaults(output_format="html")
    return parser.parse_args(argv)


def copy_asset_directories(src_dir: Path, output_dir: Path) -> None:
    if not src_dir.exists():
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    for relative_dir in ASSET_DIRECTORIES:
        source_dir = src_dir / relative_dir
        if not source_dir.exists():
            continue

        for source_path in sorted(source_dir.rglob("*")):
            if source_path.is_dir():
                continue

            relative_path = source_path.relative_to(src_dir)
            destination = output_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination)


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1].lstrip("\n")
    return text


def _clean_heading(title: str) -> str:
    title = re.sub(r"`([^`]*)`", r"\1", title)
    title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
    title = re.sub(r"[*_~]", "", title)
    return re.sub(r"\s+", " ", title).strip()


def _make_anchor(title: str, used: dict[str, int]) -> str:
    base = slugify(_clean_heading(title), "-")
    count = used.get(base, 0)
    used[base] = count + 1
    return f"{base}-{count}" if count else base


def read_main_markdown_order(main_file: Path) -> list[Path]:
    if not main_file.exists():
        raise FileNotFoundError(f"Arquivo principal não encontrado: {main_file}")

    text = main_file.read_text(encoding="utf-8")
    targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    order: list[Path] = []
    seen: set[Path] = set()

    for target in targets:
        if not target.lower().endswith(".md"):
            continue
        candidate = (main_file.parent / target).resolve()
        if candidate.exists() and candidate.is_file() and candidate.name != "main.md":
            if candidate not in seen:
                order.append(candidate)
                seen.add(candidate)

    if not order:
        order = [
            path for path in sorted(SRC_BOOK_DIR.glob("*.md")) if path.name != "main.md"
        ]

    return order


def _render_toc_items(nodes: list[dict[str, object]]) -> str:
    if not nodes:
        return ""

    html = ["<ul>"]
    for node in nodes:
        title = str(node["title"])
        href = str(node["href"])
        children = node.get("children", [])
        html.append(f'<li><a href="{href}">{title}</a>')
        if children:
            html.append(_render_toc_items(children))
        html.append("</li>")
    html.append("</ul>")
    return "".join(html)


def build_toc(files: Iterable[Path]) -> str:
    roots: list[dict[str, object]] = []
    for file_path in files:
        text = strip_front_matter(file_path.read_text(encoding="utf-8"))
        headings: list[tuple[int, str]] = []
        for line in text.splitlines():
            match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
            if not match:
                continue
            level = len(match.group(1))
            title = _clean_heading(match.group(2).strip())
            if title:
                headings.append((level, title))

        if not headings:
            continue

        used: dict[str, int] = {}
        first_level, first_title = headings[0]
        first_anchor = _make_anchor(first_title, used)
        root = {"title": first_title, "href": f"#{first_anchor}", "children": []}
        stack: list[tuple[int, list[dict[str, object]]]] = [(first_level - 1, root["children"])]

        for level, title in headings[1:]:
            anchor = _make_anchor(title, used)
            node = {"title": title, "href": f"#{anchor}", "children": []}
            while stack and level <= stack[-1][0]:
                stack.pop()
            parent = stack[-1][1]
            parent.append(node)
            stack.append((level, node["children"]))

        roots.append(root)

    if not roots:
        return "<nav class=\"book-toc\"><h2>Índice</h2><p>Nenhum capítulo encontrado.</p></nav>"

    toc_html = [
        "<nav class=\"book-toc\">",
        "<h2>Índice</h2>",
        _render_toc_items(roots),
        "</nav>",
    ]
    return "\n".join(toc_html)


def render_markdown_file(file_path: Path) -> str:
    text = strip_front_matter(file_path.read_text(encoding="utf-8"))
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    html = markdown.markdown(
        text,
        extensions=[
            "extra",
            "fenced_code",
            "sane_lists",
            "tables",
            "toc",
            "md_in_html",
        ],
        output_format="html5",
    )
    section_id = slugify(file_path.stem, "-")
    return f'<section id="{section_id}" class="book-section">{html}</section>'


def generate_book_html(src_dir: Path = SRC_BOOK_DIR) -> str:
    ordered_files = read_main_markdown_order(src_dir / "main.md")
    cover_html = ""
    rest_html: list[str] = []

    for file_path in ordered_files:
        if not file_path.exists() or file_path.suffix.lower() != ".md":
            continue

        rendered = render_markdown_file(file_path)
        if file_path.name == "cover.md":
            cover_html = rendered
        else:
            rest_html.append(rendered)

    toc = build_toc(ordered_files)
    title = "SlackBook"

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    @page {{
      size: A4;
      margin: 1.5cm;
    }}
    :root {{
      --page-bg: #faf8f4;
      --panel-bg: #ffffff;
      --border: #d8d3c6;
      --text: #1f2933;
      --muted: #52606d;
      --accent: #005a9c;
      --code-bg: #f3f4f6;
    }}
    body {{
      margin: 0;
      background: var(--page-bg);
      color: var(--text);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.7;
    }}
    main {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 2rem 1.25rem 4rem;
    }}
    .book-toc {{
      background: var(--panel-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1rem 1.25rem;
      margin-bottom: 2rem;
    }}
    .book-toc ul {{
      margin: 0.5rem 0 0 1.25rem;
      padding-left: 1rem;
    }}
    .book-toc li {{
      margin: 0.2rem 0;
    }}
    .book-toc a, a {{
      color: var(--accent);
      text-decoration: none;
    }}
    .book-toc a:hover, a:hover {{
      text-decoration: underline;
    }}
    .book-section {{
      background: var(--panel-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem 1.5rem 2rem;
      margin-bottom: 2rem;
    }}
    .book-section h1, .book-section h2, .book-section h3 {{
      color: #111827;
      margin-top: 1.5rem;
      margin-bottom: 0.75rem;
    }}
    .book-section img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 1rem auto;
      border: 1px solid var(--border);
      border-radius: 6px;
    }}
    .book-section pre {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1rem;
      overflow-x: auto;
    }}
    .book-section code {{
      background: var(--code-bg);
      padding: 0.1rem 0.35rem;
      border-radius: 4px;
    }}
    .book-section blockquote {{
      border-left: 4px solid var(--accent);
      padding-left: 1rem;
      color: var(--muted);
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin: 1rem 0;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 0.55rem 0.75rem;
      text-align: left;
      vertical-align: top;
    }}
  </style>
</head>
<body>
  <main>
    {cover_html}
    {toc}
    {''.join(rest_html)}
  </main>
</body>
</html>
'''


def export_pdf(html_content: str, output_path: Path = OUTPUT_PDF_FILE) -> Path:
    if HTML is None:
        raise RuntimeError(
            "A geração de PDF requer a biblioteca 'weasyprint'. Instale com: pip install weasyprint"
        )

    HTML(string=html_content, base_url=str(OUTPUT_DIR)).write_pdf(target=str(output_path))
    return output_path


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    copy_asset_directories(SRC_BOOK_DIR, OUTPUT_DIR)

    html_content = generate_book_html(SRC_BOOK_DIR)
    OUTPUT_FILE.write_text(html_content, encoding="utf-8")
    print(f"Livro gerado em: {OUTPUT_FILE}")

    if args.output_format == "pdf":
        pdf_path = export_pdf(html_content, OUTPUT_PDF_FILE)
        print(f"Livro PDF gerado em: {pdf_path}")


if __name__ == "__main__":
    main()
