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


if __name__ == "__main__":
    unittest.main()
