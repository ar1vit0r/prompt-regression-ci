"""promptfoo custom provider: replays pre-recorded model responses instead of calling a live API.

CI runs against these fixtures so the pipeline costs $0 and has no network dependency.
Regenerate fixtures/recorded_responses.json with scripts/record.py when the prompt changes.
"""
import json
from pathlib import Path

_FIXTURES = Path(__file__).parent.parent / "fixtures" / "recorded_responses.json"
_RECORDED = json.loads(_FIXTURES.read_text())


def call_api(prompt: str, options: dict, context: dict) -> dict:
    ticket_id = context["vars"]["id"]
    recorded = _RECORDED.get(ticket_id)
    if recorded is None:
        return {"error": f"no recorded response for ticket id {ticket_id!r}"}
    return {"output": json.dumps(recorded)}
