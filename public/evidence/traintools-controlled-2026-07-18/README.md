# TrainTools controlled benchmark

Run on 18 July 2026 with the public PyPI releases of TrainTools 0.6.2 and
MBE Eval 0.4.0.

## Passed gates

- 48 of 48 paired training configurations produced identical final parameter
  hashes, validation losses, and test accuracies with and without TrainTools.
- 100 of 100 injected known failures were detected.
- 0 of 50 clean controls produced a warning.
- AUM label-noise ranking achieved 0.99995 mean AUROC and 99.5% mean
  precision at the top 20%, across five seeds.

This is a controlled synthetic classification benchmark. It is evidence of
non-interference and detector behavior under the tested conditions, not an
estimate of average production performance.

## Withheld claim

The corrected 48-row MBE audit is included for transparency but is not used as
promotional evidence. Its random negative control had partial rho +0.297 with a
95% bootstrap confidence interval of [-0.010, +0.529], missing the frozen
absolute point-estimate threshold of 0.20. See `CORRECTION_LOG.md` and
`mbe_report.md`.

## Reproduce

Run `run_benchmark.py` in an isolated Python environment. The exact script hash,
package versions, seeds, and output checksums are recorded in `manifest.json`
and `benchmark_summary.json`.
