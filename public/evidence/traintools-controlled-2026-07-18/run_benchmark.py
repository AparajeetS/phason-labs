from __future__ import annotations

import hashlib
import json
import math
import platform
import time
from pathlib import Path

import mbe_eval
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import traintools
from mbe_eval import audit_metrics, write_markdown_report
from traintools import AUMTracker, BatchInspector, GradientHealthMonitor
from traintools.callbacks.pytorch import TraintoolsTracker


ROOT = Path(__file__).resolve().parent
N_FEATURES = 20
N_CLASSES = 3
BATCH_SIZE = 64
TRAIN_STEPS = 100


class TinyClassifier(nn.Module):
    def __init__(self, n_features: int = N_FEATURES, hidden: int = 32) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(n_features, hidden),
            nn.ReLU(),
            nn.Linear(hidden, N_CLASSES),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def base_data() -> tuple[torch.Tensor, ...]:
    generator = torch.Generator().manual_seed(20260718)
    weights = torch.randn(N_FEATURES, N_CLASSES, generator=generator)

    def split(n: int) -> tuple[torch.Tensor, torch.Tensor]:
        x = torch.randn(n, N_FEATURES, generator=generator)
        logits = x @ weights + 0.8 * torch.randn(n, N_CLASSES, generator=generator)
        return x, logits.argmax(dim=1)

    return *split(768), *split(256), *split(256)


def noisy_training_data(
    data: tuple[torch.Tensor, ...], noise_fraction: float, seed: int
) -> tuple[torch.Tensor, ...]:
    train_x, clean_train_y, val_x, val_y, test_x, test_y = data
    train_y = clean_train_y.clone()
    n_flip = round(noise_fraction * len(train_y))
    if n_flip:
        generator = torch.Generator().manual_seed(seed + 50_000)
        indices = torch.randperm(len(train_y), generator=generator)[:n_flip]
        offsets = torch.randint(1, N_CLASSES, (n_flip,), generator=generator)
        train_y[indices] = (train_y[indices] + offsets) % N_CLASSES
    return train_x, train_y, val_x, val_y, test_x, test_y


def evaluate(
    model: nn.Module, x: torch.Tensor, y: torch.Tensor, loss_fn: nn.Module
) -> tuple[float, float]:
    model.eval()
    with torch.no_grad():
        logits = model(x)
        loss = float(loss_fn(logits, y))
        accuracy = float((logits.argmax(dim=1) == y).float().mean())
    model.train()
    return loss, accuracy


def parameter_hash(model: nn.Module) -> str:
    digest = hashlib.sha256()
    for value in model.state_dict().values():
        digest.update(value.detach().cpu().contiguous().numpy().tobytes())
    return digest.hexdigest()


