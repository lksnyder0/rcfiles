#!/usr/bin/env python3
"""Start-of-day: seed the four-section daily note and regenerate its two Bases.

Stdlib only by design — PyYAML is not installed and must not be added.
This script owns every deterministic decision; the SOD skill only supplies
human-judged commitments via `commit-add`.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path

VAULT = Path(os.environ.get("SOD_VAULT", "/Users/luke.snyder/code/Vaults/Work"))
COMMITMENTS_DIR = VAULT / "Commitments"
PROJECT_DIR = VAULT / "Project Work"
TODO_PATH = VAULT / "TODO.md"
DAILY_DIR = VAULT / "Daily notes"

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


def sh(args):
    """Run a command, return stdout. stderr is discarded: `short` writes a
    progress spinner there that would otherwise corrupt JSON parsing."""
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


# --- PR REVIEW BACKLOG -------------------------------------------------------
# Four selection criteria, merged and deduped by (repo, number). "Assigned
# directly to me" is GitHub's `assignee` — never `author`, and never
# `review-requested`, which the two team criteria already cover.

PR_FIELDS = "number,title,url,createdAt,isDraft"

PR_QUERIES = [
    ("assignee", True, [
        "gh", "search", "prs", "--assignee", "@me", "--state", "open",
        "--owner", "huntresslabs", "--json", PR_FIELDS + ",repository",
        "--limit", "100"]),
    ("team:infrastructure-sre", False, [
        "gh", "search", "prs", "--review-requested", "huntresslabs/infrastructure-sre",
        "--state", "open", "--owner", "huntresslabs",
        "--json", PR_FIELDS + ",repository", "--limit", "100"]),
    ("team:idex", False, [
        "gh", "search", "prs", "--review-requested", "huntresslabs/idex",
        "--state", "open", "--owner", "huntresslabs",
        "--json", PR_FIELDS + ",repository", "--limit", "100"]),
    ("repo:infra-elastic", False, [
        "gh", "pr", "list", "--repo", "huntresslabs/infra-elastic",
        "--state", "open", "--json", PR_FIELDS, "--limit", "100"]),
]


def gh_json(args):
    return json.loads(sh(args) or "[]")


def collect_prs():
    merged = {}
    for reason, keep_drafts, args in PR_QUERIES:
        for raw in gh_json(args):
            if raw.get("isDraft") and not keep_drafts:
                continue
            # `gh pr list` omits the repository field; that query is repo-scoped.
            repo = (raw.get("repository") or {}).get("nameWithOwner") \
                or "huntresslabs/infra-elastic"
            row = merged.setdefault((repo, raw["number"]), {
                "repo": repo,
                "number": raw["number"],
                "title": raw["title"],
                "url": raw["url"],
                "created_at": parse_date(raw["createdAt"]),
                "is_draft": bool(raw.get("isDraft")),
                "reasons": set(),
            })
            row["reasons"].add(reason)
    prs = sorted(merged.values(), key=lambda p: (p["created_at"], p["repo"], p["number"]))
    for pr in prs:
        pr["reasons"] = sorted(pr["reasons"])
    return prs


def render_prs(prs):
    if not prs:
        return "_No open PRs matching the backlog criteria._"
    lines = ["| PR | Title | Opened | Why |", "| --- | --- | --- | --- |"]
    for pr in prs:
        short_repo = pr["repo"].split("/", 1)[1]
        draft = " *(draft)*" if pr["is_draft"] else ""
        title = pr["title"].replace("|", "\\|")
        lines.append(
            f"| [{short_repo}#{pr['number']}]({pr['url']}){draft} | {title} "
            f"| {pr['created_at']} | {', '.join(pr['reasons'])} |"
        )
    return "\n".join(lines)


def cmd_prs():
    return render_prs(collect_prs())


# --- PROJECT WORK ------------------------------------------------------------
# Fully regenerated from Shortcut each run, so closed or reassigned stories and
# the epics they leave empty disappear without any delete bookkeeping.

NO_EPIC_RANK = 99
NO_EPIC_LABEL = "No epic"
PROJECT_FIELDS = ("type", "id", "title", "state", "epic_id", "created_at",
                  "due_date", "complexity", "blocker", "link", "epic_group",
                  "sort_key")


def short_api(path, **params):
    args = ["short", "api", path]
    for key, value in params.items():
        args += ["-f", f"{key}={value}"]
    return json.loads(sh(args))


def done_state_ids():
    """State ids whose workflow-state `type` is 'done'. Never match on state
    name: 'Blocked' is `unstarted` in one workflow and `started` in another."""
    return {
        state["id"]
        for workflow in short_api("/workflows")
        for state in workflow["states"]
        if state["type"] == "done"
    }


def _state_names():
    return {
        state["id"]: state["name"]
        for workflow in short_api("/workflows")
        for state in workflow["states"]
    }


def search_stories(query):
    """Shortcut caps search page_size at 25, so follow the `next` cursor.
    20 stories today, but this must not silently truncate at 26."""
    stories, params = [], {"query": query, "page_size": 25}
    while True:
        page = short_api("/search/stories", **params)
        stories.extend(page.get("data") or [])
        cursor = page.get("next")
        if not cursor:
            return stories
        token = re.search(r"next=([^&]+)", str(cursor))
        if not token:
            return stories
        params = {"query": query, "page_size": 25, "next": token[1]}


def estimate_to_complexity(estimate):
    if estimate is None:
        return None
    if estimate <= 1:
        return "low"
    if estimate <= 3:
        return "medium"
    return "high"


def fetch_project_work():
    mention = short_api("/member")["mention_name"]
    done = done_state_ids()
    names = _state_names()

    stories = []
    for s in search_stories(f"owner:{mention} !is:done"):
        if s["workflow_state_id"] in done:
            continue  # belt and braces behind `!is:done`
        stories.append({
            "type": "story",
            "id": s["id"],
            "title": s["name"],
            "state": names.get(s["workflow_state_id"], ""),
            "epic_id": s.get("epic_id"),
            "created_at": parse_date(s["created_at"]),
            "due_date": parse_date(s.get("deadline")),
            "complexity": estimate_to_complexity(s.get("estimate")),
            "blocker": bool(s.get("blocker")),
            "link": s["app_url"],
        })

    epics = []
    for epic_id in sorted({s["epic_id"] for s in stories if s["epic_id"]}):
        e = short_api(f"/epics/{epic_id}")
        epics.append({
            "type": "epic",
            "id": e["id"],
            "title": e["name"],
            "state": e.get("state", ""),
            "epic_id": None,
            "created_at": parse_date(e["created_at"]),
            "due_date": parse_date(e.get("deadline")),
            "complexity": None,
            "blocker": False,
            "link": e["app_url"],
        })
    return epics, stories


def _story_order(story):
    """Blockers first, then due_date asc, then complexity asc."""
    return (0 if story["blocker"] else 1,
            story["due_date"] or FAR_FUTURE,
            complexity_rank(story["complexity"]),
            story["id"])


def order_project_work(epics, stories):
    ranked = sorted(epics, key=lambda e: (
        0 if e["due_date"] else 1,
        e["due_date"] or FAR_FUTURE,
        e["created_at"],
        e["id"],
    ))
    rows = []
    for rank, epic in enumerate(ranked):
        # The numeric prefix makes Bases' alphabetical group ordering reproduce
        # the epic ranking computed here.
        group = f"{rank:02d} — {epic['title']}"
        epic["epic_group"] = group
        rows.append(epic)
        kids = [s for s in stories if s["epic_id"] == epic["id"]]
        for story in sorted(kids, key=_story_order):
            story["epic_group"] = group
            rows.append(story)

    group = f"{NO_EPIC_RANK:02d} — {NO_EPIC_LABEL}"
    for story in sorted((s for s in stories if not s["epic_id"]), key=_story_order):
        story["epic_group"] = group
        rows.append(story)

    for index, row in enumerate(rows):
        row["sort_key"] = index
    return rows


def _clear_generated(directory, types):
    """Only unlink notes this script owns — anything a human dropped in the
    folder has no `type: epic|story` and survives."""
    for path in directory.glob("*.md"):
        if read_note(path).get("type") in types:
            path.unlink()


def cmd_project_work():
    epics, stories = fetch_project_work()
    rows = order_project_work(epics, stories)
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    _clear_generated(PROJECT_DIR, {"epic", "story"})
    for row in rows:
        fields = {k: row.get(k) for k in PROJECT_FIELDS}
        fields["created_at"] = str(row["created_at"]) if row["created_at"] else None
        fields["due_date"] = str(row["due_date"]) if row["due_date"] else None
        write_note(PROJECT_DIR / f"{row['type']}-{row['id']}.md", fields,
                   f"[{row['title']}]({row['link']})\n")
    n_epics = sum(1 for r in rows if r["type"] == "epic")
    return f"Project Work: {n_epics} epics, {len(rows) - n_epics} stories"


def main(argv=None):
    parser = argparse.ArgumentParser(prog="sod")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prs", help="render the PR REVIEW BACKLOG table")
    sub.add_parser("project-work", help="regenerate the Project Work Base")
    args = parser.parse_args(argv)
    if args.cmd == "prs":
        print(cmd_prs())
    elif args.cmd == "project-work":
        print(cmd_project_work())


if __name__ == "__main__":
    main()
