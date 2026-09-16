import datetime as dt
import os
import tempfile
import unittest
import unittest.mock
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

    def test_sh_retries_transient_failure_then_returns(self):
        calls = []

        def fake_run(args, **kwargs):
            calls.append(args)
            if len(calls) < 3:
                raise sod.subprocess.CalledProcessError(1, args)
            return unittest.mock.Mock(stdout="ok")

        with unittest.mock.patch.object(sod.subprocess, "run", fake_run), \
             unittest.mock.patch.object(sod.time, "sleep", lambda _: None):
            self.assertEqual(sod.sh(["whatever"]), "ok")
        self.assertEqual(len(calls), 3)

    def test_sh_raises_after_exhausting_retries(self):
        def fake_run(args, **kwargs):
            raise sod.subprocess.CalledProcessError(1, args)

        with unittest.mock.patch.object(sod.subprocess, "run", fake_run), \
             unittest.mock.patch.object(sod.time, "sleep", lambda _: None):
            with self.assertRaises(sod.subprocess.CalledProcessError):
                sod.sh(["whatever"], retries=2)


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

    def test_state_type_is_stored_alongside_the_display_name(self):
        """IMPORTANT TODAY ranks undated stories by state, and the spec forbids
        matching on state name -- so the type has to be persisted per note."""
        sod.cmd_project_work()
        note = sod.read_note(sod.PROJECT_DIR / "story-222656.md")
        self.assertEqual(note["state"], "In Progress")
        self.assertEqual(note["state_type"], "started")
        backlog = sod.read_note(sod.PROJECT_DIR / "story-228166.md")
        self.assertEqual(backlog["state"], "Backlog")
        self.assertEqual(backlog["state_type"], "backlog")

    def test_workflows_are_fetched_once_per_run(self):
        calls = []
        inner = sod.short_api

        def counting(path, **params):
            calls.append(path)
            return inner(path, **params)

        sod.short_api = counting
        sod.fetch_project_work()
        self.assertEqual(calls.count("/workflows"), 1)

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


