"""Measure a reproducible synthetic market-data event pipeline."""

from __future__ import annotations

import json
import random
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def percentile(values: list[float], quantile: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def main() -> None:
    rng = random.Random(20261007)
    latencies_us = [8.0 + rng.expovariate(1 / 2.8) + (22 if index % 997 == 0 else 0) for index in range(10_000)]
    load_levels = [10, 25, 50, 75, 100]
    p99_by_load = [round(17 + load**1.65 * 0.009, 2) for load in load_levels]
    dropped = 3
    reordered = 7
    metrics = {
        "events_processed": len(latencies_us),
        "p50_latency_us": round(percentile(latencies_us, 0.50), 2),
        "p95_latency_us": round(percentile(latencies_us, 0.95), 2),
        "p99_latency_us": round(percentile(latencies_us, 0.99), 2),
        "mean_latency_us": round(statistics.mean(latencies_us), 2),
        "throughput_events_per_sec": 2_400_000,
        "observed_load_levels_pct": load_levels,
        "dropped_events": dropped,
        "drop_rate_ppm": round(dropped / len(latencies_us) * 1_000_000, 1),
        "out_of_order_events": reordered,
        "sequence_recovery_rate_pct": 99.93,
    }
    payload = {
        "project": "Low-Latency Market Data Handler",
        "data_notice": "Synthetic timing fixture; throughput and latency are illustrative, not hardware benchmarks.",
        "metrics": metrics,
        "chart": {
            "title": "Tail latency under increasing input load",
            "x_label": "Input load (%)",
            "y_label": "p99 handler latency (us)",
            "series": [{"name": "p99 latency", "values": p99_by_load}],
        },
        "flow": ["Multicast feed", "Packet decoder", "Sequence repair", "Book builder", "Consumer API"],
        "flow_values": [0.08, 0.7, 1.4, 2.2, 0.35],
    }
    output = ROOT / "reports" / "metrics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
