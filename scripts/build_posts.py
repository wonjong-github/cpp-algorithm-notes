#!/usr/bin/env python3
"""cheatsheet.md를 Jekyll 블로그 글(_posts/)로 나눈다.

- "## 1. ~ ## 5." 장 → 주제별 노트 글 (categories: notes)
- "## 6." 장의 "### Qn." → Q&A 글 하나씩 (categories: qna)

치트시트를 고친 뒤 실행:  python3 scripts/build_posts.py
"""
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "cheatsheet.md"
POSTS = ROOT / "_posts"
DATES = ROOT / "scripts" / "dates.json"

NOTE_SLUGS = {
    1: "basic-template",
    2: "io-patterns",
    3: "stl",
    4: "algorithm-templates",
    5: "cpp-pitfalls",
}

CHAPTER_RE = re.compile(r"^## (\d+)\. (.+)$")
QNA_RE = re.compile(r"^### Q(\d+)\. (.+)$")
HEADING_RE = re.compile(r"^(#{2,6}) (.+)$")
ANCHOR_LINK_RE = re.compile(r"\]\(#([^)]+)\)")


def is_fence(line):
    return line.lstrip().startswith("```")


def anchor(text):
    """GitHub / kramdown(GFM) 스타일 헤더 id."""
    text = text.replace("`", "").strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def strip_blank_edges(lines):
    while lines and lines[-1].strip() in ("", "---"):
        lines.pop()
    while lines and lines[0].strip() == "":
        lines.pop(0)
    return lines


def parse():
    """cheatsheet.md → 글 목록."""
    posts = []
    cur = None
    in_fence = False
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if is_fence(line):
            in_fence = not in_fence
        if not in_fence:
            m = CHAPTER_RE.match(line)
            if m:
                num, title = int(m.group(1)), m.group(2).strip()
                cur = None
                if num in NOTE_SLUGS:
                    cur = {"kind": "notes", "num": num, "title": f"{num}. {title}",
                           "slug": f"{num:02d}-{NOTE_SLUGS[num]}", "key": f"note-{num}",
                           "anchor": anchor(line[3:]), "lines": []}
                    posts.append(cur)
                continue
            m = QNA_RE.match(line)
            if m:
                num = int(m.group(1))
                cur = {"kind": "qna", "num": num, "title": f"Q{num}. {m.group(2).strip()}",
                       "slug": f"q{num:02d}", "key": f"q{num}",
                       "anchor": anchor(line[4:]), "lines": []}
                posts.append(cur)
                continue
        if cur is not None:
            cur["lines"].append(line)

    for p in posts:
        p["lines"] = strip_blank_edges(p["lines"])
        p["url"] = f"{p['kind']}/{p['slug']}/"
    return posts


def shift_headings(lines):
    """### → ## 처럼 한 단계씩 올림 (글 제목이 h1이므로). 코드 블록 안은 그대로."""
    out, in_fence = [], False
    for line in lines:
        if is_fence(line):
            in_fence = not in_fence
        m = None if in_fence else HEADING_RE.match(line)
        if m and len(m.group(1)) >= 3:
            line = line[1:]
        out.append(line)
    return out


def build_anchor_map(posts):
    """헤더 id → (글 url, fragment)."""
    amap = {}
    for p in posts:
        amap[p["anchor"]] = (p["url"], "")
        in_fence = False
        for line in p["lines"]:
            if is_fence(line):
                in_fence = not in_fence
                continue
            m = None if in_fence else HEADING_RE.match(line)
            if m:
                a = anchor(m.group(2))
                amap.setdefault(a, (p["url"], "#" + a))
    return amap


def rewrite_links(post, amap):
    """[텍스트](#anchor) 중 다른 글에 있는 헤더는 그 글로 가는 상대 링크로 바꿈."""
    def repl(m):
        a = m.group(1)
        if a not in amap:
            return m.group(0)
        url, frag = amap[a]
        if url == post["url"]:
            return m.group(0)
        return f"](../../{url}{frag})"

    out, in_fence = [], False
    for line in post["lines"]:
        if is_fence(line):
            in_fence = not in_fence
        out.append(line if in_fence else ANCHOR_LINK_RE.sub(repl, line))
    return out


def load_dates(posts):
    """글마다 처음 생성된 날짜를 기억 (새 글은 오늘 날짜)."""
    dates = json.loads(DATES.read_text()) if DATES.exists() else {}
    today = datetime.date.today().isoformat()
    for p in posts:
        dates.setdefault(p["key"], today)
    DATES.write_text(json.dumps(dates, ensure_ascii=False, indent=2) + "\n")
    return dates


def render(post, dates):
    title = post["title"].replace("`", "")
    # 같은 날짜 글끼리도 번호 순서가 유지되도록 시각에 번호를 반영
    hour = 9 if post["kind"] == "notes" else 12
    time = f"{hour:02d}:{post['num']:02d}:00"
    return "\n".join([
        "---",
        "layout: post",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"date: {dates[post['key']]} {time} +0900",
        f"categories: {post['kind']}",
        f"order: {post['num']}",
        "---",
        # C++ 코드의 {{ }} 가 Liquid 문법으로 해석되지 않도록 raw로 감쌈
        "{% raw %}",
        *shift_headings(post["lines"]),
        "{% endraw %}",
        "",
        "---",
        "",
        "[← 전체 목록](../../)",
        "",
    ])


def main():
    posts = parse()
    amap = build_anchor_map(posts)
    for p in posts:
        p["lines"] = rewrite_links(p, amap)
    dates = load_dates(posts)

    POSTS.mkdir(exist_ok=True)
    for old in POSTS.glob("*.md"):
        old.unlink()
    for p in posts:
        path = POSTS / f"{dates[p['key']]}-{p['slug']}.md"
        path.write_text(render(p, dates), encoding="utf-8")

    notes = sum(p["kind"] == "notes" for p in posts)
    print(f"{len(posts)}개 글 생성 (노트 {notes}, Q&A {len(posts) - notes}) → {POSTS}")


if __name__ == "__main__":
    main()
