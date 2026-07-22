# Due diligence: CIFAR-10 / ResNet-18 development shard

Audit date: 2026-07-22

## Scope

This audit asks whether the published files support the narrow statements made
about one PTDB-1 development shard. It does not use this shard to establish
cross-architecture, cross-dataset, natural-label-noise, MBE or protected-holdout
claims.

## Provenance and completeness

The independently rerun audit verified:

- the exact frozen protocol and Kaggle source hashes;
- all execution-manifest and analysis-manifest output hashes;
- 12 complete executions, 300 epoch rows and zero error rows;
- 405,000 example rows with 45,000 unique IDs per instrumented run;
- exactly 9,000 corrupted examples in each noisy run and zero in clean runs;
- three exact clean plain/instrumented model pairs;
- every published AUROC, average precision and precision-at-noise value by
  recomputing it from the compressed example rows.

The maximum discrepancy between an independently recomputed metric and the
published value was `4.0e-15`, attributable to floating-point arithmetic.

## Supported observations

Across three seeds and both frozen corruption regimes:

| Score | Aggregate AUROC | Run-level range |
|---|---:|---:|
| EL2N | 0.9932 | 0.9925 to 0.9940 |
| Mean confidence | 0.9895 | 0.9850 to 0.9938 |
| AUM | 0.9885 | 0.9827 to 0.9942 |
| Mean loss | 0.9792 | 0.9640 to 0.9934 |
| Random control | 0.4986 | 0.4957 to 0.5020 |
| Forgetting count | 0.3361 | 0.3134 to 0.3588 |

- AUM exceeded mean loss in all six noisy runs.
- AUM narrowly exceeded EL2N in all three symmetric-noise runs.
- EL2N exceeded AUM in all three class-conditional runs and therefore had the
  higher aggregate AUROC.
- Forgetting count was below random in all six runs under the prospectively
  declared direction. This is a target-specific reversal, not evidence that
  forgetting statistics are universally defective.
- AUM precision at the known 20% noise rate was 0.9143, compared with prevalence
  0.20.
- The three clean pairs had identical final parameter hashes, losses and
  accuracies. Median instrumented/plain runtime ratio was 3.01 and p90 was 3.34.

## Checks against circularity and leakage

The corruption flag is used only to evaluate rankings. AUM, EL2N, confidence,
loss and forgetting are computed from training dynamics without receiving that
flag. Seeds, corruption mechanisms, score directions, comparators, cluster unit,
bootstrap seed and primary AUM-versus-loss contrast were frozen before this
shard completed.

Precision at 20% does use the known injected prevalence to choose its cutoff, so
it is not a prevalence-free deployment estimate. AUROC and average precision are
reported alongside it. All metrics are evaluated on examples seen during
training; this is appropriate for label auditing but is not a test-set
generalization claim.

## Material limitations and anomalies

1. There is one dataset and one architecture. The bootstrap has only two
   dataset-model-regime clusters, so its interval cannot justify broad
   generalization despite three stable seeds.
2. Noise is synthetic. Symmetric replacement and the deterministic
   class-conditional `(label + 1) mod 10` mechanism do not represent the full
   structure of naturally mislabeled data.
3. The six diagnostics are related measurements of the same training process.
   Only AUM versus mean loss was the primary contrast; the full ranking is
   descriptive and is not a multiple-comparison-adjusted leaderboard.
4. Twelve epoch rows have `mean_grad_norm=inf`, concentrated at epochs 23 to 24.
   Primary losses, accuracies and final models remain finite, and matched clean
   plain/instrumented runs share the anomaly. Gradient-norm evidence from this
   shard is therefore withheld pending diagnosis.
5. TrainGuard has infinite prediction bounds at epoch 1 in each instrumented run
   because there is insufficient curve history. Later predictions are finite,
   but no stop decision fired. This shard does not validate stopping utility.
6. The 3.01x overhead measures the deliberately probe-heavy PTDB configuration,
   including per-epoch GNS and plasticity probes. It is not an estimate for a
   typical minimal TrainTools integration.
7. This is development evidence. The protected STL-10/ConvNeXt holdout remains
   sealed, and this result cannot change its rules.

## Claim status

**Supported for this slice:** strong AUM label-noise detection; a small AUM
advantage over accumulated mean loss; a regime-dependent AUM/EL2N ordering; a
forgetting-count sign reversal for this target; exact non-interference in three
clean deterministic pairs.

**Provisional:** the broader claim that metric choice changes predictably with
architecture, dataset and intervention. The running WRN shard is the first
prospective architecture replication.

**Not established:** general MBE validity, a universal metric selector, naturally
mislabeled-data performance, language-model applicability, protected-holdout
success, or JMLR-scale confirmation.
