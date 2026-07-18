# Phason Controlled Benchmark: MBE Audit

- Target: `test_accuracy`
- Controls: `learning_rate`, `weight_decay`, `label_noise`, `seed`
- Controlled synthetic benchmark; not universal metric evidence.
- Confidence intervals use 500 row-bootstrap resamples.

| Metric | n | Raw rho | MBE partial rho | Delta | Class |
|---|---:|---:|---:|---:|---|
| `latest_plasticity_score` | 48 | -0.927 | -0.437 | +0.491 | survives |
| `latest_gns` | 48 | -0.223 | -0.332 | -0.108 | survives |
| `random_metric` | 48 | -0.014 | +0.297 | +0.311 | hidden-after-control |
| `confounded_lr_proxy` | 48 | -0.640 | +0.287 | +0.927 | sign-inversion |
| `validation_loss` | 48 | -0.945 | -0.240 | +0.705 | survives |
| `mean_update_ratio` | 48 | +0.671 | -0.207 | -0.877 | reverse-inversion |
| `mean_grad_norm` | 48 | -0.054 | -0.120 | -0.065 | weak-or-mixed |

Class counts: hidden-after-control: 1, reverse-inversion: 1, sign-inversion: 1, survives: 3, weak-or-mixed: 1.
