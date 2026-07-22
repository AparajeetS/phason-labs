# Due diligence: CIFAR-10 / WRN-28-2 development shard

Audit date: 2026-07-22

## Integrity

The independent audit verified all execution and analysis hashes, the frozen
protocol and exact Kaggle source, 12 complete executions, 300 epoch rows, zero
errors, 405,000 unique example rows, exact corruption counts, and all three
plain/instrumented model pairs. It recomputed AUROC, average precision, and
precision at the known noise rate for every score and noisy run.

Maximum discrepancy from the published metrics was `5.45e-15`, attributable to
floating-point arithmetic.

## Supported observations

- AUM aggregate AUROC is `0.9859` and exceeds mean loss in all six noisy runs.
- AUM minus mean-loss AUROC is `0.01087`, with frozen two-cluster interval
  `[0.00076, 0.02098]`.
- EL2N aggregate AUROC is `0.9913`.
- AUM exceeds EL2N in all three symmetric-noise runs; EL2N exceeds AUM in all
  three class-conditional runs.
- Forgetting count is below random in all six runs under the declared direction.
- All three clean instrumented runs exactly match their plain twins.

Together with the earlier ResNet-18 shard, the regime ordering now reproduces
across two architectures: AUM leads EL2N in six of six symmetric runs, and EL2N
leads AUM in six of six class-conditional runs. This supports a
regime-conditioned metric-selection hypothesis, not a universal leaderboard.

## Circularity and leakage

The corruption flag is used only to evaluate rankings. None of the scores
receives it as input. Seeds, corruption mechanisms, score directions,
comparators, cluster units, bootstrap seed, and the primary AUM-versus-loss
contrast were frozen before completion.

Precision at 20% uses the known injected prevalence to select its cutoff; AUROC
and average precision are reported alongside it. These are training-example
label-audit targets, not held-out generalization claims.

## Material limitations and adverse findings

1. Both completed shards use CIFAR-10 and related convolutional architectures.
   This is architecture replication, not cross-dataset generalization.
2. Noise is synthetic. Symmetric replacement and deterministic
   `(label + 1) mod 10` corruption do not represent natural labeling errors.
3. Only AUM versus mean loss is the primary contrast. The full score ranking is
   descriptive and not a multiplicity-adjusted leaderboard.
4. Fifteen epoch rows have `mean_grad_norm=inf`, between epochs 18 and 25.
   Primary losses, accuracies, and final models remain finite. Gradient-norm
   evidence is withheld pending diagnosis.
5. TrainGuard emitted three stop flags at epochs 17, 20, and 23, outside the
   frozen decision epochs. Two flagged runs later improved validation loss by
   `0.0691` and `0.0432`; the third improved by `0.0050`. This is potentially
   adverse evidence. Stopping utility remains unresolved until the registered
   policy comparison is run.
6. Median instrumentation overhead is `3.94x` and p90 is `4.04x` in this
   deliberately probe-heavy configuration. It is not a minimal-use estimate.
7. The protected STL-10/ConvNeXt holdout remains sealed.

## Claim status

**Supported for this development scope:** strong synthetic label-noise
detection; AUM exceeding mean loss; replicated regime-dependent AUM/EL2N
ordering across ResNet-18 and WRN-28-2; forgetting-count reversal; and exact
non-interference in six clean pairs across the two shards.

**Not established:** natural-label-noise performance, cross-dataset or broad
cross-architecture generalization, universal metric selection, MBE's complete
research thesis, TrainGuard utility, gradient-norm validity at the anomalous
epochs, language-model applicability, or protected-holdout confirmation.