def train_one(
    mode: str,
    label_noise: float,
    learning_rate: float,
    weight_decay: float,
    seed: int,
    clean_data: tuple[torch.Tensor, ...],
) -> dict[str, object]:
    data = noisy_training_data(clean_data, label_noise, seed)
    train_x, train_y, val_x, val_y, test_x, test_y = data
    torch.manual_seed(seed)
    model = TinyClassifier()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=learning_rate, weight_decay=weight_decay
    )
    batch_generator = torch.Generator().manual_seed(seed + 100_000)

    tracker = None
    inspector = None
    gradient_monitor = None
    grad_norms: list[float] = []
    update_ratios: list[float] = []
    batch_warnings = 0
    gradient_warnings = 0
    if mode == "traintools":
        tracker = TraintoolsTracker(
            model,
            loss_fn,
            gns_freq=25,
            plasticity_freq=25,
            earlyguard=False,
            gns_splits=2,
            verbose=False,
        )
        inspector = BatchInspector(expected_num_classes=N_CLASSES)
        gradient_monitor = GradientHealthMonitor(max_grad_norm=5.0)

    started = time.perf_counter()
    last_loss = float("nan")
    for step in range(1, TRAIN_STEPS + 1):
        indices = torch.randint(
            len(train_x), (BATCH_SIZE,), generator=batch_generator
        )
        x, y = train_x[indices], train_y[indices]
        if inspector is not None and step == 1:
            batch_warnings += len(inspector.inspect(x, y, step=step).warnings)

        optimizer.zero_grad(set_to_none=True)
        loss = loss_fn(model(x), y)
        loss.backward()
        last_loss = float(loss.detach())
        if gradient_monitor is not None and step % 25 == 0:
            result = gradient_monitor.inspect(
                model, step=step, lr=optimizer.param_groups[0]["lr"]
            )
            grad_norms.append(result.total_grad_norm)
            if result.global_update_ratio is not None:
                update_ratios.append(result.global_update_ratio)
            gradient_warnings += len(result.warnings)
        optimizer.step()
        if tracker is not None:
            tracker.step(step=step, inputs=x, targets=y)

    duration_s = time.perf_counter() - started
    val_loss, val_accuracy = evaluate(model, val_x, val_y, loss_fn)
    test_loss, test_accuracy = evaluate(model, test_x, test_y, loss_fn)
    gns = tracker.gns_history.results if tracker is not None else []
    plasticity = tracker.plasticity_history.results if tracker is not None else []
    run_id = (
        f"noise={label_noise:g}|lr={learning_rate:g}|"
        f"wd={weight_decay:g}|seed={seed}"
    )
    random_seed = int.from_bytes(
        hashlib.sha256(run_id.encode("ascii")).digest()[:8], "big"
    )
    random_metric = float(np.random.default_rng(random_seed).normal())
    return {
        "mode": mode,
        "run_id": run_id,
        "label_noise": label_noise,
        "learning_rate": learning_rate,
        "weight_decay": weight_decay,
        "seed": seed,
        "steps": TRAIN_STEPS,
        "batch_size": BATCH_SIZE,
        "duration_s": duration_s,
        "final_train_batch_loss": last_loss,
        "validation_loss": val_loss,
        "validation_accuracy": val_accuracy,
        "test_loss": test_loss,
        "test_accuracy": test_accuracy,
        "parameter_hash": parameter_hash(model),
        "mean_grad_norm": float(np.mean(grad_norms)) if grad_norms else np.nan,
        "mean_update_ratio": float(np.mean(update_ratios)) if update_ratios else np.nan,
        "latest_gns": gns[-1].gns if gns else np.nan,
        "latest_critical_batch": gns[-1].critical_batch if gns else np.nan,
        "latest_gns_regime": gns[-1].regime if gns else "",
        "latest_plasticity_score": (
            plasticity[-1].global_score if plasticity else np.nan
        ),
        "random_metric": random_metric,
        "confounded_lr_proxy": -math.log10(learning_rate) + 0.05 * random_metric,
        "batch_warning_count": batch_warnings,
        "gradient_warning_count": gradient_warnings,
        "gns_measurements": len(gns),
        "plasticity_measurements": len(plasticity),
    }


def paired_benchmark() -> tuple[pd.DataFrame, dict[str, object]]:
    clean_data = base_data()
    grid = [
        (noise, learning_rate, weight_decay, seed)
        for noise in (0.0, 0.10, 0.25)
        for learning_rate in (1e-3, 5e-3)
        for weight_decay in (0.0, 1e-2)
        for seed in (11, 22, 33, 44)
    ]
    train_one("plain_pytorch", *grid[0], clean_data)
    train_one("traintools", *grid[0], clean_data)

    rows: list[dict[str, object]] = []
    for mode in ("plain_pytorch", "traintools"):
        for index, config in enumerate(grid, start=1):
            row = train_one(mode, *config, clean_data)
            rows.append(row)
            print(
                f"paired {mode:13s} {index:02d}/{len(grid)} "
                f"acc={row['test_accuracy']:.4f} time={row['duration_s']:.3f}s",
                flush=True,
            )

    ledger = pd.DataFrame(rows)
    ledger.to_csv(ROOT / "paired_runs.csv", index=False)
    plain = ledger[ledger["mode"] == "plain_pytorch"].set_index("run_id")
    tools = ledger[ledger["mode"] == "traintools"].set_index("run_id")
    paired = tools.join(plain, lsuffix="_tools", rsuffix="_plain")
    ratios = paired["duration_s_tools"] / paired["duration_s_plain"]
    summary = {
        "paired_configurations": len(grid),
        "exact_parameter_hash_matches": int(
            (paired["parameter_hash_tools"] == paired["parameter_hash_plain"]).sum()
        ),
        "max_abs_test_accuracy_difference": float(
            (paired["test_accuracy_tools"] - paired["test_accuracy_plain"]).abs().max()
        ),
        "max_abs_validation_loss_difference": float(
            (paired["validation_loss_tools"] - paired["validation_loss_plain"]).abs().max()
        ),
        "plain_total_seconds": float(plain["duration_s"].sum()),
        "traintools_total_seconds": float(tools["duration_s"].sum()),
        "mean_overhead_percent": float(
            100 * (tools["duration_s"].mean() / plain["duration_s"].mean() - 1)
        ),
        "median_runtime_ratio": float(ratios.median()),
        "p90_runtime_ratio": float(ratios.quantile(0.90)),
        "non_interference_gate_pass": bool(
            (paired["parameter_hash_tools"] == paired["parameter_hash_plain"]).all()
            and (paired["test_accuracy_tools"] == paired["test_accuracy_plain"]).all()
            and (paired["validation_loss_tools"] == paired["validation_loss_plain"]).all()
        ),
    }
    return ledger, summary


