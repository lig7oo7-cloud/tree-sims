#!/usr/bin/env python3
"""src/<slug>.html 조각 파일을 공통 틀(build/shell.html)에 넣어 sims/<slug>.html 단독 파일로 만든다.

조각 파일 형식:
<!--meta
{"id": "...", "title": "...", "subject": "나무의사", "unit": "...", "summary": "...",
 "added": "YYYY-MM-DD", "headline": "...", "sub": "..."}
-->
<!--@intro--> ...HTML
<!--@sim--> ...HTML
<!--@js--> ...JavaScript
<!--@teacher--> ...HTML
<!--@quiz--> [{"q": "...", "o": ["..."], "a": 0, "e": "..."}]

사용: python3 build/build.py            (src 전체 빌드 + list.json 갱신)
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHELL = (ROOT / "build" / "shell.html").read_text(encoding="utf-8")
SECTIONS = ["intro", "sim", "js", "teacher", "quiz"]


def parse(path):
    s = path.read_text(encoding="utf-8")
    m = re.search(r"<!--meta\s*(\{.*?\})\s*-->", s, re.S)
    if not m:
        raise SystemExit(f"{path.name}: meta 없음")
    meta = json.loads(m.group(1))
    parts = {}
    for i, name in enumerate(SECTIONS):
        start = s.index(f"<!--@{name}-->") + len(f"<!--@{name}-->")
        end = s.index(f"<!--@{SECTIONS[i+1]}-->") if i + 1 < len(SECTIONS) else len(s)
        parts[name] = s[start:end].strip()
    quiz = json.loads(parts["quiz"])
    assert len(quiz) == 4, f"{path.name}: 쪽지시험은 4문제"
    for q in quiz:
        assert 0 <= q["a"] < len(q["o"]), f"{path.name}: 정답 번호 오류"
    parts["quiz"] = json.dumps(quiz, ensure_ascii=False)
    return meta, parts


def build_one(path):
    meta, parts = parse(path)
    out = SHELL
    for k in ("title", "headline", "sub"):
        out = out.replace("{{" + k + "}}", meta[k])
    for k, v in parts.items():
        out = out.replace("{{" + k + "}}", v)
    dest = ROOT / "sims" / f"{meta['id']}.html"
    dest.write_text(out, encoding="utf-8")
    return meta


def main():
    metas = [build_one(p) for p in sorted((ROOT / "src").glob("*.html"))]
    lst_path = ROOT / "list.json"
    lst = json.loads(lst_path.read_text(encoding="utf-8"))
    by_id = {x["id"]: x for x in lst}
    for m in metas:
        by_id[m["id"]] = {k: m[k] for k in ("id", "title", "subject", "unit", "summary", "added")} | {"file": f"sims/{m['id']}.html"}
    order = [x["id"] for x in lst] + [m["id"] for m in metas if m["id"] not in {x["id"] for x in lst}]
    new = [by_id[i] for i in order]
    lst_path.write_text("[\n" + ",\n".join("  " + json.dumps(x, ensure_ascii=False) for x in new) + "\n]\n", encoding="utf-8")
    print(f"built {len(metas)} sims; list has {len(new)}")


if __name__ == "__main__":
    main()
