# PTDB-1 CIFAR-10 / WRN-28-2 evidence bundle

This directory contains the validated 25-epoch WRN-28-2 architecture
replication from the Phason Training Diagnostics Benchmark. It ran on one
Kaggle Tesla T4 with the public `traintools==0.6.2` package.

The result is development evidence. It extends the earlier ResNet-18 result to
a second CIFAR-10 architecture, but does not open or validate the protected
holdout.

## Start here

- [`DUE_DILIGENCE.md`](DUE_DILIGENCE.md): claim audit, anomalies, and boundaries.
- [`CROSS_ARCHITECTURE.md`](CROSS_ARCHITECTURE.md): frozen ResNet-18 plus WRN-28-2 comparison.
- [`independent_audit.json`](independent_audit.json): machine-readable raw-row audit.
- [`RESULT.md`](RESULT.md): concise result and cross-architecture interpretation.
- [`shard_validation.json`](shard_validation.json): frozen completeness checks.
- [`bundle_manifest.json`](bundle_manifest.json): SHA-256 for every bundled file.

## Raw evidence

- `example_scores.csv.gz`: 405,000 example-level rows.
- `epoch_metrics.csv`: all 300 epoch rows.
- `run_summary.csv`: 12 completed executions.
- `paired_noninterference.csv`: three declared clean pairs.
- `errors.json`: complete error ledger, containing zero rows.
- `manifest.json`: environment, frozen configuration, and artifact hashes.
- `combined_base_summary.json` and `combined_label_noise_by_run.csv`: frozen
  ResNet-18 plus WRN-28-2 comparison.

## Reproduction

`run_shard.py` is the exact Kaggle source recorded by `manifest.json`.
`analyze_base.py` is the frozen analysis. `independent_audit.py` uses only the
Python standard library to recompute all six ranking metrics from raw rows.

```bash
python independent_audit.py
```

The canonical research ledger is in the
[TrainTools PTDB-1 directory](https://github.com/AparajeetS/Traintools/tree/main/benchmarks/ptdb_v1).
The executed notebook is
[on Kaggle](https://www.kaggle.com/code/aparajeetshadangi/phason-ptdb-1-cifar-10-wrn28-2-development).
