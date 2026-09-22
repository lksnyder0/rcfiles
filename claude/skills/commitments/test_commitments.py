import datetime as dt
import json
import os
import tempfile
import unittest
from pathlib import Path

_TMP = tempfile.mkdtemp()
os.environ["COMMITMENTS_VAULT"] = _TMP

import commitments


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
        commitments.write_note(p, fm, "body text\n")
        got = commitments.read_note(p)
        self.assertEqual(got["title"], fm["title"])
        self.assertEqual(got["tags"], ["elasticsearch", "idex"])
        self.assertEqual(got["sort_key"], 3)
        self.assertEqual(got["status"], "open")
        self.assertIn("body text", got["_body"])
        self.assertEqual(got["_path"], p)

    def test_colon_in_value_is_quoted_and_survives(self):
        p = self.dir / "b.md"
        commitments.write_note(p, {"title": "Fix: the thing", "link": "https://x/y?a=1"}, "")
        got = commitments.read_note(p)
        self.assertEqual(got["title"], "Fix: the thing")
        self.assertEqual(got["link"], "https://x/y?a=1")

    def test_empty_list_and_null(self):
        p = self.dir / "c.md"
        commitments.write_note(p, {"tags": [], "epic_id": None}, "")
        got = commitments.read_note(p)
        self.assertEqual(got["tags"], [])
        self.assertIsNone(got["epic_id"])

    def test_reads_human_edited_status_toggle(self):
        p = self.dir / "d.md"
        p.write_text("---\ntitle: x\nstatus: done\n---\n\n")
        self.assertEqual(commitments.read_note(p)["status"], "done")

    def test_no_frontmatter_returns_body_only(self):
        p = self.dir / "e.md"
        p.write_text("just a body\n")
        got = commitments.read_note(p)
        self.assertEqual(got["_body"].strip(), "just a body")