def known_failure_benchmark(trials: int = 25) -> tuple[pd.DataFrame, dict[str, object]]:
    rows: list[dict[str, object]] = []
    batch_inspector = BatchInspector(
        expected_num_classes=N_CLASSES, class_imbalance_warn=0.95
    )
    for trial in range(trials):
        generator = torch.Generator().manual_seed(80_000 + trial)
        x = torch.randn(BATCH_SIZE, N_FEATURES, generator=generator)
        y = torch.arange(BATCH_SIZE) % N_CLASSES
        conditions: dict[str, tuple[torch.Tensor, torch.Tensor]] = {
            "clean_batch": (x.clone(), y.clone()),
            "nan_feature": (x.clone(), y.clone()),
            "invalid_label": (x.clone(), y.clone()),
            "class_imbalance": (x.clone(), torch.zeros_like(y)),
        }
        conditions["nan_feature"][0][0, 0] = float("nan")
        conditions["invalid_label"][1][0] = N_CLASSES
        conditions["class_imbalance"][1][-1] = 1
        for condition, (condition_x, condition_y) in conditions.items():
            report = batch_inspector.inspect(condition_x, condition_y, step=trial)
            expected = condition != "clean_batch"
            rows.append(
                {
                    "trial": trial,
                    "diagnostic": "batch_inspector",
                    "condition": condition,
                    "expected_warning": expected,
                    "detected_warning": not report.ok,
                    "warning_count": len(report.warnings),
                    "warnings": " | ".join(report.warnings),
                }
            )

        for condition, multiplier in (("clean_gradient", 1.0), ("amplified_gradient", 1e5)):
            torch.manual_seed(90_000 + trial)
            model = TinyClassifier()
            loss = nn.CrossEntropyLoss()(model(x), y) * multiplier
            loss.backward()
            report = GradientHealthMonitor().inspect(model, step=trial, lr=1e-3)
            expected = condition == "amplified_gradient"
            rows.append(
                {
                    "trial": trial,
                    "diagnostic": "gradient_health",
                    "condition": condition,
                    "expected_warning": expected,
                    "detected_warning": not report.ok,
                    "warning_count": len(report.warnings),
                    "warnings": " | ".join(report.warnings),
                }
            )

    frame = pd.DataFrame(rows)
    frame.to_csv(ROOT / "known_failure_results.csv", index=False)
    injected = frame[frame["expected_warning"]]
    clean = frame[~frame["expected_warning"]]
    summary = {
        "trials_per_condition": trials,
        "injected_cases": len(injected),
        "clean_control_cases": len(clean),
        "injected_detection_rate": float(injected["detected_warning"].mean()),
        "clean_false_positive_rate": float(clean["detected_warning"].mean()),
        "gate_pass": bool(
            injected["detected_warning"].all()
            and not clean["detected_warning"].any()
        ),
        "by_condition": {
            condition: {
                "detections": int(group["detected_warning"].sum()),
                "trials": len(group),
            }
            for condition, group in frame.groupby("condition")
        },
    }
    return frame, summary


def rank_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    labels = labels.astype(bool)
    ranks = pd.Series(scores).rank(method="average").to_numpy()
    positives = int(labels.sum())
    negatives = len(labels) - positives
    rank_sum = float(ranks[labels].sum())
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def aum_seed(seed: int) -> dict[str, object]:
    generator = torch.Generator().manual_seed(120_000 + seed)
    n = 600
    features = 12
    clean_y = torch.arange(n) % N_CLASSES
    means = torch.randn(N_CLASSES, features, generator=generator) * 2.0
    x = means[clean_y] + torch.randn(n, features, generator=generator)
    noisy_y = clean_y.clone()
    n_flip = round(0.20 * n)
    flipped = torch.randperm(n, generator=generator)[:n_flip]
    offsets = torch.randint(1, N_CLASSES, (n_flip,), generator=generator)
    noisy_y[flipped] = (noisy_y[flipped] + offsets) % N_CLASSES
    is_flipped = torch.zeros(n, dtype=torch.bool)
    is_flipped[flipped] = True

    torch.manual_seed(seed)
    model = TinyClassifier(n_features=features, hidden=32)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-2, weight_decay=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    tracker = AUMTracker(min_observations=3)
    step = 0
    started = time.perf_counter()
    for epoch in range(20):
        order = torch.randperm(n, generator=torch.Generator().manual_seed(seed * 100 + epoch))
        for start in range(0, n, BATCH_SIZE):
            ids = order[start : start + BATCH_SIZE]
            logits = model(x[ids])
            tracker.update(ids, logits, noisy_y[ids], step=step)
            optimizer.zero_grad(set_to_none=True)
            loss_fn(logits, noisy_y[ids]).backward()
            optimizer.step()
            step += 1

    aum = np.array([tracker.examples[i].aum for i in range(n)], dtype=float)
    labels = is_flipped.numpy()
    suspicious_score = -aum
    auc = rank_auc(labels, suspicious_score)
    k = n_flip
    lowest = np.argsort(aum)[:k]
    precision = float(labels[lowest].mean())
    return {
        "seed": seed,
        "examples": n,
        "flipped_examples": n_flip,
        "epochs": 20,
        "auroc": auc,
        "precision_at_20pct": precision,
        "random_precision_baseline": 0.20,
        "mean_aum_flipped": float(aum[labels].mean()),
        "mean_aum_clean": float(aum[~labels].mean()),
        "duration_s": time.perf_counter() - started,
    }


