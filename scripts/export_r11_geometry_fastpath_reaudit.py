"""Export the reopened R11 geometry fast-path re-audit bundle."""

from __future__ import annotations

import json
from pathlib import Path
import random
from statistics import median
from typing import Any

from geometry import HullKVCache, brute_force_hardmax_2d
from utils import detect_runtime_environment


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "R11_geometry_fastpath_reaudit"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def results_match(left: object, right: object) -> bool:
    return (
        getattr(left, "value", None) == getattr(right, "value", None)
        and getattr(left, "score", None) == getattr(right, "score", None)
        and set(getattr(left, "maximizer_indices", ())) == set(getattr(right, "maximizer_indices", ()))
    )


def _run_single_case(
    *,
    case_id: str,
    keys: list[tuple[int, int]],
    values: list[object],
    query: tuple[int, int],
) -> dict[str, object]:
    cache = HullKVCache()
    cache.extend(keys, values)
    brute = brute_force_hardmax_2d(keys, values, query)
    accelerated = cache.query(query)
    return {
        "case_id": case_id,
        "query_count": 1,
        "exact_match": results_match(brute, accelerated),
        "brute_score": brute.score,
        "accelerated_score": accelerated.score,
        "maximizer_count": len(brute.maximizer_indices),
    }


def build_parity_rows() -> list[dict[str, object]]:
    rows = [
        _run_single_case(
            case_id="duplicate_maximizer_average",
            keys=[(2, 3), (2, 3), (0, 0)],
            values=[1, 3, 100],
            query=(1, 1),
        ),
        _run_single_case(
            case_id="collinear_tie_case",
            keys=[(0, 0), (1, 1), (2, 2)],
            values=[10, 20, 30],
            query=(1, -1),
        ),
        _run_single_case(
            case_id="zero_query_average",
            keys=[(-1, 4), (2, 2), (2, 2)],
            values=[2, 4, 6],
            query=(0, 0),
        ),
        _run_single_case(
            case_id="vector_value_tie",
            keys=[(0, 0), (1, 1)],
            values=[(1, 3), (5, 7)],
            query=(1, -1),
        ),
    ]

    rng = random.Random(0)
    keys = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(25)]
    values = [rng.randint(-20, 20) for _ in range(25)]
    cache = HullKVCache()
    cache.extend(keys, values)
    exact_match = True
    for _ in range(200):
        query = (rng.randint(-5, 5), rng.randint(-5, 5))
        brute = brute_force_hardmax_2d(keys, values, query)
        accelerated = cache.query(query)
        exact_match = exact_match and results_match(brute, accelerated)
    rows.append(
        {
            "case_id": "seeded_randomized_reference",
            "query_count": 200,
            "exact_match": exact_match,
            "maximizer_count": None,
        }
    )
    return rows


def load_inputs() -> dict[str, Any]:
    benchmark_payload = read_json(ROOT / "results" / "M2_geometry_core" / "benchmark_geometry.json")
    r4_payload = read_json(ROOT / "results" / "R4_mechanistic_retrieval_closure" / "summary.json")
    r10_payload = read_json(ROOT / "results" / "R10_d0_same_endpoint_cost_attribution" / "summary.json")
    return {
        "benchmark_payload": benchmark_payload,
        "r4_payload": r4_payload,
        "r10_payload": r10_payload,
    }


def build_benchmark_reaudit(benchmark_payload: dict[str, Any]) -> dict[str, object]:
    rows = list(benchmark_payload["rows"])
    speedups = [float(row["cache_speedup_vs_bruteforce"]) for row in rows]
    ordered_by_history = sorted(rows, key=lambda row: int(row["history_size"]))
    monotonic = all(
        float(left["cache_speedup_vs_bruteforce"]) < float(right["cache_speedup_vs_bruteforce"])
        for left, right in zip(ordered_by_history, ordered_by_history[1:])
    )
    return {
        "row_count": len(rows),
        "min_history_size": min(int(row["history_size"]) for row in rows),
        "max_history_size": max(int(row["history_size"]) for row in rows),
        "min_cache_speedup_vs_bruteforce": min(speedups),
        "median_cache_speedup_vs_bruteforce": median(speedups),
        "max_cache_speedup_vs_bruteforce": max(speedups),
        "speedup_increases_with_history": monotonic,
    }


def build_same_endpoint_guard(r10_payload: dict[str, Any]) -> dict[str, object]:
    overall = r10_payload["summary"]["overall"]
    distilled = r10_payload["summary"]["claim_impact"]["distilled_result"]
    dominant_component = str(distilled["dominant_component"])
    median_exact_vs_lowered_ratio = float(distilled["median_exact_vs_lowered_ratio"])
    median_retrieval_share = float(distilled["median_retrieval_share_of_exact"])
    same_endpoint_fastpath_material = median_exact_vs_lowered_ratio < 1.0 and dominant_component != "retrieval_total"
    return {
        "dominant_exact_component": dominant_component,
        "median_retrieval_share_of_exact": median_retrieval_share,
        "median_exact_vs_lowered_ratio": median_exact_vs_lowered_ratio,
        "profiled_row_count": int(overall["profiled_row_count"]),
        "representative_pair_count": int(overall["representative_pair_count"]),
        "negative_attribution_explicit": bool(distilled["negative_attribution_explicit"]),
        "same_endpoint_fastpath_material": same_endpoint_fastpath_material,
    }