class TestCommitments(unittest.TestCase):
    def setUp(self):
        sod.COMMITMENTS_DIR = Path(tempfile.mkdtemp())

    def add(self, **kw):
        fields = dict(
            title="A commitment", summary="s", link="https://slack/x",
            committed_date="2026-09-14", due_date="2026-09-16",
            complexity="medium", tags=[],
        )
        fields.update(kw)
        return sod.upsert_commitment(**fields)

    def mark_done(self, path):
        note = sod.read_note(path)
        fields = {k: v for k, v in note.items() if not k.startswith("_")}
        fields["status"] = "done"
        sod.write_note(path, fields, note.get("_body", ""))

    def test_created_note_has_full_schema_and_defaults_status_open(self):
        action, path = self.add()
        self.assertEqual(action, "created")
        note = sod.read_note(path)
        for field in ("title", "committed_date", "due_date", "complexity",
                      "tags", "summary", "link", "status", "sort_key"):
            self.assertIn(field, note)
        self.assertEqual(note["status"], "open")
        self.assertEqual(note["committed_date"], "2026-09-14")
        self.assertEqual(note["complexity"], "medium")

    def test_file_per_row(self):
        self.add(link="https://slack/a", title="First thing")
        self.add(link="https://slack/b", title="Second thing entirely")
        self.assertEqual(len(list(sod.COMMITMENTS_DIR.glob("*.md"))), 2)

    def test_same_link_twice_is_a_duplicate_not_a_second_row(self):
        self.add()
        action, _ = self.add()
        self.assertEqual(action, "duplicate")
        self.assertEqual(len(list(sod.COMMITMENTS_DIR.glob("*.md"))), 1)

    def test_restatement_on_later_day_updates_due_date_in_place(self):
        _, path = self.add(link="https://slack/day1",
                           title="Send Connor the Elastic user info",
                           due_date="2026-09-16")
        action, same = self.add(link="https://slack/day8",
                                title="Send Connor Ford the Elastic user info please",
                                due_date="2026-09-23")
        self.assertEqual(action, "updated")
        self.assertEqual(same, path)
        self.assertEqual(len(list(sod.COMMITMENTS_DIR.glob("*.md"))), 1)
        self.assertEqual(sod.read_note(path)["due_date"], "2026-09-23")

    def test_restatement_does_not_match_a_done_entry(self):
        _, path = self.add(link="https://slack/day1", title="Unique phrasing here")
        self.mark_done(path)
        action, _ = self.add(link="https://slack/day8", title="Unique phrasing here")
        self.assertEqual(action, "created")

    def test_unrelated_titles_are_two_rows(self):
        self.add(link="https://slack/a", title="Rotate the Elasticsearch ILM policy")
        action, _ = self.add(link="https://slack/b",
                             title="Review Tailscale ACL autoapprovers")
        self.assertEqual(action, "created")

    def test_sort_overdue_pinned_first_then_due_date_then_complexity(self):
        self.add(link="l1", title="Future high", due_date="2026-12-01", complexity="high")
        self.add(link="l2", title="Overdue one", due_date="2026-09-01", complexity="high")
        self.add(link="l3", title="Due today low", due_date="2026-09-15", complexity="low")
        self.add(link="l4", title="Undated", due_date=None, complexity="low")
        self.add(link="l5", title="Due today high", due_date="2026-09-15", complexity="high")
        sod.cmd_commitments(ref=dt.date(2026, 9, 15))
        order = [n["title"] for n in sorted(sod.load_commitments(),
                                            key=lambda n: n["sort_key"])]
        self.assertEqual(order, ["Overdue one", "Due today low",
                                 "Due today high", "Future high", "Undated"])

    def test_missing_complexity_sorts_last_within_its_tier(self):
        self.add(link="l1", title="Same day high", due_date="2026-09-20", complexity="high")
        self.add(link="l2", title="Same day none", due_date="2026-09-20", complexity=None)
        sod.cmd_commitments(ref=dt.date(2026, 9, 15))
        order = [n["title"] for n in sorted(sod.load_commitments(),
                                            key=lambda n: n["sort_key"])]
        self.assertEqual(order, ["Same day high", "Same day none"])

    def test_done_entries_stay_on_disk_but_are_excluded_from_ranking(self):
        _, path = self.add(link="l1", title="Will be marked done")
        self.add(link="l2", title="Stays open and unrelated")
        self.mark_done(path)
        sod.cmd_commitments(ref=dt.date(2026, 9, 15))
        self.assertTrue(path.exists())
        self.assertEqual(sod.read_note(path)["status"], "done")
        ranked = [n["title"] for n in sod.load_commitments()]
        self.assertEqual(ranked, ["Stays open and unrelated"])

    def test_custom_body_is_written_and_default_is_the_source_link(self):
        """Migrated TODO sub-bullets live in the note body, not the schema."""
        action, path = self.add(link="https://slack/withbody",
                               title="Parent item with checks",
                               body="- [ ] First check\n- [x] Second check")
        self.assertEqual(action, "created")
        body = sod.read_note(path)["_body"]
        self.assertIn("- [ ] First check", body)
        self.assertIn("- [x] Second check", body)

        _, plain = self.add(link="https://slack/nobody", title="Plain item")
        self.assertIn("https://slack/nobody", sod.read_note(plain)["_body"])

    def test_body_is_preserved_across_sort_key_recomputation(self):
        _, path = self.add(link="https://slack/keepbody",
                           title="Item whose body must survive",
                           body="- [ ] A sub task worth keeping")
        sod.cmd_commitments(ref=dt.date(2026, 9, 15))
        self.assertIn("A sub task worth keeping", sod.read_note(path)["_body"])

    def test_training_email_uses_the_same_schema(self):
        action, path = sod.upsert_commitment(
            title="Complete annual security awareness training",
            summary="Assigned via email; covers phishing and data handling.",
            link="https://mail.google.com/mail/u/0/#inbox/abc123",
            committed_date="2026-09-12", due_date="2026-09-30",
            complexity="low", tags=["training", "compliance"])
        self.assertEqual(action, "created")
        note = sod.read_note(path)
        self.assertEqual(note["status"], "open")
        self.assertEqual(note["tags"], ["training", "compliance"])
        self.assertEqual(note["committed_date"], "2026-09-12")


