import datetime as dt
import os
import tempfile
import unittest
from pathlib import Path

_TMP = tempfile.mkdtemp()
os.environ["SOD_VAULT"] = _TMP

import sod


class TestFrontmatter(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())

    def test_roundtrip_scalars_and_list(self):
        p = self.dir / "a.md"
        fm = {
            "title": "Send Connor the Elastic user info",
            "due_date": "2026-09-16",
            "complexity": "low",
            "tags": ["elasticsearch", "idex"],
            "status": "open",
            "sort_key": 3,
        }
        sod.write_note(p, fm, "body text\n")
        got = sod.read_note(p)
        self.assertEqual(got["title"], fm["title"])
        self.assertEqual(got["tags"], ["elasticsearch", "idex"])
        self.assertEqual(got["sort_key"], 3)
        self.assertEqual(got["status"], "open")
        self.assertIn("body text", got["_body"])
        self.assertEqual(got["_path"], p)

    def test_colon_in_value_is_quoted_and_survives(self):
        p = self.dir / "b.md"
        sod.write_note(p, {"title": "Fix: the thing", "link": "https://x/y?a=1"}, "")
        got = sod.read_note(p)
        self.assertEqual(got["title"], "Fix: the thing")
        self.assertEqual(got["link"], "https://x/y?a=1")

    def test_empty_list_and_null(self):
        p = self.dir / "c.md"
        sod.write_note(p, {"tags": [], "epic_id": None}, "")
        got = sod.read_note(p)
        self.assertEqual(got["tags"], [])
        self.assertIsNone(got["epic_id"])

    def test_reads_human_edited_status_toggle(self):
        p = self.dir / "d.md"
        p.write_text("---\ntitle: x\nstatus: done\n---\n\n")
        self.assertEqual(sod.read_note(p)["status"], "done")

    def test_no_frontmatter_returns_body_only(self):
        p = self.dir / "e.md"
        p.write_text("just a body\n")
        got = sod.read_note(p)
        self.assertEqual(got["_body"].strip(), "just a body")


