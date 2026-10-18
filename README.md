# Low-Latency Market Data Handler

A compact event-pipeline demonstration reporting latency percentiles, event throughput, dropped messages, and an illustrative load/latency curve.

Run `python3 run.py` to write `reports/metrics.json`; run `python3 ../run_all.py` from the portfolio root to regenerate all screenshots.

![Market data performance overview](reports/project-overview.png)

![Market data pipeline](reports/project-flow.png)

Timing and throughput values are deterministic synthetic fixtures, not measurements from a specific host, feed, or production system.