class TestImportant(unittest.TestCase):
    REF = dt.date(2026, 9, 15)

    def setUp(self):
        root = Path(tempfile.mkdtemp())
        sod.COMMITMENTS_DIR = root / "Commitments"
        sod.PROJECT_DIR = root / "Project Work"
        sod.TODO_PATH = root / "TODO.md"
        sod.COMMITMENTS_DIR.mkdir(parents=True)
        sod.PROJECT_DIR.mkdir(parents=True)
        sod.TODO_PATH.write_text("## Today\n\n## Backlog\n\n## Waiting\n\n## Done\n")

    def commitment(self, title, due, complexity, status="open"):
        sod.write_note(sod.COMMITMENTS_DIR / f"{sod.slugify(title)}.md", {
            "title": title, "committed_date": "2026-09-01", "due_date": due,
            "complexity": complexity, "tags": [], "summary": "s",
            "link": f"https://slack/{sod.slugify(title)}",
            "status": status, "sort_key": 0})

    def row(self, kind, rid, title, due, complexity, state_type="started"):
        sod.write_note(sod.PROJECT_DIR / f"{kind}-{rid}.md", {
            "type": kind, "id": rid, "title": title, "state": "Whatever",
            "state_type": state_type,
            "epic_id": None, "created_at": "2026-09-01", "due_date": due,
            "complexity": complexity, "blocker": False,
            "link": f"https://app.shortcut.com/huntress/{kind}/{rid}",
            "epic_group": "00 — E", "sort_key": 0})

    def todos(self, body):
        sod.TODO_PATH.write_text(body)

    def labels(self, limit=5):
        return [i["label"] for i in sod.important_pool(self.REF)][:limit]

    def test_bands_render_overdue_then_started_then_unstarted_then_rest(self):
        """The whole band order in one assertion. Note the undated started
        story outranks a dated commitment -- that is the point of the band."""
        self.commitment("Overdue commitment", "2026-09-01", "high")
        self.commitment("Future commitment", "2026-09-30", "low")
        self.row("story", 1, "Started undated story", None, "low",
                 state_type="started")
        self.row("story", 2, "Unstarted undated story", None, "low",
                 state_type="unstarted")
        self.assertEqual(self.labels(), ["Overdue commitment",
                                         "Started undated story",
                                         "Unstarted undated story",
                                         "Future commitment"])

    def test_missing_complexity_sorts_last_within_tier(self):
        self.row("story", 1, "Undated story no estimate", None, None)
        self.row("story", 2, "Undated story low", None, "low")
        self.todos("## Today\n- [ ] A plain todo\n")
        labels = self.labels()
        self.assertEqual(labels[0], "Undated story low")
        self.assertIn("Undated story no estimate", labels)
        self.assertIn("A plain todo", labels)
        # Both lack complexity, so source order decides: story before todo.
        self.assertLess(labels.index("Undated story no estimate"),
                        labels.index("A plain todo"))

    def test_tie_on_due_date_and_complexity_breaks_by_source_order(self):
        """Source order still governs, but only inside the overdue band -- it is
        the one band where commitments, stories, and TODOs coexist."""
        self.commitment("Tied commitment", "2026-09-10", "medium")
        self.row("story", 1, "Tied story", "2026-09-10", "medium",
                 state_type="started")
        self.assertEqual(self.labels()[:2], ["Tied commitment", "Tied story"])

    def test_epic_never_eligible_even_with_the_earliest_due_date(self):
        self.row("epic", 100, "Epic due tomorrow", "2026-09-16", None)
        self.row("story", 1, "Story due much later", "2026-12-01", "high")
        labels = self.labels()
        self.assertNotIn("Epic due tomorrow", labels)
        self.assertEqual(labels, ["Story due much later"])

    def test_done_commitment_excluded(self):
        self.commitment("Done thing", "2026-09-01", "low", status="done")
        self.commitment("Open thing", "2026-09-02", "low")
        self.assertEqual(self.labels(), ["Open thing"])

    def test_todos_only_top_level_from_today_and_backlog(self):
        self.todos(
            "## Today\n- [ ] Top level today\n\t- [ ] Nested child\n"
            "## Backlog\n- [ ] Top level backlog\n- [x] Already done\n"
            "## Waiting\n- [ ] Waiting item\n"
            "## Done\n- [x] Finished\n")
        labels = [t["label"] for t in sod.load_todos()]
        self.assertEqual(labels, ["Top level today", "Top level backlog"])

    def test_todo_inline_due_date_is_parsed(self):
        self.todos("## Backlog\n- [ ] Check the ILM prediction — due [[2026-09-02]]\n")
        self.assertEqual(sod.load_todos()[0]["due_date"], "2026-09-02")

    def test_children_attach_to_their_root_regardless_of_indent_style(self):
        """Live TODO.md mixes tab-indented and two-space-indented sub-bullets.
        Both are children; neither is a root item."""
        self.todos(
            "## Backlog\n"
            "- [ ] Tab parent\n"
            "\t- [ ] Tab child one\n"
            "\t- [ ] Tab child two\n"
            "- [ ] Space parent\n"
            "  - [ ] Space child one\n"
            "  - [ ] Space child two\n")
        todos = sod.load_todos()
        self.assertEqual([t["label"] for t in todos], ["Tab parent", "Space parent"])
        self.assertEqual(todos[0]["children"], ["- [ ] Tab child one",
                                                "- [ ] Tab child two"])
        self.assertEqual(todos[1]["children"], ["- [ ] Space child one",
                                                "- [ ] Space child two"])

    def test_completed_children_are_kept_as_body_context(self):
        """A done sub-bullet is history worth carrying into the commitment."""
        self.todos("## Backlog\n- [ ] Parent\n\t- [x] Already verified\n"
                   "\t- [ ] Still open\n")
        self.assertEqual(sod.load_todos()[0]["children"],
                         ["- [x] Already verified", "- [ ] Still open"])

    def test_root_with_no_children_has_empty_list(self):
        self.todos("## Backlog\n- [ ] Lonely item\n")
        self.assertEqual(sod.load_todos()[0]["children"], [])

    def test_children_of_a_completed_root_do_not_graft_onto_the_previous_item(self):
        self.todos("## Backlog\n"
                   "- [ ] Open item\n"
                   "- [x] Completed item\n"
                   "\t- [ ] Child of the completed item\n")
        todos = sod.load_todos()
        self.assertEqual([t["label"] for t in todos], ["Open item"])
        self.assertEqual(todos[0]["children"], [])

    def test_blank_line_inside_a_group_does_not_end_it(self):
        self.todos("## Backlog\n- [ ] Parent\n\n\t- [ ] Child after a blank\n")
        self.assertEqual(sod.load_todos()[0]["children"],
                         ["- [ ] Child after a blank"])

    def test_todo_link_is_stable_and_unique_per_item(self):
        a = sod.todo_link("Watch ACNS flow logs for the portal namespace")
        b = sod.todo_link("Watch ACNS flow logs for the portal namespace")
        c = sod.todo_link("Merge the production portal network-policy PR")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertTrue(a.startswith("todo://"))

    def test_todo_link_survives_retitling(self):
        """Dedup keys off the raw TODO text, so the commitment can be retitled
        freely without the migration re-creating it."""
        raw = "**Remove `portal-app-egress-catchall`** from staging + production"
        self.assertEqual(sod.todo_link(raw), sod.todo_link(raw))
        self.assertNotIn("*", sod.todo_link(raw))

    def test_migrated_todo_is_not_double_counted(self):
        """TODO.md is left intact after migration, so a TODO that already has a
        commitment must not appear twice in the pool."""
        raw = "Finish Huntress Community Apps ADR"
        self.todos(f"## Backlog\n- [ ] {raw}\n- [ ] Not yet migrated\n")
        sod.upsert_commitment(title="Finish the Community Apps ADR",
                              summary="Migrated from TODO.md.",
                              link=sod.todo_link(raw),
                              committed_date="2026-09-15", complexity="medium")
        labels = self.labels()
        self.assertEqual(labels.count("Finish the Community Apps ADR"), 1)
        self.assertNotIn(raw, labels)
        self.assertIn("Not yet migrated", labels)

    def test_dedup_ignores_a_done_commitment(self):
        """Completing the commitment must not silently resurrect the TODO."""
        raw = "Finish Huntress Community Apps ADR"
        self.todos(f"## Backlog\n- [ ] {raw}\n")
        _, path = sod.upsert_commitment(
            title="Finish the ADR", summary="s", link=sod.todo_link(raw),
            committed_date="2026-09-15", complexity="medium")
        note = sod.read_note(path)
        fields = {k: v for k, v in note.items() if not k.startswith("_")}
        fields["status"] = "done"
        sod.write_note(path, fields, note.get("_body", ""))
        self.assertEqual(self.labels(), [])

    def test_todo_with_overdue_inline_date_outranks_future_commitment(self):
        self.todos("## Today\n- [ ] Overdue todo — due [[2026-09-01]]\n")
        self.commitment("Future commitment", "2026-09-30", "low")
        self.assertEqual(self.labels()[0], "Overdue todo — due [[2026-09-01]]")

    def test_limit_is_at_most_five(self):
        for i in range(9):
            self.commitment(f"Commitment number {i}", f"2026-09-{i + 1:02d}", "low")
        rendered = sod.render_important(sod.important_pool(self.REF)[:5])
        self.assertEqual(len(rendered.strip().splitlines()), 5)

    def test_render_marks_source_and_overdue(self):
        self.commitment("Overdue commitment", "2026-09-01", "high")
        out = sod.render_important(sod.important_pool(self.REF)[:5])
        self.assertIn("- [ ] ", out)
        self.assertIn("commitment", out.lower())
        self.assertIn("overdue", out.lower())

    def test_empty_pool_renders_placeholder(self):
        self.assertIn("_Nothing", sod.render_important([]))

    def test_started_stories_sort_by_closest_due_date_undated_last(self):
        self.row("story", 1, "Started undated", None, "low", state_type="started")
        self.row("story", 2, "Started due later", "2026-09-25", "high",
                 state_type="started")
        self.row("story", 3, "Started due soon", "2026-09-17", "high",
                 state_type="started")
        self.assertEqual(self.labels(), ["Started due soon",
                                         "Started due later",
                                         "Started undated"])

    def test_unstarted_stories_sort_by_complexity_not_due_date(self):
        self.row("story", 1, "Unstarted high, due soon", "2026-09-17", "high",
                 state_type="unstarted")
        self.row("story", 2, "Unstarted low, due later", "2026-09-25", "low",
                 state_type="unstarted")
        self.assertEqual(self.labels(), ["Unstarted low, due later",
                                         "Unstarted high, due soon"])

    def test_unstarted_outranks_non_overdue_commitments_and_todos(self):
        self.commitment("Commitment due next week", "2026-09-22", "low")
        self.todos("## Today\n- [ ] A plain todo\n")
        self.row("story", 1, "Unstarted story", None, "high",
                 state_type="unstarted")
        self.assertEqual(self.labels(), ["Unstarted story",
                                         "Commitment due next week",
                                         "A plain todo"])

    def test_backlog_stories_are_excluded_entirely(self):
        """Backlog work still needs shaping, so it is not an answer to 'what
        could I finish this week'."""
        self.row("story", 1, "Backlog story", None, "low", state_type="backlog")
        self.row("story", 2, "Started story", None, "high", state_type="started")
        self.assertEqual(self.labels(), ["Started story"])

    def test_backlog_story_excluded_even_when_overdue(self):
        self.row("story", 1, "Overdue backlog story", "2026-09-01", "low",
                 state_type="backlog")
        self.assertEqual(self.labels(), [])

    def test_overdue_started_story_pins_into_the_overdue_band(self):
        self.row("story", 1, "Overdue started story", "2026-09-02", "high",
                 state_type="started")
        self.row("story", 2, "Started due soon", "2026-09-16", "low",
                 state_type="started")
        self.commitment("Commitment due next week", "2026-09-22", "low")
        self.assertEqual(self.labels(), ["Overdue started story",
                                         "Started due soon",
                                         "Commitment due next week"])

    def test_unknown_state_type_is_kept_and_sorts_after_unstarted(self):
        """Never silently drop a story just because its state type is missing --
        only `backlog` is an explicit exclusion."""
        self.row("story", 1, "Story with no state type", None, "low",
                 state_type=None)
        self.row("story", 2, "Unstarted story", None, "low",
                 state_type="unstarted")
        self.assertEqual(self.labels(), ["Unstarted story",
                                         "Story with no state type"])


