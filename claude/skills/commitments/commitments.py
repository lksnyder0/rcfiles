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


def main(argv=None):
    parser = argparse.ArgumentParser(prog="commitments")
    parser.parse_args(argv)


if __name__ == "__main__":
    main()
