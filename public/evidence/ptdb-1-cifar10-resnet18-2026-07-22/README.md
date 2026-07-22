# PTDB-1 CIFAR-10 / ResNet-18 evidence bundle

This directory contains the first validated 25-epoch development shard of the
Phason Training Diagnostics Benchmark. It was executed on one Kaggle Tesla T4
with the public `traintools==0.6.2` package.

The result is substantial evidence for the tested slice, not proof of the broad
MBE or metric-selection thesis. WRN, ViT, CIFAR-100, SVHN and the protected
STL-10/ConvNeXt holdout were not part of this result.

## Start here

- [`DUE_DILIGENCE.md`](DUE_DILIGENCE.md): claim audit, limitations and withheld claims.
- [`independent_audit.json`](independent_audit.json): machine-readable independent checks.
- [`RESULT.md`](RESULT.md): concise frozen-analysis result.
- [`shard_validation.json`](shard_validation.json): completeness and checksum validation.
- [`bundle_manifest.json`](bundle_manifest.json): SHA-256 for every file in this bundle.

## Raw evidence

- `example_scores.csv.gz`: 405,000 example-level rows.
- `epoch_metrics.csv`: all 300 epoch rows.
- `run_summary.csv`: 12 completed executions.
- `paired_noninterference.csv`: three declared clean pairs.
- `errors.json`: complete error ledger, containing zero rows.
- `manifest.json`: execution environment, frozen config and source/output hashes.

## Reproduction and analysis

- `run_shard.py`: exact Kaggle source whose hash appears in `manifest.json`.
- `PROTOCOL.md`, `FULL_RUN_PLAN.md`, `ANALYSIS_PLAN.md`: frozen research rules.
- `analyze_base.py`: precommitted cluster-bootstrap analysis.
- `independent_audit.py`: standard-library recomputation from raw rows.
- `base_summary.json`, `label_noise_by_run.csv`, `trainguard_decision_targets.csv`:
  frozen analysis outputs.

Run the independent audit with Python 3.10 or newer:

```bash
python independent_audit.py
```

The canonical research ledger is in the
[TrainTools PTDB-1 directory](https://github.com/AparajeetS/Traintools/tree/main/benchmarks/ptdb_v1).
The executed private-kernel page is
[on Kaggle](https://www.kaggle.com/code/aparajeetshadangi/phason-ptdb-1-cifar-10-resnet18-development).