def aum_benchmark() -> tuple[pd.DataFrame, dict[str, object]]:
    rows = [aum_seed(seed) for seed in (101, 202, 303, 404, 505)]
    frame = pd.DataFrame(rows)
    frame.to_csv(ROOT / "aum_label_noise_results.csv", index=False)
    summary = {
        "seeds": len(frame),
        "mean_auroc": float(frame["auroc"].mean()),
        "min_auroc": float(frame["auroc"].min()),
        "mean_precision_at_20pct": float(frame["precision_at_20pct"].mean()),
        "min_precision_at_20pct": float(frame["precision_at_20pct"].min()),
        "random_precision_baseline": 0.20,
        "gate_pass": bool(
            frame["auroc"].mean() >= 0.75
            and frame["precision_at_20pct"].mean() >= 0.60
        ),
    }
    return frame, summary


def mbe_benchmark(ledger: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    instrumented = ledger[ledger["mode"] == "traintools"].copy()
    started = time.perf_counter()
    report = audit_metrics(
        instrumented,
        metrics=[
            "validation_loss",
            "mean_grad_norm",
            "mean_update_ratio",
            "latest_gns",
            "latest_plasticity_score",
            "random_metric",
            "confounded_lr_proxy",
        ],
        target="test_accuracy",
        controls=["learning_rate", "weight_decay", "label_noise", "seed"],
        bootstrap=500,
        seed=20260718,
    )
    duration_s = time.perf_counter() - started
    report.to_csv(ROOT / "mbe_results.csv", index=False)
    write_markdown_report(
        report,
        ROOT / "mbe_report.md",
        title="Phason Controlled Benchmark: MBE Audit",
        target="test_accuracy",
        controls=["learning_rate", "weight_decay", "label_noise", "seed"],
        notes=[
            "Controlled synthetic benchmark; not universal metric evidence.",
            "Confidence intervals use 500 row-bootstrap resamples.",
        ],
    )
    random_row = report[report["metric"] == "random_metric"].iloc[0]
    summary = {
        "rows": len(instrumented),
        "metrics": len(report),
        "bootstrap_resamples": 500,
        "duration_s": duration_s,
        "random_negative_control_partial_r": float(random_row["partial_r"]),
        "random_negative_control_ci": [
            float(random_row["partial_ci_low"]),
            float(random_row["partial_ci_high"]),
        ],
        "random_negative_control_gate_pass": bool(
            abs(float(random_row["partial_r"])) < 0.20
            and float(random_row["partial_ci_low"]) <= 0
            and float(random_row["partial_ci_high"]) >= 0
        ),
    }
    return report, summary


def main() -> None:
    torch.set_num_threads(1)
    manifest = {
        "protocol": "PROTOCOL.md",
        "started_at_unix": time.time(),
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "traintools": traintools.__version__,
            "mbe_eval": mbe_eval.__version__,
            "traintools_path": str(Path(traintools.__file__).resolve()),
            "mbe_eval_path": str(Path(mbe_eval.__file__).resolve()),
            "device": "cpu",
        },
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    ledger, paired_summary = paired_benchmark()
    _, failure_summary = known_failure_benchmark()
    _, aum_summary = aum_benchmark()
    _, mbe_summary = mbe_benchmark(ledger)
    final = {
        "manifest": manifest,
        "paired": paired_summary,
        "known_failures": failure_summary,
        "aum_label_noise": aum_summary,
        "mbe": mbe_summary,
        "all_primary_gates_pass": bool(
            paired_summary["non_interference_gate_pass"]
            and failure_summary["gate_pass"]
            and aum_summary["gate_pass"]
            and mbe_summary["random_negative_control_gate_pass"]
        ),
    }
    (ROOT / "benchmark_summary.json").write_text(
        json.dumps(final, indent=2), encoding="utf-8"
    )
    print(json.dumps(final, indent=2), flush=True)


if __name__ == "__main__":
    main()
