#!/usr/bin/env python3
"""Convert DocBook XML chapters into Markdown while preserving the full text."""

from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent

ENTITY_MAP = {
    "&mdash;": "—",
    "&ndash;": "–",
    "&ldquo;": "“",
    "&rdquo;": "”",
    "&lsquo;": "‘",
    "&rsquo;": "’",
    "&hellip;": "…",
    "&middot;": "·",
    "&copy;": "©",
    "&reg;": "®",
    "&trade;": "™",
}

INLINE_TAGS = {
    "application": "`{}`",
    "filename": "`{}`",
    "userinput": "`{}`",
    "keycap": "<kbd>{}</kbd>",
    "arg": "`{}`",
    "prompt": "`{}`",
    "parameter": "`{}`",
    "literal": "`{}`",
    "command": "`{}`",
    "computeroutput": "`{}`",
    "classname": "`{}`",
    "function": "`{}`",
    "systemitem": "`{}`",
    "email": "<{ }>",
}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def clean_space(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def inline_render(node: ET.Element | None) -> str:
    if node is None:
        return ""

    tag = local_name(node.tag)
    if tag in {"title", "bookinfo"}:
        text = "".join(node.itertext())
        return clean_space(text)

    if tag in INLINE_TAGS:
        raw = clean_space("".join(node.itertext()))
        if tag == "keycap":
            return f"<kbd>{raw}</kbd>"
        if tag == "email":
            return f"<{raw}>"
        return INLINE_TAGS[tag].format(raw)

    if tag == "emphasis":
        raw = clean_space("".join(node.itertext()))
        if node.get("role") in {"strong", "bold"}:
            return f"**{raw}**"
        return f"*{raw}*"

    if tag == "quote":
        raw = clean_space("".join(node.itertext()))
        return f"\"{raw}\""

    parts: list[str] = []
    if node.text:
        parts.append(clean_space(node.text))
    for child in list(node):
        parts.append(inline_render(child))
        if child.tail:
            parts.append(clean_space(child.tail))
    return " ".join(p for p in parts if p).strip()


def title_text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return clean_space("".join(node.itertext()))


def render_list(node: ET.Element, ordered: bool) -> list[str]:
    out: list[str] = []
    prefix = "1." if ordered else "-"
    for item in node.findall("./listitem"):
        item_parts: list[str] = []
        for child in list(item):
            tag = local_name(child.tag)
            if tag == "para":
                item_parts.append(inline_render(child))
            elif tag in {"itemizedlist", "orderedlist"}:
                nested = render_list(child, tag == "orderedlist")
                item_parts.append("\n".join(f"  {line}" if line.startswith("-") or line.startswith("1.") else line for line in nested))
            elif tag == "screen":
                body = clean_space("".join(child.itertext()))
                if body:
                    item_parts.append("```text\n" + body + "\n```")
            elif tag == "table":
                item_parts.append(render_table(child))
            else:
                item_parts.append(inline_render(child))
        text = " ".join(part.strip() for part in item_parts if part.strip())
        if text:
            out.append(f"{prefix} {text}")
    return out


def render_table(node: ET.Element) -> str:
    tgroup = node.find("./tgroup")
    if tgroup is None:
        return ""
    rows: list[list[str]] = []
    for row in tgroup.findall("./thead/row") + tgroup.findall("./tbody/row"):
        cells = [clean_space("".join(entry.itertext())) for entry in row.findall("./entry")]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(row[: len(header)]) + " |")
    return "\n".join(lines)


def render_block(node: ET.Element) -> list[str]:
    tag = local_name(node.tag)
    if tag in {"screen", "programlisting", "literallayout"}:
        body = clean_space("".join(node.itertext()))
        if body:
            return ["```text", body, "```"]
        return []
    if tag == "para":
        text = inline_render(node)
        return [text] if text else []
    if tag == "section":
        return render_section(node, 2)
    if tag == "table":
        table = render_table(node)
        return [table] if table else []
    if tag in {"itemizedlist", "orderedlist"}:
        return render_list(node, ordered=(tag == "orderedlist"))
    if tag == "blockquote":
        text = clean_space("".join(node.itertext()))
        return [f"> {text}"] if text else []
    if tag == "imagedata":
        ref = node.get("fileref")
        if ref:
            return [f"![image]({ref})"]
        return []
    if tag == "title":
        return []

    out: list[str] = []
    for child in list(node):
        out.extend(render_block(child))
    return out


def render_section(node: ET.Element, level: int) -> list[str]:
    out: list[str] = []
    title = None
    for child in list(node):
        if local_name(child.tag) == "title":
            title = child
            break
    if title is not None:
        heading = "#" * level
        out.append(f"{heading} {title_text(title)}")
    for child in list(node):
        if local_name(child.tag) == "title":
            continue
        if local_name(child.tag) == "section":
            out.extend(render_section(child, level + 1))
        else:
            out.extend(render_block(child))
    return out


def normalize_entities(raw: str) -> str:
    for entity, replacement in ENTITY_MAP.items():
        raw = raw.replace(entity, replacement)
    return raw


def convert_file(xml_path: Path) -> str:
    raw = normalize_entities(xml_path.read_text(encoding="utf-8"))
    root = ET.fromstring(raw)
    title = None
    for child in list(root):
        if local_name(child.tag) == "title":
            title = child
            break

    lines: list[str] = []
    if title is not None:
        lines.append(f"# {title_text(title)}")

    for child in list(root):
        if local_name(child.tag) == "title":
            continue
        if local_name(child.tag) == "section":
            lines.extend(render_section(child, 2))
        else:
            lines.extend(render_block(child))

    return "\n\n".join(filter(None, lines)).rstrip() + "\n"


def md_name(xml_name: str) -> str:
    return xml_name.replace(".xml", ".md")


def aggregate_index() -> str:
    files = [
        "preface.md",
        *[f"chapter_{i:02d}.md" for i in range(1, 20)],
        "appendix_emacspeak.md",
    ]
    lines = [
        "---",
        "title: \"The Slack Book\"",
        "---",
        "",
        "# The Slack Book",
        "",
    ]
    for name in files:
        if not (ROOT / name).exists():
            continue
        label = "Preface"
        if name.startswith("chapter_"):
            num = name.split("_")[1].split(".")[0]
            label = f"Chapter {int(num)}"
        elif name == "appendix_emacspeak.md":
            label = "Appendix: Emacspeak"
        lines.append(f"- [{label}]({name})")
    return "\n".join(lines) + "\n"


def generate() -> None:
    for xml_file in sorted(ROOT.glob("*.xml")):
        name = xml_file.name
        if name in {"main.xml", "template.xml"}:
            continue
        md_file = ROOT / md_name(name)
        md_file.write_text(convert_file(xml_file), encoding="utf-8")

    (ROOT / "main.md").write_text(aggregate_index(), encoding="utf-8")
    (ROOT / "template.md").write_text("---\ntitle: \"The Slack Book\"\n---\n\n# The Slack Book\n", encoding="utf-8")


if __name__ == "__main__":
    generate()
