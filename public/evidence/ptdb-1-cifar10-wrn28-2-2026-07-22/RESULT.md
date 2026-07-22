# PTDB-1 CIFAR-10 / WRN-28-2 development result

The frozen validator and independent raw-row audit both pass. The shard contains
12 complete executions, 300 epoch rows, zero errors, three exact clean model
pairs, and 405,000 example-level score rows.

| Score | Aggregate AUROC | Run-level range |
|---|---:|---:|
| EL2N | 0.9913 | 0.9895 to 0.9931 |
| AUM | 0.9859 | 0.9781 to 0.9933 |
| Mean confidence | 0.9855 | 0.9775 to 0.9928 |
| Mean loss | 0.9750 | 0.9571 to 0.9925 |
| Random control | 0.5022 | 0.4959 to 0.5054 |
| Forgetting count | 0.3270 | 0.3025 to 0.3494 |

AUM beats mean loss in all six noisy runs. AUM beats EL2N in all three
symmetric-noise runs; EL2N beats AUM in all three class-conditional runs. The
same six-of-six regime split occurred on ResNet-18, making this a prospective
architecture replication of a task-conditioned ordering.

This is not evidence for a universal ranking. It is one dataset, two synthetic
corruption regimes, and a second convolutional architecture. The protected
holdout remains sealed.
