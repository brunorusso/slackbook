from pathlib import Path
import re

try:
    import markdown
    from markdown.extensions.toc import slugify
except ModuleNotFoundError:
    raise SystemExit(
        "The 'markdown' package is required. Install it with: python3 -m pip install markdown"
    )

ROOT = Path(__file__).resolve().parent
MAIN_MD = ROOT / "main.md"
OUTPUT_HTML = ROOT / "book.html"


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1].lstrip("\n")
    return text


def get_first_heading(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        match = re.match(r"^(#+)\s+(.*)$", line.strip())
        if match:
            return match.group(2).strip()
    return "Untitled"


def collect_heading_entries(markdown_text: str) -> list[tuple[int, str, str]]:
    entries: list[tuple[int, str, str]] = []
    for line in markdown_text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()
        if title:
            entries.append((level, title, slugify(title, "-")))
    return entries


def build_nested_toc(entries: list[tuple[int, str, str]]) -> str:
    if not entries:
        return ""

    root_level = min(level for level, _, _ in entries)
    root: list[dict[str, object]] = []
    stack: list[tuple[int, list[dict[str, object]]]] = [(root_level - 1, root)]

    for level, title, anchor in entries:
        while stack and level <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]
        node = {"title": title, "anchor": anchor, "children": []}
        parent.append(node)
        stack.append((level, node["children"]))

    def render(items: list[dict[str, object]]) -> str:
        if not items:
            return ""
        html = ["<ul>"]
        for item in items:
            title = str(item["title"])
            anchor = str(item["anchor"])
            children = item["children"]
            html.append(f'<li><a href="#{anchor}">{title}</a>')
            if children:
                html.append(render(children))
            html.append("</li>")
        html.append("</ul>")
        return "".join(html)

    return render(root)


def collect_markdown_files() -> list[Path]:
    if not MAIN_MD.exists():
        raise FileNotFoundError(f"{MAIN_MD.name} not found")

    root = MAIN_MD.parent
    ordered = []
    seen = set()

    for name in ["cover.md", "preface.md"]:
        path = root / name
        if path.exists() and path not in seen:
            ordered.append(path)
            seen.add(path)

    for i in range(1, 100):
        name = f"chapter_{i:02d}.md"
        path = root / name
        if path.exists() and path not in seen:
            ordered.append(path)
            seen.add(path)
        elif not path.exists():
            break

    for name in sorted(root.glob("*.md")):
        if name.name in {"cover.md", "preface.md", "main.md", "template.md"}:
            continue
        if name.name.startswith("chapter_"):
            continue
        if name.name not in {p.name for p in ordered}:
            ordered.append(name)

    return ordered


def render_toc(files: list[Path]) -> str:
    items = []
    for path in files:
        if path.name in {"cover.md", "main.md", "template.md"}:
            continue

        content = strip_front_matter(path.read_text(encoding="utf-8"))
        headings = collect_heading_entries(content)
        if not headings:
            continue

        chapter_title, chapter_anchor = headings[0][1], headings[0][2]
        nested = ""
        if len(headings) > 1:
            nested = build_nested_toc(headings[1:])

        items.append(f'<li><a href="#{chapter_anchor}">{chapter_title}</a>{nested}</li>')

    return f"""
<nav>
  <h2>Table of Contents</h2>
  <ul>
    {' '.join(items)}
  </ul>
</nav>
"""


def render_chapter(path: Path) -> str:
    content = strip_front_matter(path.read_text(encoding="utf-8"))
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    html = markdown.markdown(
        content,
        extensions=["fenced_code", "tables", "toc", "sane_lists", "nl2br"],
    )
    return f'<section id="{path.stem}">{html}</section>'


def normalize_chapter_headings() -> None:
    xml_titles = {}
    for path in sorted(ROOT.glob("chapter_*.xml")):
        chapter_no = int(path.stem.split("_")[1])
        match = re.search(r"<title>(.*?)</title>", path.read_text(encoding="utf-8"), re.S)
        if match:
            title = re.sub(r"<[^>]+>", " ", match.group(1))
            title = re.sub(r"\s+", " ", title).strip()
            xml_titles[chapter_no] = title

    for path in sorted(ROOT.glob("chapter_*.md")):
        chapter_no = int(path.stem.split("_")[1])
        lines = path.read_text(encoding="utf-8").splitlines()
        out = []
        in_code_fence = False
        h2 = 0
        h3 = 0
        h4 = 0
        for line in lines:
            if line.strip().startswith("```"):
                out.append(line)
                in_code_fence = not in_code_fence
                continue
            if in_code_fence:
                out.append(line)
                continue

            match = re.match(r"^(#+)\s*(.*)$", line)
            if not match:
                out.append(line)
                continue

            level = len(match.group(1))
            title = match.group(2).strip()
            clean_title = re.sub(r"^[\d\.\s]+", "", title).strip()

            if level == 1:
                final_title = clean_title or xml_titles.get(chapter_no, "")
                if final_title:
                    out.append(f"# {chapter_no}. {final_title}")
                else:
                    out.append(f"# {chapter_no}")
            elif level == 2:
                h2 += 1
                h3 = 0
                h4 = 0
                out.append(f"## {chapter_no}.{h2}{f' {clean_title}' if clean_title else ''}")
            elif level == 3:
                h3 += 1
                h4 = 0
                out.append(f"### {chapter_no}.{h2}.{h3}{f' {clean_title}' if clean_title else ''}")
            elif level >= 4:
                h4 += 1
                out.append(f"{'#' * level} {chapter_no}.{h2}.{h3}.{h4}{f' {clean_title}' if clean_title else ''}")

        path.write_text("\n".join(out) + "\n", encoding="utf-8")


def build_book_html() -> str:
    chapter_files = collect_markdown_files()
    title = "The Slack Book"

    rendered_html = []
    for idx, path in enumerate(chapter_files):
        if idx == 0 and path.name == "cover.md":
            rendered_html.append(render_chapter(path))
            rendered_html.append(render_toc(chapter_files))
            continue
        if path.name == "preface.md":
            rendered_html.append(render_chapter(path))
            continue
        if path.name.startswith("chapter_"):
            rendered_html.append(render_chapter(path))
            continue
        if path.name.endswith(".md"):
            rendered_html.append(render_chapter(path))

    book_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{ font-family: sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem 3rem; line-height: 1.7; }}
    h1, h2, h3 {{ color: #222; }}
    nav {{ background: #f7f7f7; border: 1px solid #ddd; padding: 1rem 1.25rem; margin-bottom: 2rem; }}
    nav ul {{ padding-left: 1.25rem; }}
    section {{ margin-top: 2rem; }}
    img {{ max-width: 100%; height: auto; display: block; margin: 1rem 0; }}
    pre {{ background: #f5f5f5; padding: 1rem; overflow-x: auto; }}
    code {{ font-family: monospace; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
    th, td {{ border: 1px solid #d0d0d0; padding: 0.5rem 0.75rem; text-align: left; }}
  </style>
</head>
<body>
  {''.join(rendered_html)}
</body>
</html>
"""
    return book_html


if __name__ == "__main__":
    OUTPUT_HTML.write_text(build_book_html(), encoding="utf-8")
    print(f"Generated {OUTPUT_HTML}")