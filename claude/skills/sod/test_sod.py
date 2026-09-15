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


if __name__ == "__main__":
    unittest.main()
