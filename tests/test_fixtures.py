"""Fast, $0, no-network regression check over the recorded classifier fixtures.

Runs in milliseconds so it's the first line of defense; the promptfoo eval
(same replay fixtures, richer per-case report) is the second.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from metrics import compute_metrics  # noqa: E402

ACCURACY_FLOOR_PCT = 80.0


def test_schema_validity_is_100_percent():
    m = compute_metrics()
    assert m["schema_validity_pct"] == 100.0, m


def test_category_accuracy_above_floor():
    m = compute_metrics()
    assert m["category_accuracy_pct"] >= ACCURACY_FLOOR_PCT, m


def test_priority_accuracy_above_floor():
    m = compute_metrics()
    assert m["priority_accuracy_pct"] >= ACCURACY_FLOOR_PCT, m


def test_every_ticket_has_a_recorded_response():
    from metrics import load_fixtures

    tickets, recorded = load_fixtures()
    missing = [t["id"] for t in tickets if t["id"] not in recorded]
    assert not missing, f"tickets with no recorded response: {missing}"
