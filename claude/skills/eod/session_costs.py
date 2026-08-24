#!/usr/bin/env python3
"""Aggregate Claude Code token costs from JSONL session transcripts.

Usage:
    python3 session_costs.py [YYYY-MM-DD] [--json]

Defaults to today if no date given.
--json emits machine-readable JSON for script consumption.
"""

import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Pricing per 1M tokens (USD). Matched by model name prefix.
PRICING = {
    "claude-opus-4":   {"input": 15.00, "cache_write": 18.75, "cache_read": 1.50,  "output": 75.00},
    "claude-sonnet-4": {"input":  3.00, "cache_write":  3.75, "cache_read": 0.30,  "output": 15.00},
    "claude-haiku-4":  {"input":  0.80, "cache_write":  1.00, "cache_read": 0.08,  "output":  4.00},
    "claude-opus-3":   {"input": 15.00, "cache_write": 18.75, "cache_read": 1.50,  "output": 75.00},
    "claude-sonnet-3": {"input":  3.00, "cache_write":  3.75, "cache_read": 0.30,  "output": 15.00},
    "claude-haiku-3":  {"input":  0.25, "cache_write":  0.30, "cache_read": 0.03,  "output":  1.25},
}


def get_pricing(model: str) -> dict | None:
    for prefix, prices in PRICING.items():
        if model.startswith(prefix):
            return prices
    return None


def cost_for_usage(usage: dict, prices: dict) -> float:
    per_m = 1_000_000
    return (
        usage.get("input_tokens", 0)                 * prices["input"]       / per_m
        + usage.get("cache_creation_input_tokens", 0) * prices["cache_write"] / per_m
        + usage.get("cache_read_input_tokens", 0)     * prices["cache_read"]  / per_m
        + usage.get("output_tokens", 0)               * prices["output"]      / per_m
    )


def aggregate(target_date: str) -> dict:
    by_model: dict[str, dict] = defaultdict(lambda: {
        "input_tokens": 0, "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0, "output_tokens": 0,
        "cost_usd": 0.0, "turns": 0,
    })
    by_session: dict[str, dict] = defaultdict(lambda: {
        "model": "", "cwd": "",
        "input_tokens": 0, "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0, "output_tokens": 0,
        "cost_usd": 0.0, "turns": 0,
    })
    unknown_models: set[str] = set()

    if not PROJECTS_DIR.is_dir():
        return _empty(target_date)

    for jsonl_path in PROJECTS_DIR.glob("**/*.jsonl"):
        session_id = jsonl_path.stem
        try:
            with open(jsonl_path, errors="replace") as f:
                for raw in f:
                    raw = raw.strip()
                    if not raw:
                        continue
                    try:
                        obj = json.loads(raw)
                    except json.JSONDecodeError:
                        continue

                    if obj.get("type") != "assistant":
                        continue
                    if (obj.get("timestamp") or "")[:10] != target_date:
                        continue

                    msg = obj.get("message") or {}
                    usage = msg.get("usage")
                    model = msg.get("model") or ""
                    if not usage or not model:
                        continue

                    prices = get_pricing(model)
                    if prices is None:
                        if model and not model.startswith("<"):
                            unknown_models.add(model)
                        continue

                    cost = cost_for_usage(usage, prices)

                    m = by_model[model]
                    m["input_tokens"]                 += usage.get("input_tokens", 0)
                    m["cache_creation_input_tokens"]  += usage.get("cache_creation_input_tokens", 0)
                    m["cache_read_input_tokens"]      += usage.get("cache_read_input_tokens", 0)
                    m["output_tokens"]                += usage.get("output_tokens", 0)
                    m["cost_usd"]                     += cost
                    m["turns"]                        += 1

                    s = by_session[session_id]
                    s["model"] = model
                    s["cwd"]   = s["cwd"] or obj.get("cwd") or ""
                    s["input_tokens"]                 += usage.get("input_tokens", 0)
                    s["cache_creation_input_tokens"]  += usage.get("cache_creation_input_tokens", 0)
                    s["cache_read_input_tokens"]      += usage.get("cache_read_input_tokens", 0)
                    s["output_tokens"]                += usage.get("output_tokens", 0)
                    s["cost_usd"]                     += cost
                    s["turns"]                        += 1

        except OSError:
            continue

    total_cost = sum(m["cost_usd"] for m in by_model.values())
    total_tokens = {
        "input_tokens":                sum(m["input_tokens"]                for m in by_model.values()),
        "cache_creation_input_tokens": sum(m["cache_creation_input_tokens"] for m in by_model.values()),
        "cache_read_input_tokens":     sum(m["cache_read_input_tokens"]     for m in by_model.values()),
        "output_tokens":               sum(m["output_tokens"]               for m in by_model.values()),
    }

    return {
        "date":            target_date,
        "total_cost_usd":  total_cost,
        "total_tokens":    total_tokens,
        "by_model":        dict(by_model),
        "by_session":      dict(by_session),
        "unknown_models":  sorted(unknown_models),
    }


def _empty(target_date: str) -> dict:
    return {
        "date": target_date, "total_cost_usd": 0.0,
        "total_tokens": {"input_tokens": 0, "cache_creation_input_tokens": 0,
                         "cache_read_input_tokens": 0, "output_tokens": 0},
        "by_model": {}, "by_session": {}, "unknown_models": [],
    }


def _fmt_tokens(n: int) -> str:
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def format_text(data: dict) -> str:
    lines = [f"Claude Code costs — {data['date']}"]
    if not data["by_model"]:
        lines.append("  No sessions found.")
        return "\n".join(lines)

    t = data["total_tokens"]
    lines.append(f"  Total: ${data['total_cost_usd']:.4f}")
    lines.append(
        f"  Tokens: {_fmt_tokens(t['input_tokens'])} input, "
        f"{_fmt_tokens(t['output_tokens'])} output, "
        f"{_fmt_tokens(t['cache_read_input_tokens'])} cache read, "
        f"{_fmt_tokens(t['cache_creation_input_tokens'])} cache write"
    )

    if len(data["by_model"]) > 1:
        lines.append("  By model:")
        for model, m in sorted(data["by_model"].items()):
            lines.append(f"    {model}: ${m['cost_usd']:.4f} ({m['turns']} turns)")

    if data["unknown_models"]:
        lines.append(f"  Unpriced models: {', '.join(data['unknown_models'])}")

    return "\n".join(lines)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != ""]
    output_json = "--json" in args
    args = [a for a in args if a != "--json"]

    target = args[0] if args else date.today().isoformat()
    result = aggregate(target)

    if output_json:
        print(json.dumps(result, indent=2))
    else:
        print(format_text(result))
