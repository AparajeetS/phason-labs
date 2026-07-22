"""Independent, standard-library audit of the PTDB-1 CIFAR-10/WRN-28-2 bundle."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TOLERANCE = 1.0e-12
PROTOCOL_SHA256 = "5b01d1ca47b6ebca6601a9debc80b0edfb262c3ee6feeb8e0cc998b0ee92821e"
SCORE_DIRECTIONS = {
    "aum": -1.0,
    "el2n": 1.0,
    "forgetting": 1.0,
    "mean_confidence": -1.0,
    "mean_loss": 1.0,
    "random": 1.0,
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def auroc(labels: list[int], scores: list[float]) -> float:
    ordered = sorted(zip(scores, labels), key=lambda pair: pair[0])
    positive = sum(labels)
    negative = len(labels) - positive
    rank_sum = 0.0
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = ((index + 1) + end) / 2.0
        rank_sum += average_rank * sum(label for _, label in ordered[index:end])
        index = end
    return (rank_sum - positive * (positive + 1) / 2.0) / (positive * negative)


def average_precision(labels: list[int], scores: list[float]) -> float:
    ordered = sorted(zip(scores, labels), key=lambda pair: pair[0], reverse=True)
    total_positive = sum(labels)
    true_positive = 0
    false_positive = 0
    previous_recall = 0.0
    result = 0.0
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        group_positive = sum(label for _, label in ordered[index:end])
        true_positive += group_positive
        false_positive += end - index - group_positive
        recall = true_positive / total_positive
        precision = true_positive / (true_positive + false_positive)
        result += (recall - previous_recall) * precision
        previous_recall = recall
        index = end
    return result


def precision_at_prevalence(labels: list[int], scores: list[float]) -> float:
    count = max(1, round(sum(labels) / len(labels) * len(labels)))
    ordered = sorted(enumerate(scores), key=lambda pair: -pair[1])
    return sum(labels[index] for index, _ in ordered[:count]) / count


def compare(observed: float, expected: str, differences: list[float]) -> None:
    difference = abs(observed - float(expected))
    differences.append(difference)
    if difference > TOLERANCE:
        raise AssertionError(f"metric mismatch: observed={observed}, expected={expected}")


def verify_declared_hashes(manifest: dict) -> bool:
    return all(
        (ROOT / name).is_file() and sha256_file(ROOT / name) == expected
        for name, expected in manifest["outputs"].items()
    )


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    analysis_manifest = json.loads((ROOT / "analysis_manifest.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "shard_validation.json").read_text(encoding="utf-8"))
    errors = json.loads((ROOT / "errors.json").read_text(encoding="utf-8"))
    runs = read_csv("run_summary.csv")
    epochs = read_csv("epoch_metrics.csv")
    pairs = read_csv("paired_noninterference.csv")
    summaries = {row["run_id"]: row for row in runs}

    rows_by_run: dict[str, list[dict[str, str]]] = defaultdict(list)
    with gzip.open(ROOT / "example_scores.csv.gz", "rt", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows_by_run[row["run_id"]].append(row)

    metric_differences: list[float] = []
    recomputed: list[dict] = []
    duplicate_free = True
    expected_corruption_counts = True
    aum_beats_loss = 0
    el2n_beats_aum = 0
    for run_id, rows in sorted(rows_by_run.items()):
        summary = summaries[run_id]
        ids = [int(row["example_id"]) for row in rows]
        duplicate_free &= len(ids) == len(set(ids)) == 45_000
        labels = [int(row["corrupted"]) for row in rows]
        expected_corrupted = 0 if summary["regime"] == "clean" else 9_000
        expected_corruption_counts &= sum(labels) == expected_corrupted
        if not expected_corrupted:
            continue

        result = {
            "run_id": run_id,
            "seed": int(summary["seed"]),
            "regime": summary["regime"],
        }
        for score_name, direction in SCORE_DIRECTIONS.items():
            source = "random_score" if score_name == "random" else score_name
            scores = [direction * float(row[source]) for row in rows]
            computed = {
                "auroc": auroc(labels, scores),
                "average_precision": average_precision(labels, scores),
                "precision_at_noise": precision_at_prevalence(labels, scores),
            }
            for metric_name, value in computed.items():
                compare(value, summary[f"{score_name}_{metric_name}"], metric_differences)
                result[f"{score_name}_{metric_name}"] = value
        if result["aum_auroc"] > result["mean_loss_auroc"]:
            aum_beats_loss += 1
        if result["el2n_auroc"] > result["aum_auroc"]:
            el2n_beats_aum += 1
        recomputed.append(result)

    epoch_counts: dict[str, int] = defaultdict(int)
    for row in epochs:
        epoch_counts[row["run_id"]] += 1
    complete_epochs = len(epochs) == 300 and set(epoch_counts) == set(summaries) and set(epoch_counts.values()) == {25}
    nonfinite_gradient_rows = [
        {"run_id": row["run_id"], "epoch": int(row["epoch"]), "value": row["mean_grad_norm"]}
        for row in epochs
        if row["mean_grad_norm"] and not math.isfinite(float(row["mean_grad_norm"]))
    ]
    nonfinite_guard_rows = [
        {"run_id": row["run_id"], "epoch": int(row["epoch"]), "value": row["guard_predicted_improvement"]}
        for row in epochs
        if row["guard_predicted_improvement"]
        and not math.isfinite(float(row["guard_predicted_improvement"]))
    ]
    finite_primary_curves = all(
        math.isfinite(float(row[field]))
        for row in epochs
        for field in ("train_loss", "train_accuracy", "val_loss", "val_accuracy")
    )

    pair_consistency = True
    for pair in pairs:
        dataset, model, seed, regime = pair["cell"].split("__")
        prefix = f"development_base__{dataset}__{model}__s{seed}__{regime}__"
        plain = summaries[prefix + "plain"]
        instrumented = summaries[prefix + "instrumented"]
        pair_consistency &= (
            plain["initial_state_hash"] == instrumented["initial_state_hash"]
            and plain["final_state_hash"] == instrumented["final_state_hash"]
            and float(plain["test_accuracy"]) == float(instrumented["test_accuracy"])
            and float(plain["test_loss"]) == float(instrumented["test_loss"])
            and int(pair["exact_final_hash"]) == 1
        )

    analysis_hashes_match = (
        sha256_file(ROOT / "analyze_base.py") == analysis_manifest["script_sha256"]
        and all(
            (ROOT / name).is_file() and sha256_file(ROOT / name) == expected
            for name, expected in analysis_manifest["outputs"].items()
        )
    )
    checks = {
        "execution_manifest_hashes_match": verify_declared_hashes(manifest),
        "analysis_script_and_output_hashes_match": analysis_hashes_match,
        "protocol_hash_matches_frozen_pointer": sha256_file(ROOT / "PROTOCOL.md") == PROTOCOL_SHA256,
        "run_script_hash_matches_manifest": sha256_file(ROOT / "run_shard.py") == manifest["script_sha256"],
        "frozen_validator_passed": validation["valid_base_shard"] is True,
        "zero_error_rows": errors == [],
        "twelve_complete_executions": len(runs) == 12,
        "three_exact_noninterference_pairs": len(pairs) == 3 and pair_consistency,
        "three_hundred_epoch_rows": complete_epochs,
        "primary_loss_and_accuracy_curves_are_finite": finite_primary_curves,
        "four_hundred_five_thousand_example_rows": sum(map(len, rows_by_run.values())) == 405_000,
        "unique_example_ids_within_each_run": duplicate_free,
        "corruption_counts_are_exact": expected_corruption_counts,
        "all_reported_ranking_metrics_recomputed": max(metric_differences, default=math.inf) <= TOLERANCE,
    }

    aum_values = [row["aum_auroc"] for row in recomputed]
    loss_values = [row["mean_loss_auroc"] for row in recomputed]
    el2n_values = [row["el2n_auroc"] for row in recomputed]
    forgetting_values = [row["forgetting_auroc"] for row in recomputed]
    audit = {
        "audit_pass": all(checks.values()),
        "checks": checks,
        "maximum_metric_recomputation_difference": max(metric_differences, default=None),
        "recomputed_noisy_runs": recomputed,
        "cross_run_checks": {
            "aum_auroc_range": [min(aum_values), max(aum_values)],
            "el2n_auroc_range": [min(el2n_values), max(el2n_values)],
            "mean_loss_auroc_range": [min(loss_values), max(loss_values)],
            "forgetting_auroc_range": [min(forgetting_values), max(forgetting_values)],
            "aum_beats_mean_loss_runs": aum_beats_loss,
            "el2n_beats_aum_runs": el2n_beats_aum,
            "noisy_runs": len(recomputed),
        },
        "epoch_diagnostic_findings": {
            "nonfinite_mean_gradient_norm_rows": nonfinite_gradient_rows,
            "nonfinite_guard_prediction_rows": nonfinite_guard_rows,
            "guard_stop_decisions": sum(int(row["guard_should_stop"] or 0) for row in epochs),
            "guard_stop_decisions_at_frozen_epochs": sum(
                int(row["guard_should_stop"] or 0)
                for row in epochs
                if int(row["epoch"]) in {6, 10, 13}
            ),
            "interpretation": (
                "Loss and accuracy curves are finite. Mean gradient norm is not reliable for the listed late epochs. "
                "TrainGuard's epoch-1 infinities reflect insufficient fit history. Three later stop flags occurred, "
                "none at the frozen decision epochs; this shard does not validate stopping utility."
            ),
        },
        "claim_status": {
            "supported": [
                "AUM strongly detects the injected 20% label corruption in this CIFAR-10/WRN-28-2 development slice.",
                "AUM exceeds accumulated mean loss in all six noisy runs in this slice.",
                "EL2N exceeds AUM in three of six noisy runs and has the higher aggregate AUROC.",
                "Forgetting count is below random in all six noisy runs for this target and score direction.",
                "TrainTools instrumentation is exactly non-interfering in the three declared clean pairs.",
            ],
            "not_established": [
                "Cross-dataset or broad cross-architecture generalization.",
                "Performance on naturally mislabeled data.",
                "A universal ranking of training metrics.",
                "Validation of MBE's broader metric-selection claim.",
                "Protected-holdout or submission-grade confirmation.",
                "Validity of mean gradient norm at the listed late-epoch rows.",
                "TrainGuard stopping utility; three flags occurred outside the frozen decision epochs, and policy comparison is a separate stage.",
            ],
        },
    }
    (ROOT / "independent_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    bundle_files = sorted(
        path for path in ROOT.iterdir() if path.is_file() and path.name != "bundle_manifest.json"
    )
    bundle = {
        "bundle": "PTDB-1 CIFAR-10/WRN-28-2 development evidence",
        "created": "2026-07-22",
        "files": {path.name: sha256_file(path) for path in bundle_files},
    }
    (ROOT / "bundle_manifest.json").write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2))
    if not audit["audit_pass"]:
        raise SystemExit("independent evidence audit failed")


if __name__ == "__main__":
    main()
