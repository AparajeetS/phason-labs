# Benchmark Correction Log

## Attempt 1: Random Negative-Control Keying Defect

The first complete execution used script SHA256
`b3e220bcfe3fdca89650e924bf2b981d42b2b4a4ca68dd15fe7e923b2bf2b92b`.
Its artifacts are preserved in `attempt1_random_control_defect/`.

The paired non-interference, known-failure, and AUM gates passed. The MBE random
negative-control gate failed with partial rho `+0.277` and a 95% interval of
`[-0.095, +0.563]`.

Inspection found that the random metric was seeded only by training seed and
label-noise level. It therefore repeated the same value across the four
learning-rate and weight-decay cells in each block, producing 12 unique values
for 48 rows. This violated the intended per-run seeded random negative control.

The correction derives the RNG seed from SHA256 of the complete frozen run ID,
which includes noise, learning rate, weight decay, and seed. It creates one
deterministic random draw per configuration without selecting or searching for
a favorable seed. No protocol threshold, candidate metric, configuration,
training seed, or model setting changed. The full benchmark is rerun under the
protocol's implementation-error provision, and the corrected outcome is
accepted whether it passes or fails.