class TestHelpers(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(sod.parse_date("2026-09-15"), dt.date(2026, 9, 15))
        self.assertEqual(sod.parse_date("2026-09-15T14:22:12Z"), dt.date(2026, 9, 15))
        self.assertIsNone(sod.parse_date(None))
        self.assertIsNone(sod.parse_date(""))
        self.assertIsNone(sod.parse_date("not a date"))

    def test_complexity_rank_orders_low_medium_high_missing(self):
        ranks = [sod.complexity_rank(v) for v in ("low", "medium", "high", None)]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(sod.complexity_rank("bogus"), sod.MISSING_RANK)

    def test_assign_sort_keys_is_dense_rank_from_zero(self):
        notes = [{"n": "c", "k": 3}, {"n": "a", "k": 1}, {"n": "b", "k": 2}]
        out = sod.assign_sort_keys(notes, lambda x: x["k"])
        self.assertEqual([x["n"] for x in out], ["a", "b", "c"])
        self.assertEqual([x["sort_key"] for x in out], [0, 1, 2])


class TestPrBacklog(unittest.TestCase):
    """Fixtures mirror live 2026-09-15 data plus the edge cases the spec names."""

    FIXTURES = {
        "assignee": [
            {"number": 1567, "title": "Tailscale operator", "isDraft": False,
             "createdAt": "2026-09-03T19:14:55Z",
             "url": "https://github.com/huntresslabs/infra-k8s/pull/1567",
             "repository": {"nameWithOwner": "huntresslabs/infra-k8s"}},
            {"number": 42, "title": "My own draft, assigned to me", "isDraft": True,
             "createdAt": "2026-01-02T00:00:00Z",
             "url": "https://github.com/huntresslabs/infra-aws/pull/42",
             "repository": {"nameWithOwner": "huntresslabs/infra-aws"}},
        ],
        "team:infrastructure-sre": [
            {"number": 890, "title": "Datadog monitors", "isDraft": False,
             "createdAt": "2026-08-21T21:03:31Z",
             "url": "https://github.com/huntresslabs/observability/pull/890",
             "repository": {"nameWithOwner": "huntresslabs/observability"}},
            {"number": 1567, "title": "Tailscale operator", "isDraft": False,
             "createdAt": "2026-09-03T19:14:55Z",
             "url": "https://github.com/huntresslabs/infra-k8s/pull/1567",
             "repository": {"nameWithOwner": "huntresslabs/infra-k8s"}},
        ],
        "team:idex": [
            {"number": 960, "title": "Key Vault public access", "isDraft": False,
             "createdAt": "2026-09-14T17:00:54Z",
             "url": "https://github.com/huntresslabs/infra-azure/pull/960",
             "repository": {"nameWithOwner": "huntresslabs/infra-azure"}},
            {"number": 719, "title": "Someone else's draft", "isDraft": True,
             "createdAt": "2026-06-25T19:51:38Z",
             "url": "https://github.com/huntresslabs/infra-azure/pull/719",
             "repository": {"nameWithOwner": "huntresslabs/infra-azure"}},
        ],
        "repo:infra-elastic": [
            {"number": 623, "title": "Draft in infra-elastic", "isDraft": True,
             "createdAt": "2026-05-21T04:32:48Z",
             "url": "https://github.com/huntresslabs/infra-elastic/pull/623"},
            {"number": 700, "title": "Open in infra-elastic", "isDraft": False,
             "createdAt": "2026-07-01T00:00:00Z",
             "url": "https://github.com/huntresslabs/infra-elastic/pull/700"},
        ],
    }

    def setUp(self):
        self._real = sod.gh_json

        def fake(args):
            if "--assignee" in args:
                return self.FIXTURES["assignee"]
            if "huntresslabs/infrastructure-sre" in args:
                return self.FIXTURES["team:infrastructure-sre"]
            if "huntresslabs/idex" in args:
                return self.FIXTURES["team:idex"]
            return self.FIXTURES["repo:infra-elastic"]

        sod.gh_json = fake

    def tearDown(self):
        sod.gh_json = self._real

    def test_sorted_created_at_asc_across_whole_table(self):
        keys = [(p["repo"], p["number"]) for p in sod.collect_prs()]
        self.assertEqual(keys, [
            ("huntresslabs/infra-aws", 42),            # 2026-01-02, own draft
            ("huntresslabs/infra-elastic", 700),       # 2026-07-01
            ("huntresslabs/observability", 890),       # 2026-08-21
            ("huntresslabs/infra-k8s", 1567),          # 2026-09-03
            ("huntresslabs/infra-azure", 960),         # 2026-09-14
        ])

    def test_pr_matching_two_criteria_appears_once_with_both_reasons(self):
        hits = [p for p in sod.collect_prs() if p["number"] == 1567]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["reasons"], ["assignee", "team:infrastructure-sre"])

    def test_own_draft_kept_when_assigned_to_me(self):
        self.assertIn(42, [p["number"] for p in sod.collect_prs()])

    def test_team_requested_draft_excluded(self):
        self.assertNotIn(719, [p["number"] for p in sod.collect_prs()])

    def test_infra_elastic_draft_excluded(self):
        self.assertNotIn(623, [p["number"] for p in sod.collect_prs()])

    def test_infra_elastic_rows_get_repo_filled_in(self):
        row = next(p for p in sod.collect_prs() if p["number"] == 700)
        self.assertEqual(row["repo"], "huntresslabs/infra-elastic")

    def test_author_only_pr_is_absent(self):
        """A PR authored by me but neither assigned nor team-requested must not
        appear: `--author` is never queried."""
        self.assertNotIn(9999, [p["number"] for p in sod.collect_prs()])
        self.assertFalse(any("--author" in query for _, _, query in sod.PR_QUERIES))

    def test_render_is_byte_identical_across_runs(self):
        self.assertEqual(sod.render_prs(sod.collect_prs()),
                         sod.render_prs(sod.collect_prs()))

    def test_render_contains_table_header_and_links(self):
        out = sod.render_prs(sod.collect_prs())
        self.assertIn("| PR | Title | Opened | Why |", out)
        self.assertIn(
            "[infra-k8s#1567](https://github.com/huntresslabs/infra-k8s/pull/1567)", out)

    def test_empty_backlog_renders_placeholder(self):
        self.assertIn("_No open PRs", sod.render_prs([]))