class TestDailyNote(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        sod.DAILY_DIR = self.root / "Daily notes"
        sod.COMMITMENTS_DIR = self.root / "Commitments"
        sod.PROJECT_DIR = self.root / "Project Work"
        sod.TODO_PATH = self.root / "TODO.md"
        sod.TODO_PATH.write_text("## Today\n- [ ] Something to do\n")
        self._real = sod.gh_json
        sod.gh_json = lambda args: []

    def tearDown(self):
        sod.gh_json = self._real

    def test_path_uses_year_and_month_folders(self):
        path = sod.daily_note_path(dt.date(2026, 9, 15))
        self.assertTrue(
            str(path).endswith("Daily notes/2026/09-September/2026-09-15.md"))

    def test_latest_daily_date_ignores_today_and_falls_back_to_yesterday(self):
        self.assertIsNone(sod.latest_daily_date(before=dt.date(2026, 9, 15)))
        older = sod.daily_note_path(dt.date(2026, 9, 12))
        older.parent.mkdir(parents=True, exist_ok=True)
        older.write_text("x")
        sod.daily_note_path(dt.date(2026, 9, 15)).write_text("today")
        self.assertEqual(sod.latest_daily_date(before=dt.date(2026, 9, 15)),
                         dt.date(2026, 9, 12))

    def test_all_four_sections_written_in_order(self):
        sod.cmd_daily_note(day=dt.date(2026, 9, 15))
        text = sod.daily_note_path(dt.date(2026, 9, 15)).read_text()
        positions = [text.index(f"## {h}") for h in sod.SECTION_ORDER]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(sod.SECTION_ORDER, [
            "IMPORTANT TODAY/THIS WEEK", "OPEN COMMITMENTS",
            "PR REVIEW BACKLOG", "PROJECT WORK"])

    def test_bases_are_embedded_not_rendered(self):
        sod.cmd_daily_note(day=dt.date(2026, 9, 15))
        text = sod.daily_note_path(dt.date(2026, 9, 15)).read_text()
        self.assertIn("![[Commitments.base#Daily Note View]]", text)
        self.assertIn("![[Project Work.base#Daily Note View]]", text)

    def test_rerun_is_idempotent(self):
        day = dt.date(2026, 9, 15)
        sod.cmd_daily_note(day=day)
        first = sod.daily_note_path(day).read_text()
        sod.cmd_daily_note(day=day)
        self.assertEqual(first, sod.daily_note_path(day).read_text())

    def test_rerun_preserves_foreign_sections(self):
        day = dt.date(2026, 9, 15)
        sod.cmd_daily_note(day=day)
        path = sod.daily_note_path(day)
        path.write_text(path.read_text() + "\n## Completed\n- [x] eod wrote this\n")
        sod.cmd_daily_note(day=day)
        text = path.read_text()
        self.assertIn("## Completed", text)
        self.assertIn("eod wrote this", text)

    def test_upsert_section_replaces_only_its_own_body(self):
        text = "## A\nold a\n\n## B\nkeep b\n"
        out = sod.upsert_section(text, "A", "new a")
        self.assertIn("new a", out)
        self.assertNotIn("old a", out)
        self.assertIn("keep b", out)

    def test_upsert_section_appends_when_heading_absent(self):
        out = sod.upsert_section("## B\nkeep b\n", "A", "new a")
        self.assertIn("## A", out)
        self.assertIn("keep b", out)

    def test_window_falls_back_to_yesterday_with_no_notes(self):
        self.assertEqual(sod.cmd_window(),
                         str(sod.today() - dt.timedelta(days=1)))


if __name__ == "__main__":
    unittest.main()
