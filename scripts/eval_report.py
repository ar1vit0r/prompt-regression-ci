"""Print the eval table (markdown) used in CI job summaries and the README."""
from metrics import compute_metrics

if __name__ == "__main__":
    m = compute_metrics()
    print(f"### Eval report ({m['n']} fixtures, replayed, $0 cost)\n")
    print("| Metric | Result | Floor |")
    print("|---|---|---|")
    print(f"| Schema validity | {m['schema_validity_pct']}% | 100% |")
    print(f"| Category accuracy | {m['category_accuracy_pct']}% | 80% |")
    print(f"| Priority accuracy | {m['priority_accuracy_pct']}% | 80% |")