class TestProjectWork(unittest.TestCase):
    WORKFLOWS = [
        {"name": "ITDR - Rapid Flow", "states": [
            {"id": 500041832, "type": "started", "name": "In Progress"},
            {"id": 500041837, "type": "backlog", "name": "Backlog"},
            {"id": 500041840, "type": "done", "name": "Completed"},
        ]},
        {"name": "Creative", "states": [
            {"id": 500000900, "type": "unstarted", "name": "Ideas"},
            {"id": 500000901, "type": "started", "name": "Blocked"},
        ]},
    ]

    # Epic A: due 2026-10-01. Epic B: no due date, created earlier.
    # Epic C: no due date, created later. Ordering must be A, B, C.
    EPICS = {
        222628: {"id": 222628, "name": "Epic A", "deadline": "2026-10-01T00:00:00Z",
                 "created_at": "2026-07-27T20:33:33Z", "state": "in progress",
                 "app_url": "https://app.shortcut.com/huntress/epic/222628"},
        228163: {"id": 228163, "name": "Epic B", "deadline": None,
                 "created_at": "2026-06-01T00:00:00Z", "state": "in progress",
                 "app_url": "https://app.shortcut.com/huntress/epic/228163"},
        233654: {"id": 233654, "name": "Epic C", "deadline": None,
                 "created_at": "2026-08-01T00:00:00Z", "state": "in progress",
                 "app_url": "https://app.shortcut.com/huntress/epic/233654"},
    }

    STORIES = [
        # Epic B: a blocker with a LATE due date, and a non-blocker with an
        # EARLY one. The blocker must still render first.
        {"id": 228166, "name": "Blocks something", "workflow_state_id": 500041837,
         "epic_id": 228163, "deadline": "2026-12-01T00:00:00Z", "estimate": None,
         "blocker": True, "created_at": "2026-09-01T00:00:00Z",
         "app_url": "https://app.shortcut.com/huntress/story/228166"},
        {"id": 228170, "name": "Blocks nothing", "workflow_state_id": 500041837,
         "epic_id": 228163, "deadline": "2026-09-20T00:00:00Z", "estimate": 1,
         "blocker": False, "created_at": "2026-09-01T00:00:00Z",
         "app_url": "https://app.shortcut.com/huntress/story/228170"},
        # Epic A: same due date, complexity decides (low before high).
        {"id": 222656, "name": "Low effort", "workflow_state_id": 500041832,
         "epic_id": 222628, "deadline": "2026-10-05T00:00:00Z", "estimate": 1,
         "blocker": False, "created_at": "2026-07-28T00:00:00Z",
         "app_url": "https://app.shortcut.com/huntress/story/222656"},
        {"id": 222657, "name": "High effort", "workflow_state_id": 500041832,
         "epic_id": 222628, "deadline": "2026-10-05T00:00:00Z", "estimate": 8,
         "blocker": False, "created_at": "2026-07-28T00:00:00Z",
         "app_url": "https://app.shortcut.com/huntress/story/222657"},
        # Epic C.
        {"id": 233661, "name": "Epic C story", "workflow_state_id": 500041832,
         "epic_id": 233654, "deadline": None, "estimate": None,
         "blocker": False, "created_at": "2026-08-02T00:00:00Z",
         "app_url": "https://app.shortcut.com/huntress/story/233661"},
        # No epic at all.
        {"id": 228627, "name": "Orphan story", "workflow_state_id": 500041837,
         "epic_id": None, "deadline": None, "estimate": None,
         "blocker": False, "created_at": "2026-09-05T00:00:00Z",
         "app_url": "https://app.shortcut.com/huntress/story/228627"},
    ]

    def setUp(self):
        sod.PROJECT_DIR = Path(tempfile.mkdtemp())
        self._real = sod.short_api
        self._stories = list(self.STORIES)
        stories = self._stories
        epics = self.EPICS
        workflows = self.WORKFLOWS

        def fake(path, **params):
            if path == "/member":
                return {"mention_name": "lukesnyder"}
            if path == "/workflows":
                return workflows
            if path == "/search/stories":
                return {"data": stories, "total": len(stories)}
            if path.startswith("/epics/"):
                return epics[int(path.rsplit("/", 1)[1])]
            raise AssertionError(path)

        sod.short_api = fake

    def tearDown(self):
        sod.short_api = self._real

    def rows(self):
        epics, stories = sod.fetch_project_work()
        return sod.order_project_work(epics, stories)

    def test_epic_order_due_date_first_then_created_at(self):
        labels = [r["title"] for r in self.rows() if r["type"] == "epic"]
        self.assertEqual(labels, ["Epic A", "Epic B", "Epic C"])

    def test_sort_key_is_dense_rank_matching_emission_order(self):
        keys = [r["sort_key"] for r in self.rows()]
        self.assertEqual(keys, list(range(len(keys))))

    def test_epic_row_precedes_its_stories(self):
        rows = self.rows()
        epic_a = next(i for i, r in enumerate(rows) if r["title"] == "Epic A")
        low = next(i for i, r in enumerate(rows) if r["title"] == "Low effort")
        self.assertLess(epic_a, low)

    def test_blocking_story_renders_above_non_blocking_despite_later_due_date(self):
        rows = self.rows()
        blocks = next(i for i, r in enumerate(rows) if r["title"] == "Blocks something")
        nothing = next(i for i, r in enumerate(rows) if r["title"] == "Blocks nothing")
        self.assertLess(blocks, nothing)

    def test_equal_due_date_breaks_on_complexity(self):
        rows = self.rows()
        low = next(i for i, r in enumerate(rows) if r["title"] == "Low effort")
        high = next(i for i, r in enumerate(rows) if r["title"] == "High effort")
        self.assertLess(low, high)

    def test_epic_group_label_sorts_alphabetically_into_epic_rank_order(self):
        groups = []
        for row in self.rows():
            if row["epic_group"] not in groups:
                groups.append(row["epic_group"])
        self.assertEqual(groups, sorted(groups))
        self.assertTrue(groups[0].endswith("Epic A"))
        self.assertIn("No epic", groups[-1])

    def test_estimate_maps_to_complexity(self):
        self.assertEqual(sod.estimate_to_complexity(0), "low")
        self.assertEqual(sod.estimate_to_complexity(1), "low")
        self.assertEqual(sod.estimate_to_complexity(2), "medium")
        self.assertEqual(sod.estimate_to_complexity(3), "medium")
        self.assertEqual(sod.estimate_to_complexity(5), "high")
        self.assertEqual(sod.estimate_to_complexity(8), "high")
        self.assertIsNone(sod.estimate_to_complexity(None))

    def test_done_detection_uses_state_type_not_name(self):
        """'Blocked' is a `started` state here — it must not read as done, and
        'Completed' must, purely from the type field."""
        done = sod.done_state_ids()
        self.assertIn(500041840, done)
        self.assertNotIn(500000901, done)

    def test_exactly_the_epics_referenced_by_my_stories(self):
        ids = {r["id"] for r in self.rows() if r["type"] == "epic"}
        self.assertEqual(ids, {222628, 228163, 233654})

    def test_file_per_row_with_schema_frontmatter(self):
        sod.cmd_project_work()
        files = sorted(p.name for p in sod.PROJECT_DIR.glob("*.md"))
        self.assertEqual(len(files), len(self.rows()))
        note = sod.read_note(sod.PROJECT_DIR / "story-222656.md")
        for field in ("type", "id", "title", "state", "epic_id",
                      "created_at", "due_date", "complexity", "link",
                      "sort_key", "epic_group"):
            self.assertIn(field, note)
        self.assertEqual(note["type"], "story")
        self.assertEqual(note["id"], 222656)
        self.assertEqual(note["complexity"], "low")
        epic_note = sod.read_note(sod.PROJECT_DIR / "epic-222628.md")
        self.assertEqual(epic_note["type"], "epic")
        self.assertIsNone(epic_note["epic_id"])

    def test_full_regeneration_drops_closed_story_and_orphaned_epic(self):
        sod.cmd_project_work()
        self.assertTrue((sod.PROJECT_DIR / "story-233661.md").exists())
        self.assertTrue((sod.PROJECT_DIR / "epic-233654.md").exists())
        self._stories[:] = [s for s in self._stories if s["id"] != 233661]
        sod.cmd_project_work()
        self.assertFalse((sod.PROJECT_DIR / "story-233661.md").exists())
        self.assertFalse((sod.PROJECT_DIR / "epic-233654.md").exists())

    def test_regeneration_preserves_non_base_files(self):
        keep = sod.PROJECT_DIR / "my notes.md"
        keep.parent.mkdir(parents=True, exist_ok=True)
        keep.write_text("---\ntitle: mine\n---\n\nhand written\n")
        sod.cmd_project_work()
        self.assertTrue(keep.exists())
        self.assertIn("hand written", keep.read_text())

    def test_search_follows_the_next_cursor(self):
        """Shortcut caps page_size at 25; truncating at one page would silently
        drop stories once the list grows past it."""
        pages = [
            {"data": [self.STORIES[0]], "next": "/api/v3/search/stories?next=TOKEN2"},
            {"data": [self.STORIES[1]], "next": None},
        ]
        seen = []

        def paged(path, **params):
            seen.append(params.get("next"))
            return pages[len(seen) - 1]

        sod.short_api = paged
        got = sod.search_stories("owner:lukesnyder !is:done")
        self.assertEqual([s["id"] for s in got], [228166, 228170])
        self.assertEqual(seen, [None, "TOKEN2"])


if __name__ == "__main__":
    unittest.main()
