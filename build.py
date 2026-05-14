from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
POSTS_DIR = CONTENT_DIR / "posts"
OUTPUT_POSTS_DIR = ROOT / "posts"


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text

    raw_meta = parts[1].strip()
    body = parts[2].lstrip()
    meta = {}

    for line in raw_meta.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()

    return meta, body


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    in_code = False
    code_lines: list[str] = []
    quote_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            content = " ".join(line.strip() for line in paragraph)
            blocks.append(f"<p>{render_inline(content)}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            items = "".join(f"<li>{render_inline(item)}</li>" for item in list_items)
            blocks.append(f"<ul>{items}</ul>")
            list_items.clear()

    def flush_code() -> None:
        if code_lines:
            content = html.escape("\n".join(code_lines))
            blocks.append(f"<pre><code>{content}</code></pre>")
            code_lines.clear()

    def flush_quote() -> None:
        if quote_lines:
            content = " ".join(line.strip() for line in quote_lines if line.strip())
            blocks.append(f"<blockquote><p>{render_inline(content)}</p></blockquote>")
            quote_lines.clear()

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_quote()
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            flush_quote()
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            flush_list()
            flush_quote()
            blocks.append(f"<h1>{render_inline(stripped[2:])}</h1>")
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flush_list()
            flush_quote()
            blocks.append(f"<h2>{render_inline(stripped[3:])}</h2>")
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            flush_list()
            flush_quote()
            blocks.append(f"<h3>{render_inline(stripped[4:])}</h3>")
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            flush_quote()
            list_items.append(stripped[2:])
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            flush_list()
            quote_lines.append(stripped[1:].lstrip())
            continue

        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    flush_quote()
    flush_code()
    return "\n".join(blocks)


def slug_to_output(slug: str) -> Path:
    return OUTPUT_POSTS_DIR / f"{slug}.html"


def source_name_to_slug(source_name: str) -> str:
    match = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", source_name)
    return match.group(1) if match else source_name


def load_site() -> dict[str, object]:
    return json.loads((CONTENT_DIR / "site.json").read_text(encoding="utf-8"))


def load_home() -> str:
    return markdown_to_html((CONTENT_DIR / "home.md").read_text(encoding="utf-8"))


def load_about() -> str:
    return markdown_to_html((CONTENT_DIR / "about.md").read_text(encoding="utf-8"))


def load_posts() -> list[dict[str, str]]:
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        slug = source_name_to_slug(path.stem)
        posts.append(
            {
                "slug": slug,
                "title": meta.get("title", slug),
                "date": meta.get("date", ""),
                "tag": meta.get("tag", ""),
                "reading_time": meta.get("reading_time", ""),
                "summary": meta.get("summary", ""),
                "body_html": markdown_to_html(body),
            }
        )
    posts.sort(key=lambda item: item["date"], reverse=True)
    return posts


def nav(current: str) -> str:
    items = [
        ("Posts", "index.html"),
        ("Archive", "archive.html"),
        ("About", "about.html"),
    ]
    links = []
    for label, href in items:
        class_name = ' class="active"' if href == current else ""
        links.append(f'<a{class_name} href="{href}">{label}</a>')
    return "".join(links)


def page_template(title: str, body: str, current: str, brand: str, description: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="stylesheet" href="styles.css">
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [["\\(", "\\)"], ["$", "$"]],
        displayMath: [["$$", "$$"], ["\\[", "\\]"]]
      }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <header class="header">
    <div class="header-inner">
      <a class="brand" href="index.html">{html.escape(brand)}</a>
      <nav class="nav">{nav(current)}</nav>
    </div>
  </header>
  <main class="container">
    {body}
  </main>
</body>
</html>
"""


def post_template(title: str, body: str, meta: str, brand: str, description: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} | {html.escape(brand)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="stylesheet" href="../styles.css">
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [["\\(", "\\)"], ["$", "$"]],
        displayMath: [["$$", "$$"], ["\\[", "\\]"]]
      }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <header class="header">
    <div class="header-inner">
      <a class="brand" href="../index.html">{html.escape(brand)}</a>
      <nav class="nav">
        <a href="../index.html">Posts</a>
        <a href="../archive.html">Archive</a>
        <a href="../about.html">About</a>
      </nav>
    </div>
  </header>
  <main class="container">
    <article class="post-page">
      <h1>{html.escape(title)}</h1>
      <div class="meta">{html.escape(meta)}</div>
      {body}
    </article>
  </main>
</body>
</html>
"""


def build_index(site: dict[str, object], home_html: str, posts: list[dict[str, str]]) -> str:
    cards = []
    for post in posts:
        cards.append(
            f"""
      <article class="post-card">
        <h2><a href="posts/{post['slug']}.html">{html.escape(post['title'])}</a></h2>
        <p>{html.escape(post['summary'])}</p>
        <div class="meta">{html.escape(post['date'])} · {html.escape(post['tag'])} · {html.escape(post['reading_time'])}</div>
      </article>
"""
        )

    links_html = ""
    for item in site["links"]:
        links_html += f'<a href="{html.escape(item["href"])}">{html.escape(item["label"])}</a>'

    body = f"""
    <section class="intro">
      {home_html}
      <div class="links">{links_html}</div>
    </section>
    <section class="posts">
      {''.join(cards)}
    </section>
"""
    return page_template(
        title=f"{site['author']} | {site['brand']}",
        body=body,
        current="index.html",
        brand=str(site["brand"]),
        description=str(site["description"]),
    )


def build_archive(site: dict[str, object], posts: list[dict[str, str]]) -> str:
    items = []
    for post in posts:
        items.append(
            f"""
      <article class="archive-item">
        <div class="archive-date">{html.escape(post['date'])}</div>
        <div>
          <a href="posts/{post['slug']}.html">{html.escape(post['title'])}</a>
          <p>{html.escape(post['tag'])}</p>
        </div>
      </article>
"""
        )

    body = f"""
    <section class="page-heading">
      <h1>Archive</h1>
      <p>把写过的内容按时间放在一起，方便回看自己的学习路径。</p>
    </section>
    <section class="archive-list">
      {''.join(items)}
    </section>
"""
    return page_template(
        title=f"Archive | {site['brand']}",
        body=body,
        current="archive.html",
        brand=str(site["brand"]),
        description="博客归档页面。",
    )


def build_about(site: dict[str, object], about_html: str) -> str:
    body = f"""
    <article class="post-page">
      {about_html}
    </article>
"""
    return page_template(
        title=f"About | {site['brand']}",
        body=body,
        current="about.html",
        brand=str(site["brand"]),
        description="关于作者。",
    )


def build_post(site: dict[str, object], post: dict[str, str]) -> str:
    meta = " · ".join(part for part in [post["date"], post["tag"], post["reading_time"]] if part)
    return post_template(
        title=post["title"],
        body=post["body_html"],
        meta=meta,
        brand=str(site["brand"]),
        description=post["summary"],
    )


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def remove_stale_post_files(posts: list[dict[str, str]]) -> None:
    OUTPUT_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    valid_names = {f"{post['slug']}.html" for post in posts}
    for path in OUTPUT_POSTS_DIR.glob("*.html"):
        if path.name not in valid_names:
            path.unlink()


def main() -> None:
    site = load_site()
    posts = load_posts()
    home_html = load_home()
    about_html = load_about()

    remove_stale_post_files(posts)
    write_file(ROOT / "index.html", build_index(site, home_html, posts))
    write_file(ROOT / "archive.html", build_archive(site, posts))
    write_file(ROOT / "about.html", build_about(site, about_html))

    for post in posts:
        write_file(slug_to_output(post["slug"]), build_post(site, post))

    print("Built blog from Markdown sources.")


if __name__ == "__main__":
    main()
