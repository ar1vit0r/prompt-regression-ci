"""Shared metric computation, used by both the pytest suite and the eval report."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
ALLOWED_CATEGORIES = {"billing", "technical", "account", "feature_request", "other"}
ALLOWED_PRIORITIES = {"low", "medium", "high", "urgent"}


def load_fixtures() -> tuple[list[dict], dict]:
    tickets = json.loads((ROOT / "fixtures" / "tickets.json").read_text())
    recorded = json.loads((ROOT / "fixtures" / "recorded_responses.json").read_text())
    recorded = {k: v for k, v in recorded.items() if k != "_meta"}
    return tickets, recorded


def compute_metrics() -> dict:
    tickets, recorded = load_fixtures()
    n = len(tickets)
    schema_valid = category_correct = priority_correct = 0

    for t in tickets:
        resp = recorded.get(t["id"], {})
        cat, pri = resp.get("category"), resp.get("priority")
        if cat in ALLOWED_CATEGORIES and pri in ALLOWED_PRIORITIES:
            schema_valid += 1
        if cat == t["expected_category"]:
            category_correct += 1
        if pri == t["expected_priority"]:
            priority_correct += 1

    return {
        "n": n,
        "schema_validity_pct": round(100 * schema_valid / n, 1),
        "category_accuracy_pct": round(100 * category_correct / n, 1),
        "priority_accuracy_pct": round(100 * priority_correct / n, 1),
    }