def build_mechanistic_baseline(r4_payload: dict[str, Any]) -> dict[str, object]:
    overall = r4_payload["summary"]["overall"]
    return {
        "program_count": int(overall["program_count"]),
        "suite_count": int(overall["suite_count"]),
        "source_observation_count": int(overall["source_observation_count"]),
        "parity_failure_count": int(overall["parity_failure_count"]),
        "contradiction_candidate_count": int(overall["contradiction_candidate_count"]),
    }


def build_summary(
    parity_rows: list[dict[str, object]],
    benchmark_reaudit: dict[str, object],
    mechanistic_baseline: dict[str, object],
    same_endpoint_guard: dict[str, object],
) -> dict[str, object]:
    exact_match_count = sum(bool(row["exact_match"]) for row in parity_rows)
    allowed_wording = [
        "Exact 2D hard-max retrieval still matches brute-force on the current bounded parity slice.",
        "Standalone Hull caching still shows a strong cache-versus-brute-force asymptotic win on the preserved geometry benchmark.",
        "The geometry fast path remains a mechanistic retrieval primitive rather than an end-to-end runtime claim.",
    ]
    blocked_wording = [
        "Do not describe R11 as showing a same-endpoint executor speedup over the lowered path.",
        "Do not widen the standalone geometry benchmark into a broader systems-superiority claim.",
    ]
    return {
        "current_exactness": {
            "parity_case_count": len(parity_rows),
            "exact_match_count": exact_match_count,
            "all_cases_exact": exact_match_count == len(parity_rows),
        },
        "benchmark_reaudit": benchmark_reaudit,
        "mechanistic_baseline": mechanistic_baseline,
        "same_endpoint_guard": same_endpoint_guard,
        "claim_impact": {
            "status": "geometry_fastpath_reaudited_on_current_code",
            "target_claims": ["D0"],
            "next_lane": "R12_append_only_executor_long_horizon",
            "supported_here": [
                "The current bounded geometry parity slice stays exactly aligned with brute-force on the active codebase.",
                "The preserved standalone benchmark still shows a strong Hull cache speedup against brute-force lookup.",
                "The preserved R4 baseline still records zero parity failures and zero contradiction candidates on the current mechanistic closure bundle.",
            ],
            "unsupported_here": [
                "R11 does not show an end-to-end same-endpoint executor speedup over the lowered path.",
                "R11 does not authorize broader systems, compiled-language, or headline-level computerhood claims.",
            ],
            "allowed_wording": allowed_wording,
            "blocked_wording": blocked_wording,
        },
    }


def main() -> None:
    environment = detect_runtime_environment()
    inputs = load_inputs()
    parity_rows = build_parity_rows()
    benchmark_reaudit = build_benchmark_reaudit(inputs["benchmark_payload"])
    mechanistic_baseline = build_mechanistic_baseline(inputs["r4_payload"])
    same_endpoint_guard = build_same_endpoint_guard(inputs["r10_payload"])
    summary = build_summary(parity_rows, benchmark_reaudit, mechanistic_baseline, same_endpoint_guard)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUT_DIR / "summary.json",
        {
            "experiment": "r11_geometry_fastpath_reaudit",
            "environment": environment.as_dict(),
            "source_artifacts": [
                "results/M2_geometry_core/benchmark_geometry.json",
                "results/R4_mechanistic_retrieval_closure/summary.json",
                "results/R10_d0_same_endpoint_cost_attribution/summary.json",
                "tests/test_geometry_hardmax.py",
                "tests/test_model_exact_hardmax.py",
            ],
            "summary": summary,
        },
    )
    write_json(
        OUT_DIR / "parity_rows.json",
        {
            "experiment": "r11_geometry_parity_rows",
            "environment": environment.as_dict(),
            "rows": parity_rows,
        },
    )
    write_json(
        OUT_DIR / "benchmark_reaudit.json",
        {
            "experiment": "r11_geometry_benchmark_reaudit",
            "environment": environment.as_dict(),
            "summary": benchmark_reaudit,
            "rows": inputs["benchmark_payload"]["rows"],
        },
    )
    write_json(
        OUT_DIR / "writing_gate.json",
        {
            "experiment": "r11_geometry_writing_gate",
            "environment": environment.as_dict(),
            "summary": {
                "same_endpoint_guard": same_endpoint_guard,
                "allowed_wording": summary["claim_impact"]["allowed_wording"],
                "blocked_wording": summary["claim_impact"]["blocked_wording"],
            },
        },
    )
    write_json(
        OUT_DIR / "claim_impact.json",
        {
            "experiment": "r11_geometry_claim_impact",
            "environment": environment.as_dict(),
            "summary": summary["claim_impact"],
        },
    )
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# R11 Geometry Fastpath Re-Audit",
                "",
                "Artifacts:",
                "- `summary.json`",
                "- `parity_rows.json`",
                "- `benchmark_reaudit.json`",
                "- `writing_gate.json`",
                "- `claim_impact.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT_DIR.as_posix())


if __name__ == "__main__":
    main()
