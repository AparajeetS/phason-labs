# Phason Controlled Training-Diagnostics Benchmark

Protocol frozen: 2026-07-18, before execution of the larger benchmark.

## Scope

This is a controlled synthetic classification benchmark for validating software
behavior under known interventions. It is not evidence that the workload is an
average real-world training run, and it is not confirmatory evidence for the
MBE research paper.

Public packages under test:

- `traintools==0.6.2` from PyPI
- `mbe-eval==0.4.0` from PyPI
- public PyTorch installation reported in the run manifest

## Benchmark A: Paired Non-Interference And Overhead

Run 48 frozen configurations twice: plain PyTorch and PyTorch instrumented with
TrainTools. The grid is:

- training-label noise: 0%, 10%, 25%;
- learning rate: 0.001, 0.005;
- weight decay: 0, 0.01;
- seed: 11, 22, 33, 44.

Each run trains the same MLP for 100 minibatch steps on the same synthetic data.
Instrumented runs add one batch inspection and four measurements each of
gradient health, GNS, and representation plasticity.

Primary non-interference gate:

- 48/48 exact final parameter-hash matches;
- maximum paired test-accuracy difference = 0;
- maximum paired validation-loss difference = 0.

Runtime overhead is reported descriptively with median, mean, and p90 paired
ratios. There is no pass threshold because this tiny CPU workload is not a
representative performance benchmark.

## Benchmark B: Known-Failure Detection

Evaluate independent clean and injected batches for:

- NaN feature injection;
- out-of-range label injection;
- 98% dominant-class imbalance;
- loss scaling large enough to produce an exploding-gradient warning.

Website gate:

- each injected condition must be detected in every trial;
- the corresponding clean controls must emit no warnings.

## Benchmark C: Injected Label-Noise Ranking

For each of five seeds, flip exactly 20% of training labels, train for 20 full
epochs, and track Area Under the Margin (AUM) using stable example IDs. Rank all
examples from lowest to highest AUM.

Primary endpoints:

- AUROC for identifying deliberately flipped labels;
- precision among the lowest-AUM 20% of examples.

Website gate:

- mean AUROC >= 0.75;
- mean precision@20% >= 0.60;
- report every seed, not only the mean.

The random-ranking precision baseline is 0.20.

## Benchmark D: MBE Audit

Audit the 48 instrumented training rows against clean test accuracy while
controlling for learning rate, weight decay, injected label-noise fraction, and
seed. Candidate metrics are validation loss, gradient norm, update ratio, GNS,
plasticity, a seeded random negative control, and a deliberately confounded
learning-rate proxy.

The MBE table is descriptive. A metric claim requires its bootstrap interval
not to cross zero. The random negative control passes its software sanity gate
when `abs(partial_r) < 0.20` and its interval crosses zero.

## Rerun Policy

Reruns are allowed only for implementation errors, interrupted execution, or
environment failure. Every correction must be documented. Outcome-dependent
changes to seeds, thresholds, configurations, or candidate metrics are not
allowed.

## Website Language

Allowed language must say `controlled synthetic benchmark` and link to the
protocol and machine-readable results. It must not say `real-world average`,
`production-proven`, or imply that this benchmark validates universal metric
reliability.
