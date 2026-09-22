#!/usr/bin/env python3
"""Commitments: one-note-per-task tracking, shared by the sod/eod/todo skills.

Stdlib only by design — PyYAML is not installed and must not be added.
Standalone: no imports from sod.py or any other skill's script. sod.py
shells out to this script's CLI exactly like it shells out to `gh`/`short`.
"""
import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path

VAULT = Path(os.environ.get("COMMITMENTS_VAULT", "/Users/luke.snyder/code/Vaults/Work"))
COMMITMENTS_DIR = VAULT / "Commitments"

COMPLEXITY_RANK = {"low": 0, "medium": 1, "high": 2}
MISSING_RANK = 3
FAR_FUTURE = dt.date(9999, 12, 31)


def today():
    return dt.date.today()


def parse_date(value):
    if not value:
        return None
    if isinstance(value, dt.date):
        return value
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(value))
    return dt.date(int(m[1]), int(m[2]), int(m[3])) if m else None


def complexity_rank(value):
    return COMPLEXITY_RANK.get(value, MISSING_RANK)


# --- frontmatter -------------------------------------------------------------
# Flat scalars and simple block lists only. The script writes every field it
# reads back, so the grammar stays small; the one externally-edited field is
# `status`, which Obsidian Bases writes as a plain scalar.

def _parse_scalar(raw):
    raw = raw.strip()
    if raw in ("", "null", "~"):
        return None
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1].replace('\\"', '"')
    if raw == "[]":
        return []
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if raw in ("true", "false"):
        return raw == "true"
    return raw


def read_note(path):
    text = Path(path).read_text()
    out = {"_body": text, "_path": Path(path)}
    if not text.startswith("---\n"):
        return out
    end = text.find("\n---", 3)
    if end == -1:
        return out
    block, body = text[4:end], text[end + 4:]
    out["_body"] = body.lstrip("\n")
    key = None
    for line in block.splitlines():
        if re.match(r"^\s*-\s", line) and key is not None:
            item = _parse_scalar(line.split("-", 1)[1])
            if item is not None:
                out.setdefault(key, [])
                if isinstance(out[key], list):
                    out[key].append(item)
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", line)
        if not m:
            continue
        key, rest = m[1], m[2]
        out[key] = [] if rest.strip() == "" else _parse_scalar(rest)
    return out


def _emit_scalar(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    s = str(value)
    if s == "" or re.search(r'[:#\[\]{}"\']', s) or s != s.strip():
        return '"' + s.replace('"', '\\"') + '"'
    return s


def write_note(path, fm, body=""):
    lines = ["---"]
    for key, value in fm.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                lines.extend(f"  - {_emit_scalar(v)}" for v in value)
        else:
            lines.append(f"{key}: {_emit_scalar(value)}")
    lines += ["---", "", body.rstrip("\n"), ""]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def assign_sort_keys(notes, key_fn):
    ordered = sorted(notes, key=key_fn)
    for index, note in enumerate(ordered):
        note["sort_key"] = index
    return ordered


def slugify(text, limit=60):
    slug = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return (slug[:limit].rstrip("-")) or "commitment"


COMMITMENT_FIELDS = ("title", "committed_date", "due_date", "complexity",
                     "tags", "summary", "link", "status", "sort_key")


def load_commitments(include_done=False):
    if not COMMITMENTS_DIR.exists():
        return []
    notes = [read_note(p) for p in sorted(COMMITMENTS_DIR.glob("*.md"))]
    notes = [n for n in notes if n.get("link")]
    if not include_done:
        notes = [n for n in notes if n.get("status", "open") != "done"]
    return notes


def _tokens(title):
    words = re.findall(r"[a-z0-9]+", str(title).lower())
    return {w for w in words if len(w) >= 4}


def similar_title(a, b, threshold=0.6):
    """Crude Jaccard overlap on long tokens. The agent has already judged these
    candidates; this only has to catch obvious cross-day restatements."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= threshold


def commitment_sort_tuple(note, ref):
    """Overdue pinned first, then due_date asc, then complexity asc.
    Missing complexity sorts last within its tier."""
    due = parse_date(note.get("due_date"))
    if due is None:
        tier = 2
    elif due < ref:
        tier = 0
    else:
        tier = 1
    return (tier, due or FAR_FUTURE,
            complexity_rank(note.get("complexity")), str(note.get("title", "")))


def upsert_commitment(title, summary, link, committed_date,
                      due_date=None, complexity=None, tags=None, body=None):
    COMMITMENTS_DIR.mkdir(parents=True, exist_ok=True)
    existing = load_commitments(include_done=True)

    # Same permalink: a same-day re-run rescanning the same window.
    for note in existing:
        if note.get("link") == link:
            return "duplicate", note["_path"]

    # Different permalink, same underlying commitment restated on a later day.
    # Only due_date is ever overwritten, so nothing is destroyed on a false hit.
    for note in existing:
        if note.get("status", "open") == "done":
            continue
        if similar_title(note.get("title", ""), title):
            fields = {k: note.get(k) for k in COMMITMENT_FIELDS}
            if due_date and fields.get("due_date") != due_date:
                fields["due_date"] = due_date
                write_note(note["_path"], fields, note.get("_body", ""))
            return "updated", note["_path"]

    stem = f"{committed_date}-{slugify(title)}"
    path = COMMITMENTS_DIR / f"{stem}.md"
    suffix = 2
    while path.exists():
        path = COMMITMENTS_DIR / f"{stem}-{suffix}.md"
        suffix += 1

    write_note(path, {
        "title": str(title)[:150],
        "committed_date": committed_date,
        "due_date": due_date,
        "complexity": complexity,
        "tags": list(tags or []),
        "summary": str(summary)[:500],
        "link": link,
        "status": "open",
        "sort_key": 0,
    }, body if body else f"[Original]({link})\n")
    return "created", path


def cmd_commitments(ref=None):
    ref = ref or today()
    notes = load_commitments()
    for note in assign_sort_keys(notes, lambda n: commitment_sort_tuple(n, ref)):
        fields = {k: note.get(k) for k in COMMITMENT_FIELDS}
        fields["sort_key"] = note["sort_key"]
        write_note(note["_path"], fields, note.get("_body", ""))
    return f"Commitments: {len(notes)} open, sort keys recomputed"


def cmd_commit_add(args):
    action, path = upsert_commitment(
        title=args.title, summary=args.summary, link=args.link,
        committed_date=args.committed_date, due_date=args.due_date,
        complexity=args.complexity, body=args.body,
        tags=[t.strip() for t in args.tags.split(",") if t.strip()])
    return f"{action}: {path}"


def main(argv=None):
    parser = argparse.ArgumentParser(prog="commitments")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("commit-add", help="create or update one commitment")
    add.add_argument("--title", required=True)
    add.add_argument("--summary", required=True)
    add.add_argument("--link", required=True)
    add.add_argument("--committed-date", required=True, dest="committed_date")
    add.add_argument("--due-date", dest="due_date")
    add.add_argument("--complexity", choices=["low", "medium", "high"])
    add.add_argument("--tags", default="", help="comma-separated")
    add.add_argument("--body", help="note body; defaults to a link back to the source")
    sub.add_parser("commitments", help="recompute open-commitment sort keys")
    args = parser.parse_args(argv)
    if args.cmd == "commit-add":
        print(cmd_commit_add(args))
    elif args.cmd == "commitments":
        print(cmd_commitments())


if __name__ == "__main__":
    main()