class TestHelpers(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(commitments.parse_date("2026-09-15"), dt.date(2026, 9, 15))
        self.assertEqual(commitments.parse_date("2026-09-15T14:22:12Z"), dt.date(2026, 9, 15))
        self.assertIsNone(commitments.parse_date(None))
        self.assertIsNone(commitments.parse_date(""))
        self.assertIsNone(commitments.parse_date("not a date"))

    def test_complexity_rank_orders_low_medium_high_missing(self):
        ranks = [commitments.complexity_rank(v) for v in ("low", "medium", "high", None)]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(commitments.complexity_rank("bogus"), commitments.MISSING_RANK)

    def test_assign_sort_keys_is_dense_rank_from_zero(self):
        notes = [{"n": "c", "k": 3}, {"n": "a", "k": 1}, {"n": "b", "k": 2}]
        out = commitments.assign_sort_keys(notes, lambda x: x["k"])
        self.assertEqual([x["n"] for x in out], ["a", "b", "c"])
        self.assertEqual([x["sort_key"] for x in out], [0, 1, 2])


class TestCommitments(unittest.TestCase):
    def setUp(self):
        commitments.COMMITMENTS_DIR = Path(tempfile.mkdtemp())

    def add(self, **kw):
        fields = dict(
            title="A commitment", summary="s", link="https://slack/x",
            committed_date="2026-09-14", due_date="2026-09-16",
            complexity="medium", tags=[],
        )
        fields.update(kw)
        return commitments.upsert_commitment(**fields)

    def mark_done(self, path):
        note = commitments.read_note(path)
        fields = {k: v for k, v in note.items() if not k.startswith("_")}
        fields["status"] = "done"
        commitments.write_note(path, fields, note.get("_body", ""))

    def test_created_note_has_full_schema_and_defaults_status_open(self):
        action, path = self.add()
        self.assertEqual(action, "created")
        note = commitments.read_note(path)
        for field in ("title", "committed_date", "due_date", "complexity",
                      "tags", "summary", "link", "status", "sort_key"):
            self.assertIn(field, note)
        self.assertEqual(note["status"], "open")
        self.assertEqual(note["committed_date"], "2026-09-14")
        self.assertEqual(note["complexity"], "medium")

    def test_file_per_row(self):
        self.add(link="https://slack/a", title="First thing")
        self.add(link="https://slack/b", title="Second thing entirely")
        self.assertEqual(len(list(commitments.COMMITMENTS_DIR.glob("*.md"))), 2)

    def test_same_link_twice_is_a_duplicate_not_a_second_row(self):
        self.add()
        action, _ = self.add()
        self.assertEqual(action, "duplicate")
        self.assertEqual(len(list(commitments.COMMITMENTS_DIR.glob("*.md"))), 1)

    def test_restatement_on_later_day_updates_due_date_in_place(self):
        _, path = self.add(link="https://slack/day1",
                           title="Send Connor the Elastic user info",
                           due_date="2026-09-16")
        action, same = self.add(link="https://slack/day8",
                                title="Send Connor Ford the Elastic user info please",
                                due_date="2026-09-23")
        self.assertEqual(action, "updated")
        self.assertEqual(same, path)
        self.assertEqual(len(list(commitments.COMMITMENTS_DIR.glob("*.md"))), 1)
        self.assertEqual(commitments.read_note(path)["due_date"], "2026-09-23")

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
        commitments.cmd_commitments(ref=dt.date(2026, 9, 15))
        order = [n["title"] for n in sorted(commitments.load_commitments(),
                                            key=lambda n: n["sort_key"])]
        self.assertEqual(order, ["Overdue one", "Due today low",
                                 "Due today high", "Future high", "Undated"])

    def test_missing_complexity_sorts_last_within_its_tier(self):
        self.add(link="l1", title="Same day high", due_date="2026-09-20", complexity="high")
        self.add(link="l2", title="Same day none", due_date="2026-09-20", complexity=None)
        commitments.cmd_commitments(ref=dt.date(2026, 9, 15))
        order = [n["title"] for n in sorted(commitments.load_commitments(),
                                            key=lambda n: n["sort_key"])]
        self.assertEqual(order, ["Same day high", "Same day none"])

    def test_done_entries_stay_on_disk_but_are_excluded_from_ranking(self):
        _, path = self.add(link="l1", title="Will be marked done")
        self.add(link="l2", title="Stays open and unrelated")
        self.mark_done(path)
        commitments.cmd_commitments(ref=dt.date(2026, 9, 15))
        self.assertTrue(path.exists())
        self.assertEqual(commitments.read_note(path)["status"], "done")
        ranked = [n["title"] for n in commitments.load_commitments()]
        self.assertEqual(ranked, ["Stays open and unrelated"])

    def test_custom_body_is_written_and_default_is_the_source_link(self):
        action, path = self.add(link="https://slack/withbody",
                               title="Parent item with checks",
                               body="- [ ] First check\n- [x] Second check")
        self.assertEqual(action, "created")
        body = commitments.read_note(path)["_body"]
        self.assertIn("- [ ] First check", body)
        self.assertIn("- [x] Second check", body)

        _, plain = self.add(link="https://slack/nobody", title="Plain item")
        self.assertIn("https://slack/nobody", commitments.read_note(plain)["_body"])

    def test_body_is_preserved_across_sort_key_recomputation(self):
        _, path = self.add(link="https://slack/keepbody",
                           title="Item whose body must survive",
                           body="- [ ] A sub task worth keeping")
        commitments.cmd_commitments(ref=dt.date(2026, 9, 15))
        self.assertIn("A sub task worth keeping", commitments.read_note(path)["_body"])

    def test_training_email_uses_the_same_schema(self):
        action, path = commitments.upsert_commitment(
            title="Complete annual security awareness training",
            summary="Assigned via email; covers phishing and data handling.",
            link="https://mail.google.com/mail/u/0/#inbox/abc123",
            committed_date="2026-09-12", due_date="2026-09-30",
            complexity="low", tags=["training", "compliance"])
        self.assertEqual(action, "created")
        note = commitments.read_note(path)
        self.assertEqual(note["status"], "open")
        self.assertEqual(note["tags"], ["training", "compliance"])
        self.assertEqual(note["committed_date"], "2026-09-12")


class TestList(unittest.TestCase):
    def setUp(self):
        commitments.COMMITMENTS_DIR = Path(tempfile.mkdtemp())

    def add(self, **kw):
        fields = dict(
            title="A commitment", summary="s", link="https://slack/x",
            committed_date="2026-09-14", due_date="2026-09-16",
            complexity="medium", tags=[],
        )
        fields.update(kw)
        return commitments.upsert_commitment(**fields)

    def test_json_default_excludes_done(self):
        self.add(link="l1", title="Open one")
        _, path = self.add(link="l2", title="Done one")
        note = commitments.read_note(path)
        fields = {k: v for k, v in note.items() if not k.startswith("_")}
        fields["status"] = "done"
        commitments.write_note(path, fields, note.get("_body", ""))
        out = json.loads(commitments.cmd_list(as_json=True))
        self.assertEqual([n["title"] for n in out], ["Open one"])

    def test_json_include_done(self):
        self.add(link="l1", title="Open one")
        _, path = self.add(link="l2", title="Done one")
        note = commitments.read_note(path)
        fields = {k: v for k, v in note.items() if not k.startswith("_")}
        fields["status"] = "done"
        commitments.write_note(path, fields, note.get("_body", ""))
        out = json.loads(commitments.cmd_list(include_done=True, as_json=True))
        self.assertEqual(sorted(n["title"] for n in out), ["Done one", "Open one"])

    def test_json_shape_matches_commitment_fields(self):
        self.add(link="l1", title="A thing")
        out = json.loads(commitments.cmd_list(as_json=True))
        self.assertEqual(set(out[0].keys()), set(commitments.COMMITMENT_FIELDS))

    def test_human_readable_default(self):
        self.add(link="l1", title="A thing", due_date="2026-09-20")
        out = commitments.cmd_list()
        self.assertIn("A thing", out)
        self.assertIn("2026-09-20", out)

    def test_human_readable_empty(self):
        self.assertIn("No commitments", commitments.cmd_list())


if __name__ == "__main__":
    unittest.main()
