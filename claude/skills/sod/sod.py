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
# Four selection criteria, merged and deduped by (repo, number). `author` is
# never queried. `review-requested @me` covers direct requests of me,
# separate from the two team criteria.

PR_FIELDS = "number,title,url,createdAt,isDraft"

PR_QUERIES = [
    ("review-requested", True, [
        "gh", "search", "prs", "--review-requested", "@me", "--state", "open",
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
PROJECT_FIELDS = ("type", "id", "title", "state", "state_type", "epic_id",
                  "created_at", "due_date", "complexity", "blocker", "link",
                  "epic_group", "sort_key")


def short_api(path, **params):
    args = ["short", "api", path]
    for key, value in params.items():
        args += ["-f", f"{key}={value}"]
    return json.loads(sh(args))


def workflow_states():
    """{state_id: {"name", "type"}} across every workflow. One fetch per run."""
    return {
        state["id"]: {"name": state["name"], "type": state["type"]}
        for workflow in short_api("/workflows")
        for state in workflow["states"]
    }


def done_state_ids(states=None):
    """State ids whose workflow-state `type` is 'done'. Never match on state
    name: 'Blocked' is `unstarted` in one workflow and `started` in another."""
    states = states if states is not None else workflow_states()
    return {sid for sid, s in states.items() if s["type"] == "done"}


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
    states = workflow_states()
    done = done_state_ids(states)

    stories = []
    for s in search_stories(f"owner:{mention} !is:done"):
        if s["workflow_state_id"] in done:
            continue  # belt and braces behind `!is:done`
        state = states.get(s["workflow_state_id"], {})
        stories.append({
            "type": "story",
            "id": s["id"],
            "title": s["name"],
            "state": state.get("name", ""),
            "state_type": state.get("type"),
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
            "state_type": None,  # epic states are their own vocabulary
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


# --- OPEN COMMITMENTS --------------------------------------------------------
# One note per row. The agent judges what is a commitment; this half owns dedup
# and ordering. `link` (Slack permalink or Gmail message URL) is the row key.

COMMITMENT_FIELDS = ("title", "committed_date", "due_date", "complexity",
                     "tags", "summary", "link", "status", "sort_key")


def slugify(text, limit=60):
    slug = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return (slug[:limit].rstrip("-")) or "commitment"


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


# --- IMPORTANT TODAY/THIS WEEK -----------------------------------------------
# Merges the two Bases with active TODOs, so it cannot be a Base query. Only
# stories are eligible from PROJECT WORK: an epic is not an atomic item that
# could be finished this week.

TODO_SECTIONS = ("Today", "Backlog")
TODO_DUE_RE = re.compile(r"due\s*\[\[(\d{4}-\d{2}-\d{2})\]\]")
SOURCE_RANK = {"commitment": 0, "project": 1, "todo": 2}

# Four bands, in render order. Shortcut estimates and deadlines are mostly
# unset in practice, so ranking undated stories on due_date/complexity alone
# collapses to story id — state is the signal that actually exists.
#
#   0  overdue, any source          due_date asc, complexity asc, source order
#   1  started stories             closest due_date first, undated last
#   2  unstarted stories           complexity asc
#   3  everything else             due_date asc, complexity asc, source order
#
# `backlog` stories are dropped outright: they still need shaping, so they are
# not an answer to "what could I finish this week". A missing or unrecognised
# state type is NOT dropped — it lands in band 2 behind real unstarted work,
# because silently losing a story is worse than mis-ranking it.
BAND_OVERDUE, BAND_STARTED, BAND_UNSTARTED, BAND_REST = 0, 1, 2, 3
STORY_BAND = {"started": BAND_STARTED, "unstarted": BAND_UNSTARTED}
EXCLUDED_STATE_TYPES = {"backlog"}
STATE_RANK = {"started": 0, "unstarted": 1}
STATE_MISSING_RANK = 2
NO_DUE_ORD = 10 ** 7


def state_rank(state_type):
    return STATE_RANK.get(state_type, STATE_MISSING_RANK)


def _due_ord(value):
    """Date as a sortable int, undated sorting last. Keeping every tuple slot
    an int means bands can reuse slots for different fields safely."""
    due = parse_date(value)
    return due.toordinal() if due else NO_DUE_ORD


TODO_LINK_PREFIX = "todo://"
# Any indented checkbox is a child. TODO.md mixes tab and two-space nesting,
# so match on "is there leading whitespace" rather than a fixed width.
TODO_CHILD_RE = re.compile(r"^[ \t]+- \[[ xX]\] ")


def todo_link(text):
    """Stable synthetic row key for a TODO-sourced commitment.

    Derived from the raw TODO line, never from the commitment's title, so the
    commitment can be retitled freely and the migration still recognises it
    instead of creating a second row.
    """
    return TODO_LINK_PREFIX + slugify(text, limit=80)


def load_todos():
    """Open root checkboxes under ## Today / ## Backlog, each carrying its
    sub-bullets in `children`.

    Only roots are pool-eligible — sub-items are implementation detail and
    would flood it. `children` exists so a TODO migrated into a commitment can
    carry its sub-bullets into the note body; completed children come along
    too, since they are context worth keeping.
    """
    if not TODO_PATH.exists():
        return []
    section, todos, collecting = None, [], False
    for line in TODO_PATH.read_text().splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            section, collecting = heading[1], False
            continue
        if section not in TODO_SECTIONS:
            continue
        if TODO_CHILD_RE.match(line):
            # Only claim children while the enclosing root is one we kept;
            # otherwise a completed root's sub-bullets would graft themselves
            # onto the previous open item.
            if collecting:
                todos[-1]["children"].append(line.strip())
            continue
        if not line.strip():
            continue  # blank lines inside a group are not a boundary
        if not line.startswith("- [ ] "):
            collecting = False
            continue
        text = line[6:].strip()
        due = TODO_DUE_RE.search(text)
        todos.append({"label": text, "due_date": due[1] if due else None,
                      "complexity": None, "link": todo_link(text),
                      "children": []})
        collecting = True
    return todos


def load_project_stories():
    if not PROJECT_DIR.exists():
        return []
    notes = [read_note(p) for p in sorted(PROJECT_DIR.glob("*.md"))]
    return [n for n in notes if n.get("type") == "story"]


def important_pool(ref=None):
    ref = ref or today()
    pool = []
    for note in load_commitments():
        pool.append({"label": note.get("title", ""), "source": "commitment",
                     "due_date": note.get("due_date"),
                     "complexity": note.get("complexity"),
                     "state_type": None,
                     "link": note.get("link")})
    for note in load_project_stories():
        if note.get("state_type") in EXCLUDED_STATE_TYPES:
            continue
        pool.append({"label": note.get("title", ""), "source": "project",
                     "due_date": note.get("due_date"),
                     "complexity": note.get("complexity"),
                     "state_type": note.get("state_type"),
                     "link": note.get("link")})
    # TODO.md is left intact when items are migrated into Commitments, so a
    # migrated TODO would otherwise be counted twice. Match on the synthetic
    # todo:// row key, which is exact — no title guessing. Done commitments
    # count as migrated too, or completing one would resurrect the TODO.
    migrated = {n.get("link") for n in load_commitments(include_done=True)}
    for todo in load_todos():
        if todo["link"] in migrated:
            continue
        pool.append({"label": todo["label"], "source": "todo",
                     "due_date": todo["due_date"], "complexity": None,
                     "state_type": None, "link": None})

    def key(item):
        due = parse_date(item["due_date"])
        due_ord = _due_ord(item["due_date"])
        cx = complexity_rank(item["complexity"])
        src = SOURCE_RANK[item["source"]]

        # Overdue wins outright, whatever the source or state.
        if due and due < ref:
            return (BAND_OVERDUE, due_ord, cx, src, 0)
        if item["source"] == "project":
            band = STORY_BAND.get(item["state_type"], BAND_UNSTARTED)
            if band == BAND_STARTED:
                return (BAND_STARTED, due_ord, cx, 0, 0)
            # Unstarted: complexity leads, due date only breaks its ties.
            return (BAND_UNSTARTED, cx, due_ord, state_rank(item["state_type"]), 0)
        return (BAND_REST, due_ord, cx, src, 0)

    for item in pool:
        due = parse_date(item["due_date"])
        item["overdue"] = bool(due and due < ref)
    return sorted(pool, key=key)


def render_important(items):
    if not items:
        return "_Nothing ranked — commitments, project work, and TODOs are all empty._"
    lines = []
    for item in items:
        bits = [item["source"]]
        if item["due_date"]:
            bits.append(("overdue " if item["overdue"] else "due ") + item["due_date"])
        if item["complexity"]:
            bits.append(item["complexity"])
        if item["state_type"]:
            bits.append(item["state_type"])
        label = f"[{item['label']}]({item['link']})" if item["link"] else item["label"]
        lines.append(f"- [ ] {label} ({', '.join(bits)})")
    return "\n".join(lines)


def cmd_important(ref=None, limit=5):
    return render_important(important_pool(ref)[:limit])


def cmd_todos():
    """Read-only inventory for driving a migration into Commitments. Prints the
    todo:// key so the same dedup the pool uses can be reproduced by hand."""
    migrated = {n.get("link") for n in load_commitments(include_done=True)}
    out = []
    for todo in load_todos():
        flag = "MIGRATED" if todo["link"] in migrated else "open"
        out.append(f"[{flag}] {todo['link']}")
        out.append(f"    {todo['label']}")
        if todo["due_date"]:
            out.append(f"    due: {todo['due_date']}")
        for child in todo["children"]:
            out.append(f"      {child}")
    return "\n".join(out) or "_No open root TODOs._"


# --- daily note --------------------------------------------------------------
# Only these four sections are touched, so re-running is safe and the sections
# `eod` appends later in the day survive untouched.

SECTION_ORDER = ["IMPORTANT TODAY/THIS WEEK", "OPEN COMMITMENTS",
                 "PR REVIEW BACKLOG", "PROJECT WORK"]
DAILY_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})\.md$")


def daily_note_path(day):
    return DAILY_DIR / f"{day:%Y}" / f"{day:%m-%B}" / f"{day:%Y-%m-%d}.md"


def latest_daily_date(before=None):
    before = before or today()
    dates = []
    for path in DAILY_DIR.rglob("*.md"):
        m = DAILY_RE.search(path.name)
        if not m:
            continue
        found = dt.date(int(m[1]), int(m[2]), int(m[3]))
        if found < before:
            dates.append(found)
    return max(dates) if dates else None


def cmd_window():
    """Oldest timestamp for the Slack/Gmail searches: the most recent daily
    note strictly before today, else yesterday on a first-ever run."""
    return str(latest_daily_date() or (today() - dt.timedelta(days=1)))


def upsert_section(text, heading, body):
    marker = f"## {heading}"
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip() == marker), None)
    if start is None:
        joined = text.rstrip("\n")
        prefix = (joined + "\n\n") if joined else ""
        out = f"{prefix}{marker}\n\n{body.rstrip()}"
    else:
        end = next((i for i in range(start + 1, len(lines))
                    if lines[i].startswith("## ")), len(lines))
        out = "\n".join(lines[:start + 1] + ["", body.rstrip(), ""] + lines[end:])
    # Both branches normalize here: otherwise appending vs. replacing the last
    # section leaves a different trailing-newline count and re-runs drift.
    return out.rstrip("\n") + "\n"


def cmd_daily_note(day=None):
    day = day or today()
    path = daily_note_path(day)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text() if path.exists() else ""
    bodies = {
        "IMPORTANT TODAY/THIS WEEK": cmd_important(),
        "OPEN COMMITMENTS": "![[Commitments.base#Daily Note View]]",
        "PR REVIEW BACKLOG": cmd_prs(),
        "PROJECT WORK": "![[Project Work.base#Daily Note View]]",
    }
    # Iterating in SECTION_ORDER means a fresh note gets the four headings
    # appended in spec order; an existing note keeps whatever order it has.
    for heading in SECTION_ORDER:
        text = upsert_section(text, heading, bodies[heading])
    path.write_text(text)
    return f"Daily note written: {path}"


def main(argv=None):
    parser = argparse.ArgumentParser(prog="sod")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prs", help="render the PR REVIEW BACKLOG table")
    sub.add_parser("project-work", help="regenerate the Project Work Base")
    sub.add_parser("commitments", help="recompute open-commitment sort keys")
    add = sub.add_parser("commit-add", help="create or update one commitment")
    add.add_argument("--title", required=True)
    add.add_argument("--summary", required=True)
    add.add_argument("--link", required=True)
    add.add_argument("--committed-date", required=True, dest="committed_date")
    add.add_argument("--due-date", dest="due_date")
    add.add_argument("--complexity", choices=["low", "medium", "high"])
    add.add_argument("--tags", default="", help="comma-separated")
    add.add_argument("--body", help="note body; defaults to a link back to the source")
    sub.add_parser("todos", help="list open root TODOs with their todo:// keys")
    imp = sub.add_parser("important", help="render IMPORTANT TODAY/THIS WEEK")
    imp.add_argument("--limit", type=int, default=5)
    sub.add_parser("window", help="print the Slack/Gmail search cutoff date")
    sub.add_parser("daily-note", help="write today's four SOD sections")
    args = parser.parse_args(argv)
    if args.cmd == "prs":
        print(cmd_prs())
    elif args.cmd == "project-work":
        print(cmd_project_work())
    elif args.cmd == "commitments":
        print(cmd_commitments())
    elif args.cmd == "commit-add":
        print(cmd_commit_add(args))
    elif args.cmd == "important":
        print(cmd_important(limit=args.limit))
    elif args.cmd == "todos":
        print(cmd_todos())
    elif args.cmd == "window":
        print(cmd_window())
    elif args.cmd == "daily-note":
        print(cmd_daily_note())


if __name__ == "__main__":
    main()
